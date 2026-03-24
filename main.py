import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os
import requests


from functions import load_data, add_key_word_to_category, categorize, save_categories

st.set_page_config(page_title="Data Visualization App", layout="wide")
 
category_file = "categories.json"


if "categories" not in st.session_state:
    st.session_state.categories = {
        "Uncategorized": []
    }

if os.path.exists(category_file):
    with open(category_file, "r") as f:
        st.session_state.categories = json.load(f)
    
def main():

    st.title("Streamlit + FastAPI Example")

    if st.button("Call Backend"):
        response = requests.get("http://127.0.0.1:8000/hello")
        data = response.json()

        st.write(data["message"])




    st.title("Financing Dashboard")
    st.write("This dashboard visualizes financing data from a CSV file.")
    uploaded_file = st.file_uploader("Transactions upload", type=["csv"])





    if uploaded_file is not None:
        df = load_data(uploaded_file)

        if df is not None:

            debits_df = df[df["Debit/Credit"] == "Debit"].copy()
            credits_df = df[df["Debit/Credit"] == "Credit"].copy()

            st.session_state.debits_df = debits_df.copy()

            tab1, tab2 = st.tabs(["Expenses (Debits)", "Payments (Credits)"])

            with tab1: 
                new_category = st.text_input("Add new category")
                new_category_button = st.button("Add")


                if new_category_button and new_category:
                    if new_category not in st.session_state.categories:
                        st.session_state.categories[new_category] = []
                        save_categories(category_file)
                        st.rerun()

                st.subheader("Your Expenses")

                edited_df = st.data_editor(
                    st.session_state.debits_df[["Date", "Details", "Amount", "Category"]],
                    column_config={
                        "Date": st.column_config.DateColumn("Date", format="DD/MM/YYYY"),
                        "Amount": st.column_config.NumberColumn("Amount", format = "%.2f AED"),
                        "Category": st.column_config.SelectboxColumn(
                            "Category",
                            options=list(st.session_state.categories.keys())
                        )
                    },
                    hide_index= True,
                    use_container_width=True,
                    key="category_editor"
                )

                save_button = st.button("Apply Changes", type = "primary")
                if save_button:
                    for idx, row in edited_df.iterrows():
                        new_category = row["Category"]
                        if row["Category"] == st.session_state.debits_df.at[idx, "Category"]:
                            continue

                        details = row["Details"]
                        st.session_state.debits_df.at[idx, "Category"] = new_category
                        add_key_word_to_category(new_category, details)

                st.subheader('Summary')
                category_totals = st.session_state.debits_df.groupby("Category")["Amount"].sum().reset_index()
                category_totals = category_totals.sort_values("Amount", ascending=False)

                st.dataframe(
                    category_totals,
                    column_config={
                        "Amount": st.column_config.NumberColumn("Amount", format="%.2f AED")
                    },
                    use_container_width=True,
                    hide_index=True
                )
                fig = px.pie(
                    category_totals,
                    values="Amount",
                    names="Category",
                    title = "Expenses by Category"
                )
                st.plotly_chart(fig, use_container_width=True)

            with tab2:

                st.subheader("Payments Summary")
                total_payments = credits_df["Amount"].sum()
                st.metric("Total Payments", f"{total_payments:,.2f}")
                st.write(credits_df)

main()