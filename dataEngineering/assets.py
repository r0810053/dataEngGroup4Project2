import requests
import feedparser
from bs4 import BeautifulSoup
import csv
import datetime
import os
from pathlib import Path
from dagster import Backoff, Jitter, RetryPolicy, asset
from .mongo import store_data


def get_stories(page: int) -> list:
    """
    Retrieves a list of stories from the Hacker News website.

    Args:
        page (int): The page number to retrieve stories from.

    Returns:
        list: A list of stories in JSON format.
    """
    request = requests.get(f'https://news.ycombinator.com/news?p={page}')
    soup = BeautifulSoup(request.text, 'html.parser')

    trs = soup.find_all('tr', {'class': 'athing'})
    stories = []
    for tr in trs:
        story = requests.get(f'https://hacker-news.firebaseio.com/v0/item/{tr["id"]}.json?print=pretty')
        stories.append(story.json())
        # sleep(0.5)
    return stories

def get_comments(stories: list) -> list:
    """
    Retrieves comments from Hacker News API for each story in the given list.

    Args:
        stories (list): A list of stories.

    Returns:
        list: A list of comments retrieved from the Hacker News API.
    """
    comments = []
    for story in stories:
        if 'kids' not in story:
            continue
        for comment_id in story['kids']:
            comment = requests.get(f'https://hacker-news.firebaseio.com/v0/item/{comment_id}.json?print=pretty')
            comments.append(comment.json())
            # sleep(0.5)
    return comments

def get_stories_from_pages(pages: int) -> list:
    """
    Retrieves stories from multiple pages.

    Args:
        pages (int): The number of pages to retrieve stories from.

    Returns:
        list: A list of stories retrieved from the specified number of pages.
    """
    stories = []
    for page in range(1, pages + 1):
        stories += get_stories(page)
    return stories

def get_stories_from_feed() -> list:
    """
    Retrieves a list of stories from the RSS feed.

    Returns:
        list: A list of stories from the RSS feed.
    """
    feed = feedparser.parse('https://rss.arxiv.org/rss/cs')
    stories = []
    for entry in feed.entries:
        stories += {entry}
    return stories


retry_policy = RetryPolicy(
    max_retries=3,
    delay=1,
    backoff=Backoff.EXPONENTIAL,
    jitter=Jitter.PLUS_MINUS,
)

import datetime
from pathlib import Path

def create_write_path(name: str) -> str:
    """
    Create a write path for the given name.

    Args:
        name (str): The name to be included in the path.

    Returns:
        str: The created write path.

    """
    month_num = datetime.datetime.now().month
    year_num = datetime.datetime.now().year
    path = f"data-lake/bronze/{name}/{year_num}/{month_num}"
    Path(path).mkdir(parents=True, exist_ok=True)
    return path


def save_dataset(stories, name):
    """
    Save a dataset of stories to a CSV file.

    Args:
        stories (list[dict]): A list of dictionaries representing stories.
        name (str): The name of the dataset.

    Returns:
        None
    """
    current_day = str(datetime.datetime.now().day)
    file_path = os.path.join(create_write_path(name), f"{current_day}.csv")

    with open(file_path, 'w', newline='', encoding='utf-8') as output_file:
        # Get all possible fieldnames from the stories
        fieldnames = set().union(*(story.keys() for story in stories))
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)

        writer.writeheader()
        for story in stories:
            writer.writerow(story)

@asset(retry_policy=retry_policy)
def download_hackernews() -> None:
    stories = get_stories_from_pages(5)
    store_data('bronze', "hacker-news", stories)
    comments = get_comments(stories)
    store_data('bronze', "hacker-news-comments", comments)

@asset(retry_policy=retry_policy)
def download_arxiv() -> None:
    stories = get_stories_from_feed()
    store_data('bronze', "feed", stories)
