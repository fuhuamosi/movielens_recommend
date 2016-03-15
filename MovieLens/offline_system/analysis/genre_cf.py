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
    def __init__(self, n=20, x=5, z=5, alpha=0.01, beta=1.0):
        self.n = n
        self.x = x
        self.z = z
        self.alpha = alpha
        self.beta = beta
        self.all_users = Common.get_all_users()
        self.all_movies = Common.get_all_movies()
        self.all_genres = [g[0] for g in Common.get_all_genres_cnt()]
        self.train_set = []
        self.test_set = []
        self.movie_score = {}
        self.um = None
        self.mg = None
        self.ug = None
        self.movie_times_genres = {}

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
                # self.mg[movie_sub, genre_sub] = 1.0

    def set_movie_times_genres(self):
        self.movie_times_genres = {}
        movie_times_dict = Common.get_movie_times_dict(self.train_set)
        for m, t in movie_times_dict.items():
            self.movie_times_genres[m] = (t, get_genres_by_id(m))

    @staticmethod
    def cal_cos(set1, set2):
        inter_set = set1 & set2
        return len(inter_set) / math.sqrt(len(set1) * len(set2))

    def recommend(self):
        for train, test in DataSpliter.split_ratings(self.x):
            self.train_set = train
            self.test_set = test
            self.movie_score = {}
            favor_genres = self.get_user_favor_genres()
            user_movie_dict = Common.get_user_movie_dict(self.train_set)
            for user in self.all_users:
                old_movies = user_movie_dict[user]
                user_favor_genres = set()
                for fg in favor_genres[user - 1]:
                    genre = self.all_genres[fg]
                    user_favor_genres.add(genre)
                for movie, times_and_genres in self.movie_times_genres.items():
                    if movie not in old_movies:
                        times = times_and_genres[0]
                        genres = times_and_genres[1]
                        genre_sim = self.cal_cos(user_favor_genres, genres)
                        self.movie_score.setdefault(user, {})
                        self.movie_score[user][movie] = self.alpha * times
                        self.movie_score[user][movie] += self.beta * genre_sim
                self.movie_score[user] = sorted(self.movie_score[user].items(),
                                                key=lambda r: r[1], reverse=True)
                self.movie_score[user] = self.movie_score[user][:self.n]
                if user < 5:
                    print(user, self.movie_score[user][:5])
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

    def get_user_favor_genres(self):
        self.set_movie_times_genres()
        self.init_matrix()
        self.ug = np.dot(self.um, self.mg)
        favor_genres = self.ug.argsort()[:, -1:-(self.z + 1):-1]
        return favor_genres

    def set_train(self, train):
        self.train_set = train


if __name__ == '__main__':
    genre_cf = GenreCF(n=20, z=5, alpha=0.015, beta=1.0)
    genre_cf.cal_evaluation()
