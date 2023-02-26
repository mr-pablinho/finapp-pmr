import plotly.express as px
import pandas as pd

# Import the data set from the file dummy_data.xlsx
df = pd.read_excel("../data/dummy_data.xlsx")

# Create an interactive scatter plot of the expenses
fig = px.scatter(df, x="Date", y="Amount", color="Category", hover_data=["Item Description"])

# Add a title to the plot
fig.update_layout(title_text="Daily Expenses")

# Display the plot
fig.show()
