import streamlit as st
import pandas as pd

def get_data() -> pd.DataFrame:
    # get the data, assuming its a csv file
    data = pd.read_csv('data.csv')
    return data

def concatenate_column_strings(df, column_name):
    """
    Concatenates all strings from a specified column in a Pandas DataFrame into a single string.
    
    Parameters:
        df (pd.DataFrame): Input Pandas DataFrame.
        column_name (str): Name of the column containing strings to be concatenated.
    
    Returns:
        str: Concatenated string of all values from the specified column.
    """
    df[column_name] = df[column_name].astype(str)
    concatenated_string = ''.join(df[column_name])
    
    return concatenated_string

df = get_data()
string1 = concatenate_column_strings(df, 'title')
string2 = concatenate_column_strings(df, 'summary')
string3 = concatenate_column_strings(df, 'text')
summary_string = string1 + string2 + string3

user_input = st.text_input("Enter a word to search for in the database:", "the")

count = 0
for word in summary_string.split():
    test_str = ''.join(letter for letter in word if letter.isalnum())
    if test_str.lower() == user_input.lower():
        count += 1
        
# Streamlit app
st.title("Word Count")
st.write(f"{user_input} appears {count} times in the database.")