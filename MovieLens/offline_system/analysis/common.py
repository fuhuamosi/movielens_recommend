# !/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'fuhuamosi'


# 提供一些该模块的常用函数
class Common:
    @staticmethod
    def get_rating_dict(ratings: list):
        rating_dict = {}
        for r in ratings:
            rating_dict.setdefault(r.user_id, {}).setdefault(r.movie_id, r.movie_rating)
        return rating_dict

    @staticmethod
    def get_users(ratings: list):
        users = set()
        for rating in ratings:
            users.add(rating.user_id)
        return users

    @staticmethod
    def get_user_movie_dict(ratings: list):
        user_movie_dict = {}
        for r in ratings:
            user_movie_dict.setdefault(r.user_id, set()).add(r.movie_id)
        return user_movie_dict

    @staticmethod
    def get_movie_times_dict(ratings: list):
        movie_times_dict = {}
        for r in ratings:
            movie_times_dict.setdefault(r.movie_id, 0)
            movie_times_dict[r.movie_id] += 1
        return movie_times_dict
