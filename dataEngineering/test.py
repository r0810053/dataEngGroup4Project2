

from dataEngineering.assets import get_stories_from_feed
from dataEngineering.mongo import store_data, get_all_data
from dataEngineering.cleaning import clean_data, store_dataframe
from dataEngineering.statistics import dataframe_for_word_count

# Some example code to test the functions

stories = get_stories_from_feed()
# print(stories)
store_data("bronze", "feed", stories)
df = clean_data("bronze", "feed", ["id"])
print(df.head(5))
store_dataframe("silver", "feed", df)
print(list(get_all_data("silver", "feed")))