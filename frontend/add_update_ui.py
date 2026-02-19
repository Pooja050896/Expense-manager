import streamlit as st
import requests
from datetime import datetime

api_url = "http://localhost:8000"

def add_update_tab():
    selected_date = st.date_input("Enter Date", datetime(2024, 8, 1), label_visibility="collapsed")
    key_prefix = str(selected_date)
    response = requests.get(f"{api_url}/expenses/{selected_date}")
    if response.status_code == 200:
        existing_expenses= response.json()
        #st.write(existing_expenses)
    else:
        st.error("Request failed")
        existing_expenses = []

    categories=["Rent","Shopping","Food","Entertainment","Other"]

    with st.form(key="Expense_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.text("Amount")
        with col2:
            st.text("Category")
        with col3:
            st.text("Notes")

        expenses = []
        for i in range(6):
            if i < len(existing_expenses):
                amount = existing_expenses[i]['amount']
                category = existing_expenses[i]["category"]
                notes = existing_expenses[i]["notes"]
                #st.write(amount, category, notes)
            else:
                amount = 0.0
                category = "Shopping"
                notes = ""


            col1,col2,col3 = st.columns(3)

            with col1:

                amount_input=st.number_input(label="Amount", value=amount,min_value=0.0, step=1.0,
                                             key=f"{key_prefix}_Amount_{i}",label_visibility="collapsed")

            with col2:
                category_input = st.selectbox(label="Category", options=categories, index=categories.index(category),
                                               key=f"{key_prefix}_Category_{i}",label_visibility="collapsed")
            with col3:
                notes_input=st.text_input(label="notes", value=notes,label_visibility="collapsed",key=f"{key_prefix}_notes_{i}")

            expenses.append({
            "amount": amount_input,
            "category": category_input,
            "notes": notes_input,
            })

        submit_button =  st.form_submit_button()
        if submit_button:
            filtered_expense = [expense for expense in expenses if expense['amount'] > 0.0]

            response = requests.post(f"{api_url}/expenses/{selected_date}", json=filtered_expense)
            st.write(response.json())
            if response.status_code == 200:
                st.success("Expenses updated successfully!")
            else:
                st.error("Failed to update expenses.")