from flask import Flask,request,render_template,jsonify
import pickle
import requests
import pandas as pd
from patsy import dmatrices

movies = pickle.load(open('artifacts/movie_list.pkl','rb'))
similarity = pickle.load(open('artifacts/similarity.pkl','rb'))

app = Flask(__name__)
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=df4c10d3269e8fa8b94ffacda1d6609b"
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/"+poster_path
    return full_path
def recommend(movie):
    l1 = []
    movies_poster = []
    index = movies[movies['title']==movie].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key=lambda x:x[1])
    for i in distances[1:6]:
        l1.append(movies.iloc[i[0]].title)
        movie_id = movies.iloc[i[0]].movie_id
        movies_poster.append(fetch_poster(movie_id))
        
    return l1,movies_poster


@app.route('/')
def movie_form():
    return render_template('index1.html', movies=movies['title'].values)


@app.route('/recommend', methods=['POST'])
def movie_recommendations():
    selected_movie = request.form.get('movieSelect')

    # Perform movie recommendation logic here based on the selected movie
    # Update the 'recommended_movies' list with the recommendations
    result = recommend(selected_movie)
    recommended_movies =result[0]
    posters = result[1]
    
    print(recommended_movies[1])

    return render_template('recommend.html', movies=movies['title'].values, recommended_movies=result)

if __name__ == '__main__':
    app.run(debug=True) 

# df4c10d3269e8fa8b94ffacda1d6609b
# https://api.themoviedb.org/3/movie/19995?api_key=df4c10d3269e8fa8b94ffacda1d6609b

# https://image.tmdb.org/t/p/w500//kyeqWdyUXW608qlYkRqosgbbJyK.jpg

# https://image.tmdb.org/t/p/w500//385XwTQZDpRX2d3kxtnpiLrjBXw.jpg