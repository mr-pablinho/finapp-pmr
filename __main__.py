import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
    
        
class Plotting:
    """
    Class for creating plots. 
    """
    
    def __init__(self):
        """
        
        """
        self.category_colors = {
            "Food": "orange",
            "Travel": "blue",
            "Entertainment": "green",
            "Shopping": "purple",
            "Health": "red",
            "Housing": "gray",
            "Transportation": "brown"
        }
        
    def create_daily_expenses_plot(self, grouped_df):
        """
        Method that creates a bar chart of daily expenses by category using the
        Plotly Express library. The method takes a Pandas DataFrame that is
        grouped by date and category as an argument, and returns a Plotly figure
        object.
        
        Args:
        - grouped_df: A Pandas DataFrame that is grouped by date and category,
          and has columns for "Date", "Category", and "Amount".
          
        Returns:
        - fig: A Plotly figure object that contains the daily expenses by category
          bar chart.
        """
        fig = px.bar(grouped_df, x="Date", y="Amount", color="Category",
                     title="Daily Expenses by Category", text="Amount",
                     color_discrete_map=self.category_colors)
        fig.update_layout(font_family="Segoe UI", title_font_family="Segoe UI")
        return fig

    def create_monthly_expenses_by_category_plot(self, total_by_category):
        """
        Method that creates a bar chart of monthly expenses by category using the
        Plotly Express library. The method takes a Pandas DataFrame that has the
        total expenses by category as an argument, and returns a Plotly figure object.
        
        Args:
        - total_by_category: A Pandas DataFrame that has columns for "Category"
          and "Amount", and shows the total expenses for each category.
          
        Returns:
        - fig: A Plotly figure object that contains the monthly expenses by category
          bar chart.
        """
        fig = px.bar(total_by_category, x="Category", y="Amount",
                     title="Monthly Expenses by Category",
                     text="Amount", color="Category",
                     color_discrete_map=self.category_colors)
        fig.update_layout(font_family="Segoe UI", title_font_family="Segoe UI")
        return fig

    def create_monthly_expenses_by_month_and_category_plot(self, melted_data):
        """
        Method that creates a bar chart of monthly expenses by month and category using
        the Plotly Express library. The method takes a Pandas DataFrame that has the
        melted data (i.e. long format) with columns for "Month", "Category", and "Amount"
        as an argument, and returns a Plotly figure object.
        
        Args:
        - melted_data: A Pandas DataFrame that has columns for "Month", "Category",
          and "Amount", and shows the expenses for each category in each month.
          
        Returns:
        - fig: A Plotly figure object that contains the monthly expenses by month
          and category bar chart.
        """
        fig = px.bar(melted_data, x="Month", y="Amount", color="Category",
                     title="Monthly Expenses by Month and Category",
                     text="Amount", color_discrete_map=self.category_colors)
        fig.update_layout(font_family="Segoe UI", title_font_family="Segoe UI")
        return fig


class ExpenseDashboard:
    
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        self.grouped_df = None
        self.total_by_category = None
        self.melted_data = None
        self.plotting = Plotting()
        
    def import_data(self):
        self.df = pd.read_excel(self.file_path)

    def preprocess_data(self):
        self.grouped_df = self.df.groupby(["Date", "Category"])[
            "Amount"].sum(numeric_only=True).reset_index()

        self.grouped_df["Month"] = pd.to_datetime(
            self.grouped_df["Date"]).dt.to_period("M")

        self.total_by_category = self.grouped_df.groupby(
            "Category")["Amount"].sum().reset_index()

        total_by_month_and_category = pd.pivot_table(
            self.grouped_df, values="Amount", index="Category", 
            columns="Month", aggfunc=np.sum)

        self.melted_data = total_by_month_and_category.reset_index().melt(
            id_vars=["Category"], var_name="Month", value_name="Amount")

        self.melted_data["Month"] = self.melted_data["Month"].dt.strftime(
            "%b %Y")
        
    def _define_styles(self):
        streamlit_style = """
			<style>
			@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@100&display=swap');
			html, body, [class*="css"]  {font-family: 'Roboto', sans-serif;}
			</style>
			"""
        st.markdown(streamlit_style, unsafe_allow_html=True)
        
    def run(self):

        self.import_data()
        self.preprocess_data()
        st.set_page_config(page_title="Expense Dashboard",
                           page_icon=":dollar:", layout="wide")
        st.title("Expense Dashboard")
        self._define_styles()
        st.write("This dashboard shows the expenses for the month of January 2021.")
        st.plotly_chart(
            self.plotting.create_daily_expenses_plot(self.grouped_df),
            use_container_width=True)
        st.plotly_chart(
            self.plotting.create_monthly_expenses_by_category_plot(
                self.total_by_category),
            use_container_width=True)
        st.plotly_chart(
            self.plotting.create_monthly_expenses_by_month_and_category_plot(
                self.melted_data),
            use_container_width=True)


if __name__ == "__main__":
    dashboard = ExpenseDashboard("../data/dummy_data.xlsx")
    dashboard.run()