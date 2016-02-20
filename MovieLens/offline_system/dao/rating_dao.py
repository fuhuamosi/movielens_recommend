# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from MovieLens.models import Rating

__author__ = 'fuhuamosi'


def add_rating(user_id: int, movie_id: int, movie_rating: float, timestamp: int):
    rating = Rating.objects.get_or_create(user_id=user_id, movie_id=movie_id)[0]
    rating.movie_rating = movie_rating
    rating.timestamp = timestamp
    rating.save()
