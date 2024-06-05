#add text from hacker news and comments, summary of arxiv papers, and store in MongoDB
from dagster import asset

from dataEngineering.cleaning import clean_arxiv, clean_hacker_news, clean_hacker_news_comments
from dataEngineering.mongo import store_data, get_dataframe_from_mongoDB
import polars as pl
import pandas as pd


def dataframe_for_word_count() -> pd.DataFrame:
    """
    Retrieves data from MongoDB collections ('hacker-news', 'feed', 'hacker-news-comments')
    and creates a DataFrame with columns 'title', 'summary', and 'text'.

    Returns:
        pd.DataFrame: DataFrame with columns 'title', 'summary', and 'text'.
    """
    df1 = get_dataframe_from_mongoDB('silver', "hacker-news")
    df2 = get_dataframe_from_mongoDB('silver', "feed")
    df3 = get_dataframe_from_mongoDB('silver', "hacker-news-comments")
    
    if not df2.empty:
        title = df1['title']
        summary = df2['summary']
        text = df3['text']
        
        df4 = pd.DataFrame({
            'title': title,
            'summary': summary,
            'text': text
        })
    else:
        title = df1['title']
        text = df3['text']
        
        df4 = pd.DataFrame({
            'title': title,
            'text': text
        })
    
    return df4

@asset(deps=[clean_hacker_news, clean_arxiv, clean_hacker_news_comments])
def store_golden_data() -> None:
    df = dataframe_for_word_count()
    store_data('gold', 'word-count', df.to_dict('records'))