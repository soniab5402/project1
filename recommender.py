from database.Database import movies, similarity
import os
import urllib.parse


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
IMAGES_DIR = os.path.join(PROJECT_ROOT, "static", "images")

EXTERNAL_POSTER_LINKS = {
    "interstellar": "https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg",
    "tenet": "https://image.tmdb.org/t/p/w500/k68nPLbIST6NP96JmTxmZijEvCA.jpg",
    "thor": "https://image.tmdb.org/t/p/w500/prSfAi1xGrhLQNxVSUFh61xQ4Qy.jpg",
    "hulk": "https://image.tmdb.org/t/p/w500/ogcqkq1x9oQWlQn4YxqXv2Fne5P.jpg",
    "iron man": "https://image.tmdb.org/t/p/w500/78lPtwv72eTNqFW9COBYI0dWDJa.jpg",

    "chhichhore": "https://image.tmdb.org/t/p/w500/7sUCRdjGe7VggDCGIHywfguYdAK.jpg",
    "veer-zaara": "https://image.tmdb.org/t/p/w500/8r0h0G9r3YyqSCDtnznuaCG2lKT.jpg",
    "yeh jawaani hai deewani": "https://image.tmdb.org/t/p/w500/4Q0y1R5b0s0rY2XkGLumZ5qX6Ch.jpg",
    "avengers": "https://image.tmdb.org/t/p/w500/RYMX2wcKCBAr24UyPD7xwmjaTn.jpg",

    "kabir singh": "https://image.tmdb.org/t/p/w500/z4A8Xv8P6Z8GDZsBo2yrG9q4CPH.jpg",
    "dilwale dulhania le jayenge": "https://image.tmdb.org/t/p/w500/2CAL2433ZeIihfX1Hb2139CX0pW.jpg",
    "tamasha": "https://image.tmdb.org/t/p/w500/1oZ2Q2qF0pP4fZxwW7X3L9q6X9P.jpg",
    "kuch kuch hota hai": "https://image.tmdb.org/t/p/w500/1GJvbe9iF7a3Zy7u8C3R5yqZz0F.jpg",

    "ta ra rum pum": "https://image.tmdb.org/t/p/w500/6fYl7Zz3r5z0k2K0n7F5p0ZqQ0X.jpg",
    "phir hera pheri": "https://image.tmdb.org/t/p/w500/9r7Jb8n7v0d0u3f0vZ0y3r0p0Q0.jpg",
    "bhool bhulaiyaa": "https://image.tmdb.org/t/p/w500/4rC7o9k3s9F0n0p0W0z0Z0y0q0X.jpg",
    "golmaal": "https://image.tmdb.org/t/p/w500/5z0Z0Z0Z0Z0Z0Z0Z0Z0Z0Z0Z0Z.jpg",

    "welcome": "https://image.tmdb.org/t/p/w500/7q7Z0Z0Z0Z0Z0Z0Z0Z0Z0Z0Z0Z.jpg",
    "housefull": "https://image.tmdb.org/t/p/w500/8Z0Z0Z0Z0Z0Z0Z0Z0Z0Z0Z0Z0Z.jpg",
    "rrr": "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
    "baahubali": "https://image.tmdb.org/t/p/w500/9BAjt8nSSms62uOVYn1t3C3dVto.jpg",
    "kgf": "https://image.tmdb.org/t/p/w500/ltHlJwvxKv7d0ooCiKSAvfwV9tX.jpg",
    "pushpa": "https://image.tmdb.org/t/p/w500/1TPBund2U8FX2SGgYQcNkF5cJ3Z.jpg",
    "jawan":"https://image.tmdb.org/t/p/w500/4lVBH9lQ4GfK8q0n9fZ4P7GdGkU.jpg",
    "dangal": "https://image.tmdb.org/t/p/w500/p2lVAcPuRPSO8Al6hDDGw0OgMi3.jpg",
    "3 idiots": "https://image.tmdb.org/t/p/w500/66A9MqXOyVFCssoloscw79z8Tew.jpg",
    "armitage": "https://image.tmdb.org/t/p/w500/7sUCRdjGe7VggDCGIHywfguYdAK.jpg",
    "war": "https://image.tmdb.org/t/p/w500/8Y43POKjjKDGI9MH89NW0NAzzp8.jpg"
}

GENRE_MAP = {
    "rrr": "Action",
    "baahubali": "Action",
    "kgf": "Action",
    "pathaan": "Action",
    "jawan": "Action",
    "pushpa": "Action",
    "war": "Action",
    "avengers": "Superhero",
    "iron man": "Superhero",
    "thor": "Superhero",
    "hulk": "Superhero",
    "inception": "Sci-Fi",
    "interstellar": "Sci-Fi",
    "tenet": "Sci-Fi",
    "dangal": "Drama",
    "3 idiots": "Comedy",
    "chhichhore": "Drama",
    "mohabbatein": "Romance",
    "kuch kuch hota hai": "Romance",
    "veer-zaara": "Romance",
    "yeh jawaani hai deewani": "Romance",
    "dilwale dulhania le jayenge": "Romance",
    "kabir singh": "Romance",
    "tamasha": "Drama",
    "ta ra rum pum": "Romance",
    "phir hera pheri": "Comedy",
    "bhool bhulaiyaa": "Horror Comedy",
    "golmaal": "Comedy",
    "welcome": "Comedy",
    "housefull": "Comedy"
}

def get_genre(title):
    return GENRE_MAP.get(title.strip().lower(), "Other")

def get_unique_genres():
    genres = set()
    for movie in movies:
        for g in movie["genre"]:
            for sub_g in g.split(","):
                genres.add(sub_g.strip())
    return sorted(list(genres))

def recommend_by_genre(genre):
    default_poster = "https://via.placeholder.com/400x600?text=No+Image"
    if not genre:
        return ["No genre selected"], [default_poster], ["Please select a genre to get recommendations."]

    rec_movies = []
    for movie in movies:
        for g in movie["genre"]:
            if genre.lower() in g.lower():
                rec_movies.append(movie)
                break

    # Sort by rating descending
    rec_movies.sort(key=lambda x: x["rating"], reverse=True)
    # Return all, not limited to 5

    names = [m["title"] for m in rec_movies]
    posters = ["/static/images/" + m["poster"] for m in rec_movies]
    descriptions = [m["description"] for m in rec_movies]

    return names, posters, descriptions


def recommend(movie):
    default_poster = "https://via.placeholder.com/400x600?text=No+Image"

    if not movie:
        return ["No movie entered"], [default_poster], ["Please enter a movie title to get recommendations."]

    movie = movie.strip().lower()

    for key in similarity:
        if movie == key.lower():
            rec_movies = similarity[key]

            names = []
            posters = []
            descriptions = []

            for m in rec_movies:
                for item in movies:
                    if item["title"].lower() == m.lower():
                        names.append(item["title"])
                        poster_file = item.get("poster", "")

                        poster_url = None
                        if poster_file:
                            candidate_path = os.path.join(IMAGES_DIR, poster_file)
                            if os.path.exists(candidate_path):
                                poster_url = f"/images/{poster_file}"
                            else:
                                base, ext = os.path.splitext(poster_file)
                                extensions = [".jpg", ".jpeg", ".png"]
                                # If extension already exists, try alternatives
                                if ext.lower() in extensions:
                                    for e in extensions:
                                        candidate_path = os.path.join(IMAGES_DIR, base + e)
                                        print(f"Checking {candidate_path}: {os.path.exists(candidate_path)}")
                                        if os.path.exists(candidate_path):
                                            poster_url = f"/images/{base + e}"
                                            break
                                else:
                                    for e in extensions:
                                        candidate_path = os.path.join(IMAGES_DIR, poster_file + e)
                                        print(f"Checking {candidate_path}: {os.path.exists(candidate_path)}")
                                        if os.path.exists(candidate_path):
                                            poster_url = f"/images/{poster_file + e}"
                                            break

                        if poster_url:
                            posters.append(poster_url)
                        else:
                            # Manual external link fallback for known titles
                            title_lower = item.get("title", "").lower()
                            if title_lower in EXTERNAL_POSTER_LINKS:
                                posters.append(EXTERNAL_POSTER_LINKS[title_lower])
                            else:
                                title_text = urllib.parse.quote(item.get("title", "No+Image"))
                                posters.append(f"https://via.placeholder.com/400x600?text={title_text}")

                        descriptions.append(item.get("description", "No description available."))

            return names, posters, descriptions

    return ["No match found 😢"], [default_poster], ["Try another movie name."]