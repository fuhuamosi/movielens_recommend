# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import django

__author__ = 'fuhuamosi'

# 设置os环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'MovieRecommend.settings')

django.setup()
