# -*- coding: utf-8 -*-
from django.test import TestCase
import json
from 臺灣言語資料庫.資料模型 import 語言腔口表
from 臺灣言語資料庫.資料模型 import 著作所在地表
from django.core.exceptions import ObjectDoesNotExist
from 臺灣言語資料庫.資料模型 import 來源表
from 臺灣言語資料庫.資料模型 import 來源屬性表

class 加來源試驗(TestCase):
	def setUp(self):
		pass
	def tearDown(self):
		pass
	def test_試驗屬性內容(self):
		self.鄉民 = 來源表.objects.create(名='鄉民')
		出世年一九五空 = 來源屬性表.objects.create(分類='出世年', 性質=json.dumps('1950'))
		出世地臺灣 = 來源屬性表.objects.create(分類='出世地', 性質=json.dumps('臺灣'))
		self.鄉民.屬性.add(出世年一九五空, 出世地臺灣)
		self.Pigu = 來源表.objects.create(名='Dr. Pigu')
		self.Pigu.屬性.add(
			來源屬性表.objects.create(分類='出世年', 性質=json.dumps('1990')),
			來源屬性表.objects.create(分類='出世地', 性質=json.dumps('花蓮人')),
			)
		self.assertEqual()