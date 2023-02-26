import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

class ExpenseDashboard:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        self.grouped_df = None
        self.total_by_category = None
        self.melted_data = None
        self.category_colors = {
            "Food": "orange",
            "Travel": "blue",
            "Entertainment": "green",
            "Shopping": "purple",
            "Health": "red",
            "Housing": "gray",
            "Transportation": "brown"
        }

    def import_data(self):
        self.df = pd.read_excel(self.file_path)

    def preprocess_data(self):
        self.grouped_df = self.df.groupby(["Date", "Category"])["Amount"].sum(numeric_only=True).reset_index()

        self.grouped_df["Month"] = pd.to_datetime(self.grouped_df["Date"]).dt.to_period("M")

        total_by_category_and_month = pd.pivot_table(self.grouped_df, values="Amount", index="Month", columns="Category", aggfunc=np.sum)

        self.total_by_category = self.grouped_df.groupby("Category")["Amount"].sum().reset_index()

        total_by_month_and_category = pd.pivot_table(self.grouped_df, values="Amount", index="Category", columns="Month", aggfunc=np.sum)

        self.melted_data = total_by_month_and_category.reset_index().melt(id_vars=["Category"], var_name="Month", value_name="Amount")

        self.melted_data["Month"] = self.melted_data["Month"].dt.strftime("%b %Y")

    def create_daily_expenses_plot(self):
        fig = px.bar(self.grouped_df, x="Date", y="Amount", color="Category",
                     title="Daily Expenses by Category", text="Amount",
                     color_discrete_map=self.category_colors)
        return fig

    def create_monthly_expenses_by_category_plot(self):
        fig = px.bar(self.total_by_category, x="Category", y="Amount",
                      title="Monthly Expenses by Category",
                      text="Amount", color="Category",
                      color_discrete_map=self.category_colors)
        return fig

    def create_monthly_expenses_by_month_and_category_plot(self):
        fig = px.bar(self.melted_data, x="Month", y="Amount", color="Category",
                      title="Monthly Expenses by Month and Category",
                      text="Amount", color_discrete_map=self.category_colors)
        return fig

    def run(self):
        self.import_data()
        self.preprocess_data()

        daily_expenses_fig = self.create_daily_expenses_plot()
        monthly_expenses_by_category_fig = self.create_monthly_expenses_by_category_plot()
        monthly_expenses_by_month_and_category_fig = self.create_monthly_expenses_by_month_and_category_plot()

        st.set_page_config(page_title="Expense Dashboard", page_icon=":dollar:")
        st.title("Expense Dashboard")
        st.plotly_chart(daily_expenses_fig, use_container_width=True)
        st.plotly_chart(monthly_expenses_by_category_fig, use_container_width=True)
        st.plotly_chart(monthly_expenses_by_month_and_category_fig, use_container_width=True)

if __name__ == "__main__":
    dashboard = ExpenseDashboard("../data/dummy_data.xlsx")
    dashboard.run()