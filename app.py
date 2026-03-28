import os
from datetime import timedelta
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from recommender import recommend_by_genre, get_genre, get_unique_genres

app = Flask(__name__)
app.secret_key = "secret123"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

@app.route('/')
def login_page():
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    if email == "soniabhattacharjee06@gmail.com" and password == "123":
        session.permanent = True
        session["user"] = "Sonia Bhattacharjee"
        return redirect(url_for("index_page"))
    else:
        return render_template("login.html", error="Invalid Login 😢")

@app.route('/signup_page')
def signup_page():
    return render_template("signup.html")

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    session.permanent = True
    session["user"] = username
    return redirect(url_for("index_page"))

@app.route('/index')
def index_page():
    if "user" not in session:
        return redirect(url_for("login_page"))
    genres = get_unique_genres()
    return render_template("index.html", user=session["user"], genres=genres)

@app.route('/recommend', methods=['POST'])
def get_recommendation():
    if "user" not in session:
        return redirect(url_for("login_page"))

    genre = request.form.get('genre')

    names, posters, descriptions = recommend_by_genre(genre)
    recommendations = []
    for name, poster, description in zip(names, posters, descriptions):
        recommendations.append({
            "title": name,
            "poster": poster,
            "description": description,
            "genre": genre  # since all are from this genre
        })

    grouped_recommendations = {genre: recommendations}

    genres = get_unique_genres()
    return render_template("result.html", grouped_recommendations=grouped_recommendations, genres=genres)

@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for("login_page"))

@app.route('/images/<path:filename>')
def serve_image(filename):
    image_dir = os.path.join(app.root_path, 'static', 'images')
    print('Serving image from', image_dir, 'file', filename)
    return send_from_directory(image_dir, filename)

if __name__ == "__main__":
    app.run(debug=True)