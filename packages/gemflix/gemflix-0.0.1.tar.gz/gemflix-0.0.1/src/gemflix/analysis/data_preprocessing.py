import sys
import os
import logging
from dotenv import load_dotenv
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
from collection.collection import MovieCollection
from utils.database import connect_to_couchbase

# Load environment variables
load_dotenv()
DB_CONN_STR = os.getenv("DB_CONN_STR")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_BUCKET = os.getenv("DB_BUCKET")
DB_SCOPE = os.getenv("DB_SCOPE")
DB_COLLECTION = os.getenv("DB_COLLECTION")


def _get_user_collection_with_movies(
    user_collection: MovieCollection, collection_name: str = None
) -> pd.DataFrame:
    """
    Returns a collection data with movie information.

    Args:
        user_collection (MovieCollection): The user's collection.
        collection_name (str): The name of the collection (optional).

    Returns:
        pd.DataFrame: user collection data with movies.
    """

    collection_data = user_collection.display_collection(collection_name)

    movie_list = collection_data["movie_title"].tolist()

    # formatting as string for N1QL query
    formatted_string = ", ".join(f'"{movie}"' for movie in movie_list)

    # connect to couchbase cluster
    cluster = connect_to_couchbase(DB_CONN_STR, DB_USERNAME, DB_PASSWORD)

    # query to get genre fields
    query = f"""
    SELECT movies.Series_Title
            , movies.Genre
            , movies.Poster_Link
            , movies.Director
            , movies.Star1
            , movies.Star2
            , movies.Star3
            , movies.Star4
    FROM `{DB_BUCKET}`.`{DB_SCOPE}`.`{DB_COLLECTION}` AS movies
    WHERE Series_Title IN [{formatted_string}]
    """

    # execute query
    try:
        result = cluster.query(query)

        # put data into dataframe
        movie_df = pd.DataFrame([row for row in result])
        merged_df = collection_data.merge(
            movie_df, left_on="movie_title", right_on="Series_Title", how="inner"
        )
        merged_df = merged_df.drop(columns=["Series_Title"])

    except Exception as e:
        logging.error(f"Error executing query:  {e}")
    return merged_df


def report_basic_stats(
    user_collection: MovieCollection, collection_name: str = None
) -> dict:
    """
    Preprocess the data for analysis and statistics.

    Args:
        user_collection (MovieCollection): The user's collection.
        collection_name (str): The name of the collection (optional).

    Returns:
        dict: a dictionary with computed statistics.
    """

    # Load the collection data with movies
    collection_with_movies = _get_user_collection_with_movies(
        user_collection, collection_name
    )
    # User ID
    user_id = collection_with_movies["user_id"].values[0]

    # Rate distribution
    rate_distribution = collection_with_movies["rate"].value_counts().sort_index()

    # Movies watched per year
    collection_with_movies["year"] = pd.to_datetime(
        collection_with_movies["watched_date"]
    ).dt.year
    movies_per_year = collection_with_movies["year"].value_counts().sort_index()

    # Top-rated movies
    top_rated_movies = collection_with_movies.loc[
        collection_with_movies["rate"] == collection_with_movies["rate"].max(),
        ["movie_title", "Poster_Link"],
    ]

    # Lowest-rated movies
    lowest_rated_movie = collection_with_movies.loc[
        collection_with_movies["rate"] == collection_with_movies["rate"].min(),
        ["movie_title", "Poster_Link"],
    ]

    # Return results as a dictionary
    stats = {
        "user_id": user_id,
        "rate_distribution": rate_distribution,
        "movies_per_year": movies_per_year,
        "top_rated_movies": top_rated_movies,
        "lowest_rated_movie": lowest_rated_movie,
    }
    return stats


def calculate_top_directors(
    user_collection: MovieCollection, collection_name: str = None
) -> dict:
    """
    Preprocess the data to compute the top 5 directors with their movies and average ratings.

    Args:
        user_collection (MovieCollection): The user's collection.
        collection_name (str): The name of the collection (optional).

    Returns:
        dict: a dictionary containing the results.
    """
    # Load the collection data with movies
    collection_with_movies = _get_user_collection_with_movies(
        user_collection, collection_name
    )

    # Group by Director and calculate movie count
    director_group = collection_with_movies.groupby("Director").agg(
        movie_count=("movie_title", "count"),
        avg_rating=("rate", "mean"),
        movies=(
            "movie_title",
            lambda x: ", ".join(x),
        ),  # Join movie titles into a single string
    )

    # Sort by movie count and get top 5 directors
    top_directors = (
        director_group.sort_values("movie_count", ascending=False).head(5).reset_index()
    )

    return top_directors


def stacked_bar_preprocess(
    user_collection: MovieCollection,
    collection_name: str,
    period: str,
    year: int = None,
) -> pd.DataFrame:
    """
    Preprocess the data to compute the genre trends

    Args:
        user_collection (MovieCollection): The user's collection.
        collection_name (str): The name of the collection.
        period (str): The period criterion ('month' or 'year').
        year (int): The specific year to filter the data (optional).

    Returns:
        pd.DataFrame: The preprocessed data.
    """

    # ensure that year is provided if period is "Month"
    if period.lower() == "month" and year is None:
        raise ValueError("Year must be provided when the period is 'Month'.")

    # Load the collection data with movies
    merged_df = _get_user_collection_with_movies(user_collection, collection_name)

    # convert watched_date to datetime and extract month
    merged_df["watched_date"] = pd.to_datetime(merged_df["watched_date"])

    # if period is 'Month' and year is provided, filter for that year
    if period.lower() == "month" and year:
        # Filter for movies watched in the specified year
        merged_df = merged_df[merged_df["watched_date"].dt.year == year]

    to_period = period[0].upper()
    merged_df[period] = merged_df["watched_date"].dt.to_period(to_period)

    # split the 'Genre' column into multiple rows
    merged_expanded = merged_df.assign(
        Genre=merged_df["Genre"].str.split(", ")
    ).explode("Genre")

    # group by period and Genre, count the number of movies
    grouped = (
        merged_expanded.groupby([period, "Genre"]).size().reset_index(name="count")
    )

    # pivot the data to have genres as columns
    pivot_table = grouped.pivot(index=period, columns="Genre", values="count").fillna(0)

    # normalize counts to percentages per period
    pivot_table = round(
        pivot_table.div(pivot_table.sum(axis=1), axis=0).fillna(0) * 100, 2
    )

    return pivot_table
