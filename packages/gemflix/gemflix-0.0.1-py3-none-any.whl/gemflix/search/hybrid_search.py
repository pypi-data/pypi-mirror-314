import sys
import os
import webbrowser
from typing import Any, List

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import numpy as np
import pandas as pd
from dotenv import load_dotenv
from couchbase.search import SearchRequest
from couchbase.options import SearchOptions
from couchbase.vector_search import VectorQuery, VectorSearch

from utils.database import connect_to_couchbase
from utils.generative_ai import generate_embeddings

# Load environment variables
load_dotenv()
DB_CONN_STR = os.getenv("DB_CONN_STR")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_BUCKET = os.getenv("DB_BUCKET")
DB_SCOPE = os.getenv("DB_SCOPE")
DB_COLLECTION = os.getenv("DB_COLLECTION")
INDEX_NAME = os.getenv("INDEX_NAME")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")


def _search_couchbase(
    scope: Any,
    index_name: str,
    embedding_key: str,
    search_text: str = None,
    search_embedding: list = None,
    fields: List[str] = ["*"],  # all fields by default
):
    """Hybrid search using Python SDK in Couchbase, with additional filters."""
    # Step 1: Generate vector embeddings from the search text if not provided
    if search_embedding is None:
        if search_text == "":
            return "Missing search text."
        else:
            search_embedding = generate_embeddings(search_text)

    # Step 2: Create the vector query
    vector_query = VectorQuery(embedding_key, search_embedding, 1000)  # k

    # Step 3: Perform the vector search
    search_req = SearchRequest.create(VectorSearch.from_vector_query(vector_query))

    docs_with_score = []

    try:
        # Perform the search
        search_iter = scope.search(
            index_name,
            search_req,
            SearchOptions(
                # limit=k,
                fields=fields
            ),
        )

        # Parse the results
        for row in search_iter.rows():
            docs_with_score.append(
                {"fields": row.fields, "score": row.score}
            )  # score = similarity score

    except Exception as e:
        raise e

    return docs_with_score


def _display_html(movie_list, search_text):
    """Generate and display an HTML page of movie results for the given search text.

    Args:
        movie_list (list): List of movie data with details like title, rating, and poster.
        search_text (str): The search query used for fetching the movie results.

    Returns:
        None
    """

    # base html structure
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>GemFlix Search Results"</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0px 200px;
            }}
            .movie-container {{
                display: flex;
                flex-wrap: wrap;
                margin: 20px;
            }}
            .movie {{
                display: flex;
                margin: 20px 0;
                width: 100%;
                border-bottom: 1px solid #ddd;
                padding-bottom: 20px;
            }}
            .movie img {{
                max-width: 200px;
                max-height: 300px;
                margin-right: 20px;
            }}
            .movie-details {{
                flex-grow: 1;
            }}
            .movie-title {{
                font-size: 1.5em;
                margin: 0;
            }}
            .movie-overview {{
                margin: 10px 0;
            }}

        </style>
    </head>
    <body>
        <h1 style="text-align:left; padding: 20px;">Showing search results for "{search_text}"</h1>
        <div class="movie-container">
    """

    # generate html content for each movie in movie list
    for movie in movie_list:
        fields = movie["fields"]
        title = fields["Series_Title"]
        year = fields["Released_Year"]
        rating = fields["IMDB_Rating"]
        runtime = fields["Runtime"]
        overview = fields["Overview"]
        poster = fields["Poster_Link"]

        html_content += f"""
        <div class="movie">
            <img src="{poster}" alt="{title} Poster">
            <div class="movie-details">
                <h2 class="movie-title">{title} ({year})</h2>
                <p class="movie-overview">{overview}</p>
                <p><strong>IMDB Rating:</strong> {rating} | <strong>Runtime:</strong> {runtime}</p>
            </div>
        </div>
        """

    # close html structure
    html_content += """
        </div>
    </body>
    </html>
    """

    # write generated content to html file
    file_path = os.path.abspath("output/movies.html")

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(html_content)

    # display results in browser
    webbrowser.open(f"file://{file_path}")


def keyword_search(search_text):
    """Perform a keyword search using Couchbase, and generate an HTML page displaying movie results based on the search text.

    Args:
        movie_list (list): A list of movie data where each item contains `fields` with movie information (e.g., title, release year, IMDB rating).
        search_text (str): The search query used for fetching the movie results.

    Returns:
        None
    """

    # open the bucket, scope, and collection
    cluster = connect_to_couchbase(DB_CONN_STR, DB_USERNAME, DB_PASSWORD)
    bucket = cluster.bucket(DB_BUCKET)
    scope = bucket.scope(DB_SCOPE)

    # get results of keyword search
    movie_list = _search_couchbase(
        scope,
        INDEX_NAME,
        "Overview_embedding",  # embedding_key
        search_text=search_text,
    )

    # if _search_couchbase returns an error message (string), return it directly
    if isinstance(movie_list, str):
        return movie_list

    # display html page with search results
    _display_html(movie_list, search_text)

    return movie_list


def _get_overview_embeddings(movie_list):
    """
    Retrieves the overview embeddings for a list of movies from the Couchbase database.

    Args:
        movie_list (list): List of movie titles to query.

    Returns:
        list: A list of overview embeddings corresponding to the provided movie titles.
    """

    formatted_string = ", ".join(f'"{movie}"' for movie in movie_list)

    query = f"""
    SELECT movies.Overview_embedding
    FROM `{DB_BUCKET}`.`{DB_SCOPE}`.`{DB_COLLECTION}` AS movies
    WHERE movies.Series_Title IN [{formatted_string}]
    """

    # connect to couchbase cluster
    cluster = connect_to_couchbase(DB_CONN_STR, DB_USERNAME, DB_PASSWORD)

    # execute query
    try:
        result = cluster.query(query)
        embeddings = []

        for row in result:
            embeddings.append(row["Overview_embedding"])

    except Exception as e:
        print(f"Error executing query: {e}")

    return embeddings


def _process_recommendations(raw_results, exclusion_list, k):
    """
    Processes raw vector search results and returns the top 'k' recommendations based on score.

    Args:
        raw_results (list): List of raw vectory search results.
        exclusion_list (list): List of movie titles to exclude from the results.
        k (int): The number of top recommendations to return.

    Returns:
        list: A list of the top 'k' recommendations after filtering and sorting by score.
    """

    # flatten and convert the raw results to a list
    raw_results = np.array(raw_results).flatten().tolist()

    # remove results where 'Series_Title' is in the exclusion list
    filtered_results = [
        result
        for result in raw_results
        if result["fields"]["Series_Title"] not in exclusion_list
    ]

    # use dictionary to remove duplicates
    unique_results = {
        result["fields"]["Series_Title"]: result for result in filtered_results
    }

    # sort filtered results by score in descending order
    sorted_results = sorted(
        unique_results.values(), key=lambda x: x["score"], reverse=True
    )

    # take top 10 results
    top_k = sorted_results[:k]

    return top_k


def recommend(collection, k=5, collection_name=None):
    """
    Generates top 'k' movie recommendations based on a collection of movies.

    Args:
        collection: Collection object to retrieve data.
        collection_name (str): The name of the collection base recommendations on.
        k (int): The number of top recommendations to return.

    Returns:
        list: A list of the top 'k' movie recommendations based on the search results.
    """

    # open the bucket, scope, and collection
    cluster = connect_to_couchbase(DB_CONN_STR, DB_USERNAME, DB_PASSWORD)
    bucket = cluster.bucket(DB_BUCKET)
    scope = bucket.scope(DB_SCOPE)

    # get movie_list and embeddings from collection
    collection_df = collection.display_collection(collection_name)
    if len(collection_df) == 0: # empty because collection doesn't exist
        return collection_df

    movie_list = collection_df["movie_title"].tolist()
    collection_embeddings = _get_overview_embeddings(movie_list)

    # get results of keyword search
    results = []

    for embedding in collection_embeddings:
        r = _search_couchbase(
            scope,
            INDEX_NAME,
            "Overview_embedding",  # embedding_key
            search_embedding=embedding,
        )

        # for row in results:
        #     print(row)

        results.append(r)  # add vector search results for one movie

    top_k = _process_recommendations(results, movie_list, k)

    # format results
    columns = [
        "Series_Title",
        "Released_Year",
        "Director",
        "Runtime",
        "Genre",
        "Overview",
        "IMDB_Rating",
    ]

    # list comprehension to extract fields and build rows
    rows = [
        {col: result["fields"].get(col, None) for col in columns} for result in top_k
    ]

    # convert the list of rows to a dataframe
    top_k_df = pd.DataFrame(rows, columns=columns)
    return top_k_df
