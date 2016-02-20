# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv

__author__ = 'fuhuamosi'


def file2list(filename, encode_type='utf-8'):
    with open(filename, mode='r', encoding=encode_type) as csv_file:
        reader = csv.reader(csv_file)
        data_list = []
        for line in reader:
            data_list.append(line)
    return data_list[1:]
