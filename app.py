import streamlit as st
import pickle
import pandas as pd
import requests

# Define fetch_poster function
def fetch_poster(movie_id):
    response = requests.get(url ='https://api.themoviedb.org/3/movie/{}?api_key=<api_key>&language=en-US'.format(movie_id))
    data = response.json()
    
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']

# Define recommend function
def recommend(movie, movies_df):
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommend_movies = []
    recommend_movies_posters = []
    for i in movies_list:
        movie_id = movies_df.iloc[i[0]].movie_id
        recommend_movies.append(movies_df.iloc[i[0]].title)
        recommend_movies_posters.append(fetch_poster(movie_id))
    return recommend_movies, recommend_movies_posters

# Load movie data and similarity matrix
movie_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit app
st.title('Movie Recommender system')

selected_movie_name = st.selectbox(
    "Movie Name",
    movies['title'].values)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name, movies)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
