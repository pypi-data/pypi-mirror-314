import os
import logging
from datetime import datetime

import pandas as pd
from dotenv import load_dotenv
from couchbase.options import QueryOptions
from couchbase.exceptions import DocumentNotFoundException

from collection.collection_interface import CollectionInterface
from utils.database import connect_to_couchbase
from utils.exceptions import NoLogException


class MovieCollection(CollectionInterface):
    def __init__(self):
        """
        Initialize the MovieCollection with Couchbase connection details.
        """
        load_dotenv()
        self.document_id = None
        self.user_id = None
        self.cluster = connect_to_couchbase(
            os.getenv("DB_CONN_STR"), os.getenv("DB_USERNAME"), os.getenv("DB_PASSWORD")
        )
        self.bucket = self.cluster.bucket(os.getenv("DB_BUCKET"))
        self.scope = self.bucket.scope(os.getenv("DB_SCOPE"))
        self.movies_collection = self.scope.collection(os.getenv("DB_COLLECTION"))
        self.user_collection = self.scope.collection(os.getenv("DB_USER_COLLECTION"))

    def _get_document(self) -> dict:
        """
        Retrieve the user document from the database.

        Returns:
            dict: The user document, or an empty dictionary if not found.
        """
        try:
            result = self.user_collection.get(self.document_id)
            return result.value
        except DocumentNotFoundException as e:
            return dict()

    def _get_collection_names(self) -> list[str]:
        """
        Retrieve all collection names for the current user.

        Returns:
            list: A list of collection names.
        """
        query = f"""
                    SELECT u.collections 
                      FROM `movie_app_data`.`movie_app`.user_collection AS u 
                     WHERE META(u).id = $1
                """
        search_pattern = f"{self.document_id}"

        try:
            result = self.scope.query(
                query, QueryOptions(positional_parameters=[search_pattern])
            )
            return [
                collection["name"]
                for item in result
                for collection in item["collections"]
            ]
        except Exception as e:
            logging.error(f"Failed to get collection names: {e}")
            return []

    def _search_movie(self, search_text: str) -> list:
        """
        Search for a movie in the movies collection by title.

        Args:
            search_text (str): The text to search for in movie titles.

        Returns:
            list: A list of matching movies sorted by IMDB rating.
        """
        query = f"""
                    SELECT META(m).id AS _id
                         , m.Series_Title
                      FROM `movie_app_data`.`movie_app`.movies AS m 
                     WHERE LOWER(m.Series_Title) LIKE $1
                  ORDER BY m.IMDB_Rating DESC
                     LIMIT 1
                """
        search_pattern = f"%{search_text.lower()}%"

        try:
            result = self.scope.query(
                query, QueryOptions(positional_parameters=[search_pattern])
            )
            return [row for row in result]
        except Exception as e:
            logging.error(f"Failed to search movies: {e}")
            return []

    def sign_up(self, user_id: str) -> str:
        """
        Sign up a new user with a default collection.

        Args:
            user_id (str): The ID of the new user.

        Returns:
            str: A success or error message.

        """
        self.user_id = user_id
        self.document_id = f"collection_{self.user_id}"

        # check if user exists.
        if self._get_document():
            return "You already signed up \U0001FAF6"

        timestamp = datetime.now().isoformat()
        collection_data = {
            "user_id": self.user_id,
            "created_at": timestamp,
            "updated_at": timestamp,
            "collections": [
                {"name": "My Collection", "created_at": timestamp, "movies": []}
            ],
        }
        self.user_collection.upsert(self.document_id, collection_data)
        return "Successfully signed up \U0001F3A5!"

    def create_collection(self, collection_name) -> str:
        """
        Create a new custom collection for the user.

        Args:
            collection_name (str): The name of the new collection.

        Returns:
            str: A success or error message.
        """

        # check if the collection already exists.
        if collection_name in self._get_collection_names():
            return f"{collection_name} collection already exists"

        document_data = self._get_document()
        timestamp = datetime.now().isoformat()
        document_data["collections"].append(
            {"name": collection_name, "created_at": timestamp, "movies": []}
        )
        document_data["updated_at"] = timestamp
        self.user_collection.upsert(self.document_id, document_data)
        return f"Successfully created the collection {collection_name} !"

    def delete_collection(self, collection_name: str) -> str:
        """
        Delete a collection.

        Args:
            collection_name (str): The name of the collection to delete.

        Returns:
            str: A success or error message.
        """

        # check if the collection exists.
        if not collection_name in self._get_collection_names():
            return f"Collection {collection_name} doesn't exist \U0001FAE2"

        # delete the collection
        document_data = self._get_document()
        timestamp = datetime.now().isoformat()
        updated_collections = [
            collection
            for collection in document_data["collections"]
            if collection["name"] != collection_name
        ]
        document_data["collections"] = updated_collections
        document_data["updated_at"] = timestamp
        self.user_collection.upsert(self.document_id, document_data)
        return f"Successfully deleted the collection {collection_name}!"

    def display_collection(self, collection_name: str = None):
        """
        Display all movies in the user's collections or a specific collection.

        Args:
            collection_name (str): The name of the collection to display (optional).

        Returns:
            pd.DataFrame: A DataFrame containing the collection's movies.
        """
        document_data = self._get_document()

        movies_data = []
        for collection in document_data["collections"]:
            if collection_name and collection["name"] != collection_name:
                continue

            for movie in collection["movies"]:
                movies_data.append(
                    {
                        "user_id": document_data["user_id"],
                        "collection_name": collection["name"],
                        "num": movie["num"],
                        "movie_title": movie["movie_title"],
                        "rate": movie["rate"],
                        "watched_date": movie["watched_date"],
                        "notes": movie["notes"],
                    }
                )

        df = pd.DataFrame(movies_data)

        if df.empty:
            raise NoLogException

        return df

    def add_log(
        self,
        collection_name: str,
        movie_title: str,
        rate: int,
        watched_date: str = None,
        notes: str = "",
    ):
        """
        Add a movie log to a specified collection.

        Args:
            collection_name (str): The name of the collection.
            movie_title (str): The title of the movie to add.
            rate (int): The user's rating for the movie.
            watched_date (str): The date the movie was watched (optional).
            notes (str): Additional notes about the movie (optional).

        Returns:
            str: A success or error message.
        """
        watched_date = watched_date or datetime.now().strftime("%Y-%m-%d")
        movie_id = ""

        # check if the movie is in movies collection
        searched_movie = self._search_movie(movie_title)
        if searched_movie:
            movie_id = searched_movie[0]["_id"]
            movie_title = searched_movie[0]["Series_Title"]

        # Find the target collection
        document_data = self._get_document()
        collection_data = next(
            (
                collection
                for collection in document_data["collections"]
                if collection["name"] == collection_name
            ),
            None,
        )

        if collection_data is None:
            return f"Collection '{collection_name}' does not exist."

        # Check if the movie already exists in the collection
        movie_titles = [movie["movie_title"] for movie in collection_data["movies"]]
        if movie_title in movie_titles:
            return f"Movie '{movie_title}' already exists in the collection '{collection_name}'."

        new_movie = {
            "num": len(collection_data["movies"]) + 1,
            "movie_id": movie_id,
            "movie_title": movie_title,
            "rate": rate,
            "watched_date": watched_date,
            "notes": notes,
        }
        collection_data["movies"].append(new_movie)
        document_data["updated_at"] = datetime.now().isoformat()
        self.user_collection.replace(self.document_id, document_data)
        return f"Movie '{movie_title}' successfully added to collection '{collection_name}'."

    def delete_log(self, collection_name, movie_title) -> str:
        """
        Delete a movie log by title from a specified collection.

        Args:
            collection_name (str): The name of the collection.
            movie_title (str): The title of the movie to delete.

        Returns:
            str: A success or error message.
        """

        # check if the collection exists.
        if not collection_name in self._get_collection_names():
            return f"Collection {collection_name} doesn't exist \U0001FAE2"

        # Find the target collection
        timestamp = datetime.now().isoformat()
        document_data = self._get_document()
        collection_data = next(
            (
                collection
                for collection in document_data["collections"]
                if collection["name"] == collection_name
            ),
            None,
        )
        updated_movies = [
            movie
            for movie in collection_data["movies"]
            if movie["movie_title"].lower() != movie_title.lower()
        ]
        if len(updated_movies) == len(collection_data["movies"]):
            return f"Movie with title '{movie_title}' not found in collection '{collection_name}'."
        collection_data["movies"] = updated_movies
        document_data["updated_at"] = timestamp
        self.user_collection.upsert(self.document_id, document_data)
        return f"Movie with title '{movie_title}' successfully deleted from collection '{collection_name}'."
