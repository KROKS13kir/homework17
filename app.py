# app.py

from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy

from models import *
from schemas import *

#настройка конфигурации
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['RESTX_JSON'] = {'ensure_ascii': False, 'indent': 3}
db = SQLAlchemy(app)

#неймспейсы
api = Api(app)
movie_ns = api.namespace("movies")
directors_ns = api.namespace("directors")
genres_ns = api.namespace("genres")


#api для фильмов
@movie_ns.route('/')
class MoviesView(Resource):
    # получааем данные (реализован поиск по director_id, genre_id)
    def get(self):
        movies_with_genre_director = db.session.query(Movie.id, Movie.title, Movie.description, Movie.rating,
                                                      Movie.trailer,
                                                      Genre.name.label("genre"),
                                                      Director.name.label("director")).join(Movie.genre).join(Movie.director)
        director_id = request.args.get("director_id")
        genre_id = request.args.get("genre_id")
        if director_id:
            movies_with_genre_director = movies_with_genre_director.filter(Movie.director_id == director_id)
        if genre_id:
            movies_with_genre_director = movies_with_genre_director.filter(Movie.genre_id == genre_id)
        movies_list = movies_with_genre_director.all()
        return movie_schema.dump(movies_list), 200

    # добавляем в базу
    def post(self):
        req_json = request.json
        new_movie = Movie(**req_json)
        with db.session.begin():
            db.session.add(new_movie)
        return f"Новый объект с id {new_movie.id} добавлен", 201

#api для фильма
@movie_ns.route('/<int:movie_id>')
class MovieView(Resource):
    # поиск по id
    def get(self, movie_id: int):
        one_movie = db.session.query(Movie.id, Movie.title, Movie.description, Movie.rating,
                                     Movie.trailer,
                                     Genre.name.label('genre'),
                                     Director.name.label('director')).join(Movie.genre).join(Movie.director).filter(
            Movie.id == movie_id).first()
        if one_movie:
            return movie_schema.dump(one_movie), 200
        return f"Нет фильма с {movie_id}", 404

    # частичное изменение данных
    def patch(self, movie_id: int):
        one_movie = db.session.query(Movie.id, Movie.title, Movie.description, Movie.rating,
                                     Movie.trailer,
                                     Genre.name.label('genre'),
                                     Director.name.label('director')).join(Movie.genre).join(Movie.director).filter(
            Movie.id == movie_id).first()
        if not movie:
            return "Нет такого фильма", 404
        req_json = request.json
        if 'title' in req_json:
            movie.title = req_json["title"]
        elif 'description' in req_json:
            movie.description = req_json["description"]
        elif 'trailer' in req_json:
            movie.trailer = req_json["trailer"]
        elif 'year' in req_json:
            movie.year = req_json["year"]
        elif 'rating' in req_json:
            movie.rating = req_json["rating"]
        elif 'genre_id' in req_json:
            movie.genre_id = req_json["genre_id"]
        elif 'director_id' in req_json:
            movie.director_id = req_json["director_id"]
        db.session.add(one_movie)
        db.session.commit()
        return f"Объект с {movie.id} обновлен", 204

    # полное изменение
    def put(self, movie_id: int):
        movie = db.session.query(Movie).get(movie_id)
        if not movie:
            return "Нет такого фильма", 404
        req_json = request.json
        movie.title = req_json.get("title")
        movie.description = req_json.get("description")
        movie.trailer = req_json.get("trailer")
        movie.year = req_json.get("year")
        movie.rating = req_json.get("rating")
        movie.genre_id = req_json.get("genre_id")
        movie.director_id = req_json.get("director_id")
        db.session.add(movie)
        db.session.commit()
        return "Данные изменены", 204

    # удаление данных по id
    def delete(self, movie_id: int):
        movie = db.session.query(Movie).get(movie_id)
        if not movie:
            return "Нет такого фильма", 404
        db.session.delete(movie)
        db.session.commit()
        return f"Фильм с {movie_id} удален", 204

#api для режиссера
@directors_ns.route('/directors/<int:id>')
class DirectorView(Resource):
    # получение по id
    def get(self, id: int):
        try:
            book = Director.query.get(id)
            return director_schema.dump(book), 200
        except Exception as e:
            return "", 404

    # изменение данных
    def put(self, id: int):
        director = db.session.query(Director).get(id)
        if not director:
            return "Нет такого режиссера", 404
        req_json = request.json
        director.name = req_json.get("name")
        db.session.add(director)
        db.session.commit()
        return "Данные изменены", 204

    # частичное изменение
    def patch(self, id: int):
        director = db.session.query(Director).get(id)
        if not director:
            return "Нет такого режиссера", 404
        req_json = request.json
        if "name" in req_json:
            director.name = req_json.get("name")
        db.session.add(director)
        db.session.commit()
        return "Данные изменены", 204

    # удаление по id
    def delete(self, id: int):
        director = db.session.query(Director).get(id)
        if not director:
            return "Нет такого режиссера", 404
        db.session.delete(director)
        db.session.commit()
        return f"Режиссер с {id} удален", 204

#api для жанров
@genres_ns.route('/genres/<int:id>')
class GenresView(Resource):
    # получение по id
    def get(self, id: int):
        try:
            genre = Genre.query.get(id)
            return genre_schema.dump(genre), 200
        except Exception as e:
            return "", 404

    # изменение данных
    def put(self, id: int):
        genre = db.session.query(Genre).get(id)
        if not genre:
            return "Нет такого жанра", 404
        req_json = request.json
        genre.name = req_json.get("name")
        db.session.add(genre)
        db.session.commit()
        return "Данные изменены", 204

    # частичное изменение
    def patch(self, id: int):
        genre = db.session.query(Genre).get(id)
        if not genre:
            return "Нет такого жанра", 404
        req_json = request.json
        if "name" in req_json:
            genre.name = req_json.get("name")
        db.session.add(genre)
        db.session.commit()
        return "Данные изменены", 204

    # удаление по id
    def delete(self, id: int):
        genre = db.session.query(Genre).get(id)
        if not genre:
            return "Нет такого жанра", 404
        db.session.delete(genre)
        db.session.commit()
        return f"Жанр с {id} удален", 204


if __name__ == '__main__':
    app.run(debug=True)
