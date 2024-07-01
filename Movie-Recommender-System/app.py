# reuired libraries
import streamlit as st
import pickle
import pandas as pd
import requests

# Function to fetch the poster of a movie using its movie_id
def fetch_poster(movie_id):
    # Sending a GET request to the TMDB API to get movie details using the movie_id
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=beb7c191ca41d0ce192d60cda6513af2&language=en-US'.format(movie_id))
    data = response.json()
    # Extracting the image path for the movie poster
    image_path = "https://image.tmdb.org/t/p/w500/"+data['poster_path']
    return image_path

# Function to recommend movies based on a given movie
def recommend(movie):
    # Finding the index of the given movie in the movies DataFrame
    movie_index = movies[movies['title']==movie].index[0]
    # Retrieving the similarity scores for the given movie
    distances = similarity[movie_index]
    # Sorting the movies based on similarity scores in descending order and selecting the top 5
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]

    # Lists to store recommended movies and their posters
    recommended_movies = []
    recommended_posters = []
    
    # Looping through the top 5 recommended movies
    for i in movies_list:
        # Getting the movie_id of the recommended movie
        id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster of movie from API
        recommended_posters.append(fetch_poster(id))

    return (recommended_movies, recommended_posters)

# Loading the movies dictionary from a pickle file
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Loading the similarity matrix from a pickle file
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Setting the title of the Streamlit app
st.title('Movie Recommender System')

# Creating a selectbox for users to select a movie from the list of movie titles
selected_movie_name = st.selectbox('How would you like to be contacted?', movies['title'].values)

# Adding a button for recommending movies
if st.button('Recommend'):
    movies, posters = recommend(selected_movie_name)
    # Creating 5 columns in Streamlit to display the recommended movies and their posters
    col1, col2, col3, col4, col5 = st.columns(5)

    # Displaying the recommended movies and their poster
    with col1:
        st.text(movies[0])
        st.image(posters[0])

    with col2:
        st.text(movies[1])
        st.image(posters[1])

    with col3:
        st.text(movies[2])
        st.image(posters[2])

    with col4:
        st.text(movies[3])
        st.image(posters[3])

    with col5:
        st.text(movies[4])
        st.image(posters[4])


