/# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from 整理華語臺語雙語語料庫系統.整合平行語料 import 來整合平行語料

urlpatterns = patterns('',
	url(r'^來整合平行語料$', 來整合平行語料, name='來整合平行語料'),
)