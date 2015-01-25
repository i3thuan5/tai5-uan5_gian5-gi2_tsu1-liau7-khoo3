# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.query import QuerySet
from 臺灣言語資料庫.欄位資訊 import 編修種類
from 臺灣言語資料庫.欄位資訊 import 狀況種類
from 臺灣言語資料庫.欄位資訊 import 猶未檢查
from 臺灣言語資料庫.欄位資訊 import 文字種類
from 臺灣言語資料庫.欄位資訊 import 關係種類
from 臺灣言語資料庫.欄位資訊 import 演化種類
from 臺灣言語資料庫.欄位資訊 import 改過
from 臺灣言語資料庫.欄位資訊 import 關係性質種類
from 臺灣言語資料庫.資料模型 import 語句

class 翻譯語音:
	甲編修 = models.ForeignKey(語句, related_name = '+關係甲')
	乙編修 = models.ForeignKey('編修', related_name = '關係乙')
	def __str__(self):
		return 'CC'
class 語音文本:
	甲編修 = models.ForeignKey(語句, related_name = '+關係甲')
	乙編修 = models.ForeignKey('編修', related_name = '關係乙')
	def __str__(self):
		return 'CC'
class 語音聽拍:
	甲編修 = models.ForeignKey(語句, related_name = '+關係甲')
	乙編修 = models.ForeignKey('編修', related_name = '關係乙')
	def __str__(self):
		return 'CC'
class 文本校對:
	甲編修 = models.ForeignKey(語句, related_name = '+關係甲')
	乙編修 = models.ForeignKey('編修', related_name = '關係乙')
	def __str__(self):
		return 'CC'
class 聽拍校對:
	甲編修 = models.ForeignKey(語句, related_name = '+關係甲')
	乙編修 = models.ForeignKey('編修', related_name = '關係乙')
	def __str__(self):
		return 'CC'
