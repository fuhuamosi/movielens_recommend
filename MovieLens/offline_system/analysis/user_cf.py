# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import numpy as np
from MovieLens.offline_system.data_preprocess.data_spliter import DataSpliter
from MovieLens.offline_system.analysis.common import Common
from MovieLens.offline_system.analysis.evaluation import Evaluation
from MovieLens.offline_system.analysis.distance import Distance

__author__ = 'fuhuamosi'


# 基于用户的协同过滤算法
class UserCf:
    def __init__(self, k, n, x=5, dis_type='cos'):
        self.k = k
        self.n = n
        self.x = x
        self.train_set = []
        self.test_set = []
        self.train_users = set()
        self.movie_score = {}
        self.dis_type = dis_type

    def user_similarity(self):
        invert_dict = self.get_invert_dict()
        sim_mat = {}
        for u1 in self.train_users:
            sim_mat[u1] = {}
            for u2 in self.train_users:
                sim_mat[u1][u2] = 0.0
        if self.dis_type == 'cos':
            um_dict = dict().fromkeys(self.train_users, 0.0)
            sim_mat = Distance.cal_cos(sim_mat, um_dict, invert_dict)
        elif self.dis_type == 'jaccard':
            um_dict = {}
            for u in self.train_users:
                um_dict[u] = set()
            sim_mat = Distance.cal_jaccard(sim_mat, um_dict, invert_dict)
        elif self.dis_type == 'cos_advance':
            user_amount = len(Common.get_all_users())
            um_dict = dict().fromkeys(self.train_users, 0.0)
            sim_mat = Distance.cal_cos_advance(sim_mat, um_dict,
                                               invert_dict, amount=user_amount)
        return sim_mat

    # 获得电影-用户倒排表
    def get_invert_dict(self):
        invert_dict = {}
        for rating in self.train_set:
            invert_dict.setdefault(rating.movie_id, set()).add(rating.user_id)
        return invert_dict

    # 从k个最近用户中挑出n部电影来推荐,进行x次验证
    def recommend(self):
        for train, test in DataSpliter.split_ratings(self.x):
            self.train_set = train
            self.test_set = test
            self.train_users = Common.get_users(self.train_set)
            sim_mat = self.user_similarity()
            for u in self.train_users:
                sim_mat[u] = sorted(sim_mat[u].items(),
                                    key=lambda a: a[1], reverse=True)
                sim_mat[u] = sim_mat[u][:self.k]
            rating_dict = Common.get_rating_dict(self.train_set)
            self.movie_score = {}
            for user in self.train_users:
                for v in sim_mat[user]:
                    sim_user = v[0]
                    similarity = v[1]
                    for movie in rating_dict[sim_user].keys():
                        if movie not in rating_dict[user].keys():
                            movie_rank = self.movie_score.setdefault(user, {})
                            movie_rank.setdefault(movie, 0.0)
                            movie_rank[movie] += similarity * rating_dict[sim_user][movie]
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
            precisions = np.append(precisions, precision)
            recalls = np.append(recalls, recall)
            coverages = np.append(coverages, eva.cal_coverage())
            popularities = np.append(popularities, eva.cal_popularity())
        print('Precisions:', precisions.mean(), precisions)
        print('Recalls:', recalls.mean(), recalls)
        print('Coverages:', coverages.mean(), coverages)
        print('Popularities:', popularities.mean(), popularities)


if __name__ == '__main__':
    user_cf = UserCf(k=30, n=20, dis_type='cos_advance')
    user_cf.cal_evaluation()
