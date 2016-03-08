# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import math
import numpy as np
from MovieLens.offline_system.data_preprocess.data_spliter import DataSpliter
from MovieLens.offline_system.analysis.common import Common
from MovieLens.offline_system.analysis.evaluation import Evaluation
from MovieLens.offline_system.dao.movie_dao import get_genres_by_id

__author__ = 'fuhuamosi'


# 基于电影风格的协同过滤算法
class GenreCF:
    def __init__(self, n, x=5):
        self.n = n
        self.x = x
        self.all_users = Common.get_all_users()
        self.all_movies = Common.get_all_movies()
        self.all_genres = [g[0] for g in Common.get_all_genres_cnt()]
        self.train_set = []
        self.test_set = []
        self.um = None
        self.mg = None

    @Common.exe_time
    def init_matrix(self):
        user_cnt = len(self.all_users)
        movie_cnt = len(self.all_movies)
        genre_cnt = len(self.all_genres)
        self.um = np.array([[0.0] * movie_cnt] * user_cnt)
        self.mg = np.array([[0.0] * genre_cnt] * movie_cnt)
        for rating in self.train_set:
            user_sub = rating.user_id - 1
            movie_sub = self.all_movies.index(rating.movie_id)
            movie_genres = get_genres_by_id(rating.movie_id)
            self.um[user_sub, movie_sub] = rating.movie_rating
            for g in movie_genres:
                genre_sub = self.all_genres.index(g)
                self.mg[movie_sub, genre_sub] = 1.0

    def recommend(self):
        for train, test in DataSpliter.split_ratings(self.x):
            self.train_set = train
            self.test_set = test
            self.init_matrix()
            ug = np.dot(self.um, self.mg)
            print(ug.argsort()[:10, -1:-6:-1])


if __name__ == '__main__':
    genre_cf = GenreCF(n=20)
    genre_cf.recommend()
