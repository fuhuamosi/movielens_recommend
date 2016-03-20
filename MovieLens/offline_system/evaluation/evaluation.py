# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from MovieLens.offline_system.common.common import Common
import math

__author__ = 'fuhuamosi'


# 统计准确率,召回率,覆盖率以及流行度
class Evaluation:
    def __init__(self, train, test, recommend_list):
        self.train_set = train
        self.test_set = test
        self.recommend_list = recommend_list
        self.user_count = len(Common.get_all_users())
        self.movie_count = len(Common.get_all_movies())

    def cal_precision_and_recall(self):
        hit = 0
        recommend_count = self.user_count * len(self.recommend_list[1])
        test_count = len(self.test_set)
        test_dict = Common.get_user_movie_dict(self.test_set)
        for user in self.recommend_list.keys():
            if user not in test_dict:
                continue
            for movie, score in self.recommend_list[user]:
                test_user_movies = test_dict[user]
                if movie in test_user_movies:
                    hit += 1
        return hit / float(recommend_count), hit / float(test_count)

    def cal_coverage(self):
        recommend_movies = set()
        for user in self.recommend_list.keys():
            for movie, score in self.recommend_list[user]:
                recommend_movies.add(movie)
        return len(recommend_movies) / float(self.movie_count)

    def cal_popularity(self):
        movie_times_dict = Common.get_movie_times_dict(self.train_set)
        popularity = 0.0
        n = 0
        for user in self.recommend_list.keys():
            for movie, score in self.recommend_list[user]:
                popularity += math.log(1 + movie_times_dict[movie])
                n += 1
        return popularity / n
