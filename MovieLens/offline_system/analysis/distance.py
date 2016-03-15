# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import math

__author__ = 'fuhuamosi'


# 计算相似性度量
class Distance:
    @staticmethod
    def cal_cos(sim_mat: dict, um_dict: dict, invert_dict: dict):
        for k, vs in invert_dict.items():
            for v1 in vs:
                um_dict[v1] += 1
                for v2 in vs:
                    if v1 == v2:
                        continue
                    sim_mat[v1][v2] += 1
        for x in sim_mat.keys():
            for y in sim_mat[x].keys():
                if x == y:
                    continue
                sim_mat[x][y] /= math.sqrt(um_dict[x] * um_dict[y])
        return sim_mat

    @staticmethod
    def cal_jaccard(sim_mat: dict, um_dict: dict, invert_dict: dict):
        for k, vs in invert_dict.items():
            for v1 in vs:
                um_dict[v1].add(k)
                for v2 in vs:
                    if v1 == v2:
                        continue
                    sim_mat[v1][v2] += 1
        for x in sim_mat.keys():
            for y in sim_mat[x].keys():
                if x == y:
                    continue
                sim_mat[x][y] /= len(um_dict[x] | um_dict[y])
        return sim_mat

    @staticmethod
    def cal_cos_advance(sim_mat: dict, um_dict, invert_dict, amount):
        for k, vs in invert_dict.items():
            for v1 in vs:
                um_dict[v1] += 1
                for v2 in vs:
                    if v1 == v2:
                        continue
                    sim_mat[v1][v2] += 1 / math.log(1 + len(vs))
        for x in sim_mat.keys():
            for y in sim_mat[x].keys():
                if x == y:
                    continue
                sim_mat[x][y] /= math.sqrt(um_dict[x] * um_dict[y])
        return sim_mat
