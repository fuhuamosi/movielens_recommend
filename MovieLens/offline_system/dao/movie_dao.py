# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from MovieLens.models import Movie

__author__ = 'fuhuamosi'


def add_movie(movie_id: int, title, genres):
    movie = Movie.objects.get_or_create(movie_id=movie_id)[0]
    movie.title = title
    movie.genres = genres
    movie.save()
