import pandas as pd
import plotly.express as px

dataFolder = r"Money management\Scraper\Outputs"
df = pd.read_csv("Money management\Scraper\Outputs\output_data.csv")

fig = px.bar(df, x="date", y="debit")
fig.show()