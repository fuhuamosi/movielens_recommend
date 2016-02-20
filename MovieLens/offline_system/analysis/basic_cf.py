# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from MovieLens.offline_system.data_preprocess.data_spliter import DataSpliter
from MovieLens.offline_system.analysis.common import Common
from MovieLens.offline_system.analysis.evaluation import Evaluation

__author__ = 'fuhuamosi'


# 基础推荐算法
class BasicCF:
    def __init__(self, n, x=5):
        self.train_set = []
        self.test_set = []
        self.train_users = set()
        self.movie_score = {}
        self.x = x
        self.n = n

    def popular_recommend(self):
        for train, test in DataSpliter.split_ratings(self.x):
            self.train_set = train
            self.test_set = test
            self.train_users = Common.get_users(self.train_set)
            movie_times_dict = Common.get_movie_times_dict(self.train_set)
            rating_dict = Common.get_rating_dict(self.train_set)
            self.movie_score = {}
            for user in self.train_users:
                previous_movies = rating_dict[user].keys()
                new_movies = movie_times_dict.keys() - previous_movies
                new_movies_times = {}
                for new_movie in new_movies:
                    new_movies_times[new_movie] = movie_times_dict[new_movie]
                self.movie_score[user] = sorted(new_movies_times.items(),
                                                key=lambda a: a[1],
                                                reverse=True)
                self.movie_score[user] = self.movie_score[user][:self.n]
            yield self.movie_score

    def cal_evaluation(self, recommend=popular_recommend):
        precisions = np.array([])
        recalls = np.array([])
        coverages = np.array([])
        popularities = np.array([])
        for recommendation_list in recommend(self):
            eva = Evaluation(self.train_set, self.test_set, recommendation_list)
            precision, recall = eva.cal_precision_and_recall()
            precisions = np.append(precisions, precision)
            recalls = np.append(recalls, recall)
            coverages = np.append(coverages, eva.cal_coverage())
            popularities = np.append(popularities, eva.cal_popularity())
        print('Precisions:', precisions.mean(), precisions)
        print('Recalls:', recalls.mean(), recalls)
        print('Coverages:', coverages.mean(), coverages)
        print('Popularities:', popularities.mean(), popularities)


if __name__ == '__main__':
    basic_cf = BasicCF(n=20)
    basic_cf.cal_evaluation()
