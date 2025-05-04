import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# App configuration
st.set_page_config(
    page_title="Personal Finance Manager",
    page_icon="💰",
    layout="wide"
)

# API configuration
API_URL = "http://localhost:5000/api"

# Initialize session state
if 'expenses' not in st.session_state:
    st.session_state.expenses = []

# Helper functions
def fetch_expenses():
    try:
        response = requests.get(f"{API_URL}/expenses")
        if response.status_code == 200:
            st.session_state.expenses = response.json()
        else:
            st.error("Failed to fetch expenses")
    except requests.exceptions.RequestException:
        st.error("Could not connect to the server")

def add_expense(name, amount, category):
    try:
        response = requests.post(
            f"{API_URL}/expenses",
            json={"name": name, "amount": amount, "category": category}
        )
        if response.status_code == 201:
            st.success("Expense added successfully!")
            fetch_expenses()
            return True
        else:
            st.error(f"Failed to add expense: {response.text}")
    except requests.exceptions.RequestException:
        st.error("Could not connect to the server")
    return False

def delete_expense(expense_id):
    try:
        response = requests.delete(f"{API_URL}/expenses/{expense_id}")
        if response.status_code == 200:
            st.success("Expense deleted successfully!")
            fetch_expenses()
        else:
            st.error(f"Failed to delete expense: {response.text}")
    except requests.exceptions.RequestException:
        st.error("Could not connect to the server")

# UI Components
def show_expense_list():
    st.subheader("Your Expenses")
    if not st.session_state.expenses:
        st.info("No expenses found. Add some expenses to get started!")
        return
    
    df = pd.DataFrame(st.session_state.expenses)
    
    # Additional frontend normalization (redundant but safe)
    if 'category' in df.columns:
        df['category'] = df['category'].str.capitalize()
    
    # Show data table
    st.dataframe(df, use_container_width=True)
    
    # Show charts
    tab1, tab2 = st.tabs(["By Category", "Bar Chart"])
    
    with tab1:
        if 'category' in df.columns:
            category_summary = df.groupby("category")["amount"].sum().reset_index()
            fig = px.pie(category_summary, names='category', values='amount', title='Expenses by Category')
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        if 'category' in df.columns:
            category_summary = df.groupby("category")["amount"].sum().reset_index()
            fig = px.bar(category_summary, x='category', y='amount', title="Most Spent by Category", color='category')
            st.plotly_chart(fig, use_container_width=True)

def show_add_expense_form():
    with st.expander("Add New Expense", expanded=False):
        with st.form("add_expense_form"):
            name = st.text_input("Expense Name", max_chars=50)
            amount = st.number_input("Amount", min_value=0.01, step=0.01, format="%.2f")
            category = st.selectbox(
                "Category",
                ["Food", "Transport", "Entertainment", "Bills", "Shopping", "Other"]
            )
            
            submitted = st.form_submit_button("Add Expense")
            if submitted and name and amount:
                if add_expense(name, amount, category):
                    st.rerun()

# Main App
def main():
    st.title("💰 Personal Finance Manager")
    st.write("Track and manage your personal expenses")
    
    fetch_expenses()
    
    show_add_expense_form()
    show_expense_list()

if __name__ == "__main__":
    main()