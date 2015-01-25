# -*- coding: utf-8 -*-
from django.db import models
from 臺灣言語資料庫.欄位資訊 import 文字種類

class 資料(models.Model):
	作者 = models.CharField(max_length = 100)
	腔口 = models.CharField(max_length = 100)
	地區 = models.CharField(max_length = 100)
	年代 = models.IntegerField()#char ?
	收錄時間 = models.DateTimeField(auto_now_add = True)
	class Meta:
		abstract = True

class 文本(資料):
	文本資料 = models.TextField()
	種類 = models.CharField(max_length = 10, choices = 文字種類)
	def __str__(self):
		return self.文本資料

class 影音(資料):
	原始資料=models.FileField()
	網頁資料=models.FileField()
	def __str__(self):
		return str(self.原始資料)

class 聽拍(資料):
	聽拍資料=models.TextField()
	def __str__(self):
		return self.聽拍資料
