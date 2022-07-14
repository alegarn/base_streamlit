import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

df = pd.read_csv(r'data/combined_final_last_10_years.csv')

print(df)

# the icon: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(
    page_title="Dashboard: Inequalities in the World 2006 - 20XX ",
    page_icon=":bar_chart:",
    layout="wide"
)

st.dataframe(df)

st.sidebar.header("Below the filters:")
year = st.sidebar.multiselect(
    "Year:",
    options=df["year"].unique(),
    default=df["year"].unique()
)

country = st.sidebar.multiselect(
    "Country:",
    options=df["country"].unique(),
    default=df["country"].unique()
)

df_selection = df.query(
    "year == @year & country == @country"
    )

st.markdown("---")

st.title(":bar_chart: Gini index")


gini_per_continent = df.groupby(by=['continent']).mean()
list_con = list(gini_per_continent.mean().index)

fig_index_continent = px.bar(
gini_per_continent,
x='gini_index',
y = gini_per_continent.index,
orientation="h",
title = "<b>2006 Gini index per continent</b>",
color_discrete_sequence=["#000000"] * len(gini_per_continent),
template="plotly_white"
)

st.plotly_chart(fig_index_continent)
