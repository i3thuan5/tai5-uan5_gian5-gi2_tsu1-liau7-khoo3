# -*- coding: utf-8 -*-
from django.db import models
from 臺灣言語資料庫.資料模型 import 外語
from 臺灣言語資料庫.資料模型 import 影音
from 臺灣言語資料庫.資料模型 import 文本
from 臺灣言語資料庫.資料模型 import 聽拍

class 翻譯影音(models.Model):
	外語 = models.ForeignKey(外語, related_name = '+關係甲')
	影音 = models.ForeignKey(影音, related_name = '+關係乙')
	def __str__(self):
		return 'CC'
class 影音文本(models.Model):
	影音 = models.ForeignKey(影音, related_name = '+關係甲')
	文本 = models.ForeignKey(文本, related_name = '+關係乙')
	def __str__(self):
		return 'CC'
class 影音聽拍(models.Model):
	影音 = models.ForeignKey(影音, related_name = '+關係甲')
	聽拍 = models.ForeignKey(聽拍, related_name = '+關係乙')
	def __str__(self):
		return 'CC'
class 文本校對(models.Model):
	舊文本 = models.ForeignKey(文本, related_name = '+關係甲')
	新文本 = models.ForeignKey(文本, related_name = '+關係乙')
	def __str__(self):
		return 'CC'
class 聽拍校對(models.Model):
	舊聽拍 = models.ForeignKey(聽拍, related_name = '+關係甲')
	新聽拍 = models.ForeignKey(聽拍, related_name = '+關係乙')
	def __str__(self):
		return 'CC'
