import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Define a function to import the data set
def import_data():
    return pd.read_excel("../data/dummy_data.xlsx")

# Define a function to preprocess the data set
def preprocess_data(df):
    # Group the expenses by date and category and sum the amounts
    grouped_df = df.groupby(["Date", "Category"])["Amount"].sum(numeric_only=True).reset_index()

    # Add a new column with the month of each expense
    grouped_df["Month"] = pd.to_datetime(grouped_df["Date"]).dt.to_period("M")

    # Compute the total amount of expenses by category and by month
    total_by_category_and_month = pd.pivot_table(grouped_df, values="Amount", index="Month", columns="Category", aggfunc=np.sum)

    # Compute the total amount of expenses by category
    total_by_category = grouped_df.groupby("Category")["Amount"].sum().reset_index()

    # Compute the total amount of expenses by month and by category
    total_by_month_and_category = pd.pivot_table(grouped_df, values="Amount", index="Category", columns="Month", aggfunc=np.sum)

    # Reshape the data using the melt function to create a flat list of values
    melted_data = total_by_month_and_category.reset_index().melt(id_vars=["Category"], var_name="Month", value_name="Amount")

    # Convert the 'Month' column to a string representation of the month
    melted_data["Month"] = melted_data["Month"].dt.strftime("%b %Y")

    return grouped_df, total_by_category, melted_data

# Define a function to create the Plotly bar plots
def create_plots(grouped_df, total_by_category, melted_data):
    # Create a dictionary to map each category to a color
    category_colors = {
        "Food": "orange",
        "Travel": "blue",
        "Entertainment": "green",
        "Shopping": "purple",
        "Health": "red",
        "Housing": "gray",
        "Transportation": "brown"
    }

    # Create an interactive bar plot of the expenses
    fig1 = px.bar(grouped_df, x="Date", y="Amount", color="Category",
                 title="Daily Expenses by Category", text="Amount",
                 color_discrete_map=category_colors)

    # Create an interactive bar plot of the monthly expenses by category
    fig2 = px.bar(total_by_category, x="Category", y="Amount",
                  title="Monthly Expenses by Category",
                  text="Amount", color="Category",
                  color_discrete_map=category_colors)

    # Create an interactive bar plot of the monthly expenses by month
    fig3 = px.bar(melted_data, x="Month", y="Amount", color="Category",
                  title="Monthly Expenses by Month and Category",
                  text="Amount", color_discrete_map=category_colors)

    return fig1, fig2, fig3

# Define the main function for the Streamlit app
def main():
    # Set the page title and heading
    st.set_page_config(page_title="Expense Dashboard", page_icon=":dollar:", layout="wide")
    st.title("Expense Dashboard")

    # Import the data set and preprocess the data
    df = import_data()
    grouped_df, total_by_category, melted_data = preprocess_data(df)

    # Create the Plotly bar plots
    fig1, fig2, fig3 = create_plots(grouped_df, total_by_category, melted_data)

    # Add the Plotly bar plots to the app
    st.plotly_chart(fig1, use_container_width=True)
    st.plotly_chart(fig2, use_container_width=True)
    st.plotly_chart(fig3, use_container_width=True)

# Call the main function to run the Streamlit app
if __name__ == '__main__':
    main()