import streamlit as st
import pandas as pd
import requests
import psycopg2

# Define the database URL
DATABASE_URL = "postgres://unxlzyodujmmnt:1d1c0ca2e94c4afb0de91ae7f614fa2810a14c5596f2adb690e6e4c330639e61@ec2-34-206-79-150.compute-1.amazonaws.com:5432/d7vdfa4mkfup83"
API_URL = "https://nameless-badlands-48731-8e09975e0b40.herokuapp.com"

# Define the list of vendors and services
VENDORS = ["Akbar Travel", "Travel City LLC", "Skysouq", "Cochin Travel", "World Travel", "SIB/ZIP", "BM/Online", "Alhind"]
SERVICES = ["Air Ticket - One Way", "Air Ticket - Round Trip", "Hotel", "Insurance inbound", "Insurance Outbound", "Air Ticket Cancelation Charges", "Visa Tourist Oman 26B", "Visa Tourist Oman 26A", "Visa Tourist Dubai 30, Cancelation/VD -Air Ticket"]

def fetch_contacts():
    try:
        # Connect to the database
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = conn.cursor()

        # Fetch contacts from the contacts table
        cursor.execute("SELECT id, name FROM contacts;")
        contacts = cursor.fetchall()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        return contacts
    except psycopg2.Error as e:
        st.error(f"Error fetching contacts: {e}")
        return []

def create_invoice(data):
    try:
        # Send a POST request to create an invoice
        response = requests.post(f"{API_URL}/invoices", json=data)
        response.raise_for_status()  # Raise an exception for HTTP errors
        st.success("Invoice created successfully")
    except requests.RequestException as e:
        st.error(f"Error creating invoice: {e}")

def main():
    # Set page title and layout
    st.set_page_config(page_title="Transactions Viewer", layout="wide")

    # Fetch contacts from the database
    contacts = fetch_contacts()
    contact_names = [contact[1] for contact in contacts] if contacts else []

    # Add form for creating invoice
    with st.form(key="create_invoice_form"):
        st.subheader("Create Invoice")
        st.write("Please fill out the details below to create an invoice:")

        # Dropdown for selecting contact name
        selected_contact_name = st.selectbox("Contact Name", contact_names)

        # Find the corresponding contact ID based on the selected name
        selected_contact_id = None
        for contact in contacts:
            if contact[1] == selected_contact_name:
                selected_contact_id = contact[0]
                break

        # Dropdown for selecting vendor
        selected_vendor = st.selectbox("Vendor", VENDORS)

        # Dropdown for selecting service
        selected_service = st.selectbox("Service", SERVICES)

        # Input fields for creating an invoice
        net_amount = st.number_input("Net Amount", min_value=0.0)
        sold_amount = st.number_input("Sold Amount", min_value=0.0)
        
        # Input field for passenger
        passenger = st.text_input("Passenger")

        submitted = st.form_submit_button("Create")

        if submitted:
            # Validate inputs
            if not selected_contact_id:
                st.error("Please select a valid contact.")
            elif net_amount <= 0 or sold_amount <= 0:
                st.error("Net Amount and Sold Amount must be positive.")
            elif not passenger:
                st.error("Passenger field cannot be empty.")
            else:
                # Prepare data for creating an invoice
                invoice_data = {
                    "service": selected_service,
                    "net_amount": net_amount,
                    "sold_amount": sold_amount,
                    "contact_id": selected_contact_id,
                    "vendor": selected_vendor,
                    "passenger": passenger  # Add passenger data
                }

                # Create the invoice
                create_invoice(invoice_data)

if __name__ == "__main__":
    main()
