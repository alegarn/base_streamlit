import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
import plotly.figure_factory as ff

# the icon: https://www.webfx.com/tools/emoji-cheat-sheet/
# The layout config
st.set_page_config(
    page_title="Dashboard: Inequalities in the World 2006 - 2016",
    page_icon=":bar_chart:",
    layout="wide"
)




#all datas
@st.experimental_memo
def csv_data():
    df = pd.read_csv(r'./data/combined_final_last_10_years.csv')
    return df

df = csv_data()

@st.experimental_memo
def df_gini_per_continent():
    gini_per_continent = df.groupby(by=['continent']).mean()
    return gini_per_continent

gini_per_continent = df_gini_per_continent()

list_con = list(gini_per_continent.mean().index)


@st.experimental_memo
def df_income_per_continent():
    #.groupby("continent", group_keys = True).
    income_per_continent = df[['continent', 'year', 'income_per_person']]
    return income_per_continent

income_per_continent = df_income_per_continent()
list_con = list(gini_per_continent.groupby("continent").mean().index)



st.dataframe(df)

# widgets sidebar
st.sidebar.header("Below the filters:")

country = st.sidebar.multiselect(
    "Country:",
    options=df["country"].unique(),
    default=df["country"].unique()
)

df_selection = df.query(
    "country == @country"
    )





st.markdown("---")

st.title(":bar_chart: Continent's datas")
# the 2 columns, influence the filters
left_column, right_column = st.columns(2)







# a slider, plotly way (seems not to work with normal streamlit chart)
# https://fcpython.com/data-analysis/building-interactive-analysis-tools-with-python-streamlit
select_year_right = right_column.slider("Date", 2006, 2016, 2016)
income_per_continent = income_per_continent[income_per_continent['year'] == select_year_right]



# chart 1, simple chart
fig_index_continent = px.bar(
    gini_per_continent,
    x='gini_index',
    y = gini_per_continent.index,
    orientation="h",
    title = "<b>Mean Gini index per continent (2006 - 2016)</b>",
    color_discrete_sequence=["#000000"] * len(gini_per_continent),
    template="plotly_white"
)




# https://docs.streamlit.io/library/api-reference/charts/st.plotly_chart
fig = px.bar(income_per_continent.groupby("continent").median(), x=list_con, y='income_per_person', title ="<b>Yearly income per person</b>")

# graphical elements
left_column.plotly_chart(fig_index_continent, use_container_width = True)
left_column.write("Basic bar chart, just a dataframe with no filters. :thumbsup:")

right_column.plotly_chart(fig, use_container_width = True)
right_column.write("Let's add a filter to this vertical bar chart! :scream:")

st.markdown("---")

st.title(":bar_chart: Yearly income per person, country and continents.")


# https://plotly.com/python/categorical-axes/
# make the chart filtered by df_selection
graph = px.scatter(df_selection, y="country", x="income_per_person", color="year", symbol="continent")
graph.update_traces(marker_size=10)
st.plotly_chart(graph, use_container_width=True)

st.write(":arrow_left: It's possible to choose the country with the sidebar filter. :muscle:")
