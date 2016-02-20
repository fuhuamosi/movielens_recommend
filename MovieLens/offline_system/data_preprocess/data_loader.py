# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from MovieLens.offline_system.data_preprocess import file_manager
from MovieLens.offline_system.dao import movie_dao, rating_dao, tag_dao
from MovieLens.models import Movie, Rating, Tag

__author__ = 'fuhuamosi'


def load_movies():
    filename = '../dataset/movies.csv'
    movies = file_manager.file2list(filename)
    if len(Movie.objects.all()) == 0:
        last_id = 0
    else:
        last_id = Movie.objects.order_by('-movie_id')[0].movie_id
    for movie in movies[last_id:]:
        movie_id = int(movie[0])
        title = movie[1].strip('"')
        genres = movie[2]
        movie_dao.add_movie(movie_id, title, genres)


def load_ratings():
    filename = '../dataset/ratings.csv'
    ratings = file_manager.file2list(filename)
    if len(Rating.objects.all()) == 0:
        last_id = 0
    else:
        last_id = Rating.objects.order_by('-id')[0].id
    for rating in ratings[last_id:]:
        user_id = int(rating[0])
        movie_id = int(rating[1])
        movie_rating = float(rating[2])
        timestamp = int(rating[3])
        rating_dao.add_rating(user_id, movie_id, movie_rating, timestamp)


def load_tags():
    filename = '../dataset/tags.csv'
    tags = file_manager.file2list(filename)
    if len(Tag.objects.all()) == 0:
        last_id = 0
    else:
        last_id = Tag.objects.order_by('-id')[0].id
    for tag in tags[last_id:]:
        user_id = int(tag[0])
        movie_id = int(tag[1])
        movie_tag = str(tag[2])
        timestamp = int(tag[3])
        tag_dao.add_tag(user_id, movie_id, movie_tag, timestamp)


if __name__ == '__main__':
    # load_movies()
    # load_ratings()
    # load_tags()
    pass
