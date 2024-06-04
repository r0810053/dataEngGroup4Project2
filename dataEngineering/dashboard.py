import polars as pl
import streamlit as st
from dataEngineering.mongo import get_dataframe_from_mongoDB

def concatenate_column_strings(df, column_name):
    """
    Concatenates all strings from a specified column in a Pandas DataFrame into a single string.
    
    Parameters:
        df (pd.DataFrame): Input Pandas DataFrame.
        column_name (str): Name of the column containing strings to be concatenated.
    
    Returns:
        str: Concatenated string of all values from the specified column.
    """
    # Ensure the column contains strings (convert to string type if needed)
    df[column_name] = df[column_name].astype(str)
    
    # Concatenate all strings from the specified column into a single string
    concatenated_string = ''.join(df[column_name])
    
    return concatenated_string



df = get_dataframe_from_mongoDB('gold', 'word-count')
st.write("Enter the word you want to search in the database.")
user_input = st.text_input("Enter text here", "AI")
string1 = concatenate_column_strings(df, 'title')
string2 = concatenate_column_strings(df, 'summary')
string3 = concatenate_column_strings(df, 'text')
summary_string = string1 + string2 + string3

apple = 0
for word in summary_string.split():
    test_str = ''.join(letter for letter in word if letter.isalnum())
    if test_str.lower() == user_input.lower():
        apple += 1
        
# Streamlit app
st.title("Word Count")

st.write(f"{user_input} appears {apple} times in the database.")

