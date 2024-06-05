from dagster import asset
import polars as pl
from dataEngineering.mongo import store_data, get_all_data, get_dataframe_from_mongoDB
from dataEngineering.assets import download_hackernews, download_arxiv
import pandas as pd

def clean_data(layer: str, database: str, subset: list) -> pd.DataFrame:
    """
    Cleans the data by removing duplicate records based on the specified subset of columns.

    Args:
        layer (str): The layer of the data.
        database (str): The database to retrieve the data from.
        subset (list): A list of column names to consider when removing duplicates.

    Returns:
        pd.DataFrame: The cleaned dataframe.

    """
    df = get_dataframe_from_mongoDB(layer, database)

    df = pd.DataFrame(df)

    if 'timestamp' in df.columns and 'id' in df.columns:
        df = df.sort_values(by=['timestamp', *subset], ascending=False)
        df = df.drop_duplicates(subset='id', keep='first')
    else:
        df = df.drop_duplicates(subset=subset, keep='first')

    return df


def store_dataframe(layer: str, database: str, df: pd.DataFrame) -> None:
    """
    Stores a pandas DataFrame in a specified layer and database.

    Parameters:
    - layer (str): The layer where the data will be stored.
    - database (str): The database where the data will be stored.
    - df (pd.DataFrame): The DataFrame to be stored.

    Returns:
    None
    """
    store_data(layer, database, df.to_dict('records'))

@asset(deps=[download_hackernews])
def clean_hacker_news() -> None:
    df = clean_data('bronze', 'hacker-news', ['id'])
    store_dataframe('silver', 'hacker-news', df)

@asset(deps=[download_arxiv])
def clean_arxiv() -> None:
    df = clean_data('bronze', 'arxiv', ['id'])
    store_dataframe('silver', 'arxiv', df)

@asset(deps=[download_hackernews])
def clean_hacker_news_comments() -> None:
    df = clean_data('bronze', 'hacker-news-comments', ['id'])
    store_dataframe('silver', 'hacker-news-comments', df)
