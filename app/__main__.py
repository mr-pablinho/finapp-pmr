import pandas as pd
import numpy as np
import plotly.express as px

# Import the data set from the file dummy_data.xlsx
df = pd.read_excel("../data/dummy_data.xlsx")

# Group the expenses by date and category and sum the amounts
grouped_df = df.groupby(["Date", "Category"])["Amount"].sum(numeric_only=True).reset_index()

# Add a new column with the month of each expense
grouped_df["Month"] = pd.to_datetime(grouped_df["Date"]).dt.to_period("M")

# Compute the total amount of expenses by category and by month
total_by_category_and_month = pd.pivot_table(grouped_df, values="Amount", index="Month", columns="Category", aggfunc=np.sum)

# Compute the mean and standard deviation of monthly expenses by category
mean_by_category = total_by_category_and_month.mean()
std_by_category = total_by_category_and_month.std()

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

# Compute the total amount of expenses by category
total_by_category = grouped_df.groupby("Category")["Amount"].sum().reset_index()

# Create an interactive bar plot of the monthly expenses
fig2 = px.bar(total_by_category, x="Category", y="Amount",
              title="Monthly Expenses by Category",
              text="Amount", color="Category",
              color_discrete_map=category_colors)

# Display the plots
fig1.show()
fig2.show()
