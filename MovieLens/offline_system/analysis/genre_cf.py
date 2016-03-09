# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import math
import numpy as np
from MovieLens.offline_system.data_preprocess.data_spliter import DataSpliter
from MovieLens.offline_system.analysis.common import Common
from MovieLens.offline_system.analysis.evaluation import Evaluation
from MovieLens.offline_system.dao.movie_dao import get_genres_by_id
from MovieLens.models import Rating
import random

__author__ = 'fuhuamosi'


# 基于电影风格的协同过滤算法
class GenreCF:
    def __init__(self, n, x=5, k=5):
        self.n = n
        self.x = x
        self.k = k
        self.all_users = Common.get_all_users()
        self.all_movies = Common.get_all_movies()
        self.all_genres = [g[0] for g in Common.get_all_genres_cnt()]
        self.train_set = []
        self.test_set = []
        self.movie_score = {}
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
                self.mg[movie_sub, genre_sub] = 1.0 / len(movie_genres)

    # 将每部电影的评分次数按照其最风格分组
    def grouping(self):
        movie_times_dict = Common.get_movie_times_dict(self.train_set)
        group_dict = {}
        for movie, times in movie_times_dict.items():
            movie_genre = get_genres_by_id(movie)
            g = movie_genre[random.randint(0, len(movie_genre) - 1)]
            g_sub = self.all_genres.index(g)
            temp = group_dict.setdefault(g_sub, {})
            temp[movie] = times
        for i in range(len(self.all_genres)):
            if group_dict.get(i) is not None:
                print(i, len(group_dict.get(i)))
        return group_dict

    def recommend(self):
        for train, test in DataSpliter.split_ratings(self.x):
            self.train_set = train
            self.test_set = test
            self.movie_score = {}
            grouping_dict = self.grouping()
            self.init_matrix()
            ug = np.dot(self.um, self.mg)
            favor_genres = ug.argsort()[:, -1:-(self.k + 1):-1]
            user_movie_dict = Common.get_user_movie_dict(self.train_set)
            for user in self.all_users:
                old_movies = user_movie_dict[user]
                user_favor_genre = set(favor_genres[user - 1])
                for g in user_favor_genre:
                    genre_movies = grouping_dict[g].copy()
                    for om in old_movies:
                        if om in genre_movies:
                            genre_movies.pop(om)
                    genre_movies = sorted(genre_movies.items(),
                                          key=lambda x: x[1],
                                          reverse=True)
                    cnt = int(self.n / self.k)
                    for movie, times in genre_movies[:cnt]:
                        movie_rank = self.movie_score.setdefault(user, {})
                        movie_rank[movie] = times
                self.movie_score[user] = sorted(self.movie_score[user].items(),
                                                key=lambda r: r[1], reverse=True)
                self.movie_score[user] = self.movie_score[user][:self.n]
            yield self.movie_score

    @Common.exe_time
    def cal_evaluation(self):
        precisions = np.array([])
        recalls = np.array([])
        coverages = np.array([])
        popularities = np.array([])
        for recommendation_list in self.recommend():
            eva = Evaluation(self.train_set, self.test_set, recommendation_list)
            precision, recall = eva.cal_precision_and_recall()
            coverage = eva.cal_coverage()
            popularity = eva.cal_popularity()
            precisions = np.append(precisions, precision)
            recalls = np.append(recalls, recall)
            coverages = np.append(coverages, coverage)
            popularities = np.append(popularities, popularity)
            print(precision, recall, coverage, popularity)
        print('Precision:', precisions.mean())
        print('Recall:', recalls.mean())
        print('Coverage:', coverages.mean())
        print('Popularity:', popularities.mean())


if __name__ == '__main__':
    genre_cf = GenreCF(n=20, k=5)
    genre_cf.cal_evaluation()
