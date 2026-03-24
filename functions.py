import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os


def save_categories(category_file):
    with open(category_file, "w") as f:
        json.dump(st.session_state.categories, f)

def categorize(df):

    df["Category"] = "Uncategorized"

    for category, keywords in st.session_state.categories.items(): 
        if category == "Uncategorized" or not keywords:
            continue

        lowered_keywords = [keyword.lower().strip() for keyword in keywords]

        for idx, row in df.iterrows():
            details = row["Details"].lower().strip()

            if details in lowered_keywords:
                df.at[idx, "Category"] = category

    return df



def categorize(base_fn):

    def enhanced_fn(base_fn):

        
        df["Category"] = "Uncategorized"

        for category, keywords in st.session_state.categories.items(): 
            if category == "Uncategorized" or not keywords:
                continue

            lowered_keywords = [keyword.lower().strip() for keyword in keywords]

            for idx, row in df.iterrows():
                details = row["Details"].lower().strip()

                if details in lowered_keywords:
                    df.at[idx, "Category"] = category

        return df

    return df



def load_data(file):
    try:

        #DATA PROCCESSING
        df = pd.read_csv(file)

        df.columns = [col.strip() for col in df.columns]

        df["Amount"] = df["Amount"].str.replace(",", "").astype(float)
        df["Date"] = pd.to_datetime(df["Date"], format="%d %b %Y")

        return categorize(df)
    

    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None
    
    

def add_key_word_to_category(category,keyword):
    keyword = keyword.strip()

    if keyword and keyword not in st.session_state.categories[category]:
        st.session_state.categories[category].append(keyword)
        save_categories()
        return True
    
    return False

