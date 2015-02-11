# -*- coding: utf-8 -*-
from django.test import TestCase
from 臺灣言語資料庫.資料模型 import 版權表
from 臺灣言語資料庫.資料模型 import 種類表
from 臺灣言語資料庫.資料模型 import 作者表
from 臺灣言語資料庫.資料模型 import 語言腔口表

# Create your tests here.
class 資料庫試驗(TestCase):
	def setUp(self):
		self.會使公開 = 版權表.objects.create(版權='會使公開')
		self.袂使公開 = 版權表.objects.create(版權='袂使公開')
		self.字詞 = 種類表.objects.create(種類='字詞')
		self.語句 = 種類表.objects.create(種類='語句')
		self.臺灣人 = 作者表.objects.create(作者名='鄉民',
			出世年='1950', 出世地='臺灣')
		self.花蓮人 = 作者表.objects.create(作者名='Dr. Pigu',
			出世年='1990', 出世地='花蓮人')
		self.閩南語 = 語言腔口表.objects.create(語言腔口='閩南語')
		self.四縣話 = 語言腔口表.objects.create(語言腔口='四縣話')
		self.噶哈巫 = 語言腔口表.objects.create(語言腔口='噶哈巫')
		self.華語 = 語言腔口表.objects.create(語言腔口='華語')

	def tearDown(self):
		pass
