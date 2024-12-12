import sys
import os
import pandas as pd
from dotenv import load_dotenv
from typing import Any, Dict, List

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.database import connect_to_couchbase

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


def _build_filter_conditions(filters: List[Dict[str, Any]]) -> str:
    """Helper function to dynamically build WHERE conditions based on filters."""
    if not filters:
        return ""

    where_conditions = []

    for filter in filters:
        field = filter["field"]
        condition = filter["condition"]
        values = filter["values"]

        if condition == "BETWEEN":
            where_conditions.append(f"{field} BETWEEN {values[0]} AND {values[1]}")

        elif condition == ">":
            where_conditions.append(f"{field} > {values[0]}")

        elif condition == "<":
            where_conditions.append(f"{field} < {values[0]}")

        elif condition == "=":
            where_conditions.append(f"{field} = {values[0]}")

        # matching substring in Genre
        elif condition == "LIKE":
            if isinstance(values[0], str):
                where_conditions.append(f"{field} LIKE '%{values[0]}%'")
            else:
                # multiple values if list is provided
                like_conditions = [f"{field} LIKE '%{value}%'" for value in values]
                where_conditions.append(f"({' OR '.join(like_conditions)})")

    return " AND ".join(where_conditions)  # Combine all conditions with AND


def _build_sort_clause(sort_by: tuple[str]) -> str:
    """Helper function to build ORDER BY clause from sort_by tuple."""
    if not sort_by:
        return ""  # no sorting if list is empty

    column, direction = sort_by

    # handle formatting errors
    if direction not in ["ASC", "DESC"]:
        raise ValueError("Invalid sort direction. Use 'ASC' or 'DESC'.")

    return f"ORDER BY {column} {direction}"  # what if we want more than 1


def filter_results(
    filters: List[Dict[str, Any]] = [], limit: int = 100, sort_by: tuple[str] = ()
):
    """
    Filter documents with dynamic conditions passed by user.

    Example filters format:
    filters = [
        {"field": "Released_Year", "condition": ">", "values": [2000]},
        {"field": "IMDB_Rating", "condition": "BETWEEN", "values": [7, 10]}
    ]
    """
    # build WHERE condition dynamically based on filters
    where_clause = _build_filter_conditions(filters)

    # build ORDER BY clause from the sort_by tuple
    sort_clause = _build_sort_clause(sort_by)

    # base N1QL query
    query = f"""
    SELECT movies.*
    FROM `{DB_BUCKET}`.`{DB_SCOPE}`.`{DB_COLLECTION}` AS movies
    """
    if where_clause:
        query += f" WHERE {where_clause}"

    if sort_clause:
        query += f" {sort_clause}"

    if limit > 0:
        query += f" LIMIT {limit}"
    else:
        query += f" LIMIT 100" # default

    # connect to couchbase cluster
    cluster = connect_to_couchbase(DB_CONN_STR, DB_USERNAME, DB_PASSWORD)

    # execute query
    try:
        result = cluster.query(query)

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
        rows = [{col: row.get(col, None) for col in columns} for row in result]

        # convert the list of rows to a dataframe
        result_df = pd.DataFrame(rows, columns=columns)
        return result_df

    except Exception as e:
        print(f"Error executing query: {e}")
