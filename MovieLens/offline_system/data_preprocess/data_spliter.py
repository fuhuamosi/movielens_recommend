# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from random import shuffle

from MovieLens.models import Rating

__author__ = 'fuhuamosi'


class DataSpliter:
    # 将评分数据shuffle后平分为x份训练集和测试集
    @staticmethod
    def split_ratings(x=5):
        scale = 1.0 / x
        src_data = list(Rating.objects.all())
        shuffle(src_data)
        size = len(src_data)
        for i in range(x):
            train_set = []
            test_set = []
            left = int(i * scale * size)
            right = int((i + 1) * scale * size)
            train_set.extend(src_data[:left])
            train_set.extend(src_data[right:])
            test_set.extend(src_data[left:right])
            yield train_set, test_set


if __name__ == '__main__':
    pass
