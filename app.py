import streamlit as st
import pandas as pd
import requests

# Define the API endpoint for transactions
TRANSACTIONS_API_URL = "https://nameless-badlands-48731-8e09975e0b40.herokuapp.com/transactions"

def fetch_transactions():
    # Fetch transactions from the API
    response = requests.get(TRANSACTIONS_API_URL)
    if response.status_code == 200:
        data = response.json()
        return pd.DataFrame(data) if isinstance(data, list) else None
    else:
        return None

def main():
    # Set page title and layout
    st.set_page_config(page_title="Transactions Viewer", layout="wide")

    # Add Transactions button
    st.button("Add Transactions", key="add_transactions_button")

    # Fetch transactions from the API
    transactions = fetch_transactions()

    # Display transactions
    if transactions is not None:
        st.title("Transactions")
        st.write("Here are the transactions:")
        st.dataframe(transactions.fillna(""))
    else:
        st.error("Failed to fetch transactions. Please try again later.")

if __name__ == "__main__":
    main()
