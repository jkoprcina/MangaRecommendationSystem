import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from data_manipulation import clean_input_data
from score_calculations import calculate_similarity_score

st.set_page_config(layout="wide")
# Importing data
data = pd.read_csv("data/top500mangaMAL.csv", usecols=[
    "English Title", "Synonims Titles", "Genres", "Score", "Popularity", "Favorites", "Manga URL"])

df = clean_input_data(data)
score_array = []


options = st.multiselect('What manga have you read so far', df.English_Title.sort_values())
st.write('You selected:', options)

col1, col2 = st.columns(2)

with col2:
    for manga in options:
        list_of_potential_recommendations, score_current = calculate_similarity_score(df, manga)
        score_array.append(score_current)

    df = df.assign(score_current=np.divide(np.sum(np.array(score_array), 0), len(score_array)))
    fig = px.scatter_3d(df, x="Score", y="Popularity", z="Favorites", hover_name="English_Title",
                        color="score_current", width=700, height=700)
    st.plotly_chart(fig, use_container_width=False, sharing="streamlit")


with col1:
    if options:
        current_df = df[['English_Title', 'score_current', 'Manga_URL']].copy()
        current_df = current_df.sort_values(by="score_current", ascending=False)
        current_df
