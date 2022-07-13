from flask import Flask, jsonify
from classes import DbReader

app = Flask(__name__)

@app.route("/movie/<title>")
def page_by_title(title):
    result = DbReader().get_film_by_title(title)
    return jsonify(result)

@app.route("/movie/<int:from_year>/to/<int:to_year>")
def page_from_year_to_year(from_year, to_year):
    result = DbReader().get_films_from_year_to_year(from_year, to_year)
    return jsonify(result)

@app.route("/rating/<rating>")
def page_by_rating(rating):
    result = DbReader().get_films_by_rating(rating)
    return jsonify(result)

@app.route("/genre/<genre>")
def page_by_genre(genre):
    result = DbReader().get_films_by_genre(genre)
    return jsonify(result)

