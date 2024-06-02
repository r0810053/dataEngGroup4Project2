import csv
import datetime
from pathlib import Path
from dagster import Backoff, Jitter, RetryPolicy, asset
import requests
import feedparser
from bs4 import BeautifulSoup

retry_policy = RetryPolicy(
    max_retries=3,
    delay=1,
    backoff=Backoff.EXPONENTIAL,
    jitter=Jitter.PLUS_MINUS,
)


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


def save_dataset(stories: list, name: str) -> None:
    """
    Save a list of stories to a CSV file.

    Args:
        stories (list): A list of dictionaries representing stories.
        name (str): The name of the dataset.

    Returns:
        None
    """
    day = datetime.datetime.now().day
    path = create_write_path(name)
    keys = stories[0].keys()
    with open(f"{path}/{day}.csv", 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(stories)


@asset(retry_policy=retry_policy)
def download_hackernews() -> None:
    stories = get_stories_from_pages(5)
    save_dataset(stories, "hacker-news")
    comments = get_comments(stories)
    save_dataset(comments, "hacker-news-comments")

@asset(retry_policy=retry_policy)
def download_arxiv() -> None:
    stories = get_stories_from_feed()
    save_dataset(stories, "arxiv")