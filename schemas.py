from marshmallow import Schema, fields

# добавлены схемы для фильмов, режиссёров, жанров

class MovieSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    director_id = fields.Int()
    genre = fields.Str()
    director = fields.Str()

class GenreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()

class DirectorSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()



movie = GenreSchema()
movie_schema = MovieSchema(many=True)

genre = GenreSchema()
genre_schema = GenreSchema(many=True)

director = DirectorSchema()
director_schema = DirectorSchema(many=True)

