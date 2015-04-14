# -*- coding: utf-8 -*-
from django.test import TestCase
from 臺灣言語資料庫.資料模型 import 版權表
from 臺灣言語資料庫.資料模型 import 種類表
from 臺灣言語資料庫.資料模型 import 來源屬性表
from 臺灣言語資料庫.資料模型 import 來源表
from 臺灣言語資料庫.資料模型 import 著作所在地表
from 臺灣言語資料庫.資料模型 import 語言腔口表
from 臺灣言語資料庫.欄位資訊 import 會使公開
from 臺灣言語資料庫.欄位資訊 import 袂使公開
from 臺灣言語資料庫.欄位資訊 import 字詞
from 臺灣言語資料庫.欄位資訊 import 語句
from 臺灣言語資料庫.資料模型 import 著作年表
import json

class 資料庫試驗:
	def 加初始資料(self):
		self.會使公開 = 版權表.objects.create(版權=會使公開)
		self.袂使公開 = 版權表.objects.create(版權=袂使公開)
		self.字詞 = 種類表.objects.create(種類=字詞)
		self.語句 = 種類表.objects.create(種類=語句)
		self.臺灣 = 著作所在地表.objects.create(著作所在地='臺灣')
		self.花蓮 = 著作所在地表.objects.create(著作所在地='花蓮')
		self.鄉民 = 來源表.objects.create(名='鄉民')
		出世年一九五空 = 來源屬性表.objects.create(分類='出世年', 性質=json.dumps('1950'))
		出世地臺灣 = 來源屬性表.objects.create(分類='出世地', 性質=json.dumps('臺灣'))
		self.鄉民.屬性.add(出世年一九五空, 出世地臺灣)
		self.Pigu = 來源表.objects.create(名='Dr. Pigu')
		self.Pigu.屬性.add(
			來源屬性表.objects.create(分類='出世年', 性質=json.dumps('1990')),
			來源屬性表.objects.create(分類='出世地', 性質=json.dumps('花蓮人')),
			)
		self.閩南語 = 語言腔口表.objects.create(語言腔口='閩南語')
		self.四縣話 = 語言腔口表.objects.create(語言腔口='四縣話')
		self.噶哈巫 = 語言腔口表.objects.create(語言腔口='噶哈巫')
		self.華語 = 語言腔口表.objects.create(語言腔口='華語')
		self.英語 = 語言腔口表.objects.create(語言腔口='英語')
		self.二空一四 = 著作年表.objects.create(著作年='2014')
		self.一九五空年代 = 著作年表.objects.create(著作年='195x')
