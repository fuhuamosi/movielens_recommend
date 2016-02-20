# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from MovieLens.models import Tag

__author__ = 'fuhuamosi'


def add_tag(user_id: int, movie_id: int, movie_tag: str, timestamp: int):
    tag = Tag.objects.create(user_id=user_id, movie_id=movie_id)
    tag.movie_tag = movie_tag
    tag.timestamp = timestamp
    tag.save()
