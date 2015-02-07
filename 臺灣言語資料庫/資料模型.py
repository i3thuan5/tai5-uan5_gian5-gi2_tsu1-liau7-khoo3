# -*- coding: utf-8 -*-
from django.db import models
from 臺灣言語資料庫.欄位資訊 import 文字種類

class 作者(models.Model):
	作者名 = models.CharField(max_length=100)
	出世年= models.CharField(max_length=10)
	出世地 = models.CharField(max_length=100)

class 權(models.Model):
# 	會使公開，袂使公開
	版權 = models.CharField(max_length=20)

class 款(models.Model):
# 	字詞 = '字詞'
# 	語句 = '語句'
	種類 = models.CharField(max_length=100)

class 話(models.Model):
# 	閩南語、閩南語永靖腔、客話四縣腔、泰雅seediq…
	語言腔口 = models.CharField(max_length=50)

class 所在(models.Model):
# 	臺灣、員林、…
	地區 = models.CharField(max_length=50)

class 語料著作時間(models.Model):
# 	臺灣、員林、…
	年 = models.CharField(max_length=50)

class 資料(models.Model):
	收錄者 = models.ForeignKey(作者, related_name='收的資料')
	收錄時間 = models.DateTimeField(auto_now_add=True)
	作者 = models.ForeignKey(作者, related_name='做的資料')
	權 = models.ForeignKey(權, related_name='+')
	款 = models.ForeignKey(款, related_name='全部資料')
	話 = models.ForeignKey(話, related_name='全部資料')
	所在 = models.ForeignKey(所在, related_name='全部資料')
	著作時間 = models.ForeignKey(語料著作時間, related_name='全部資料')
	屬性 = models.TextField() #冊名,詞性,分類,…
	class Meta:
		abstract = True

class 外語(資料):
	外語資料 = models.TextField()
	def __str__(self):
		return self.外語資料

class 文本(資料):
	文本資料 = models.TextField()
	def __str__(self):
		return self.文本資料

class 影音(資料):
	原始資料 = models.FileField()
	網頁資料 = models.FileField()
	def __str__(self):
		return str(self.原始資料)

class 聽拍規範(models.Model):
	規範名 = models.CharField(max_length=20, unique=True)
	範例 = models.TextField()
	說明 = models.TextField()

class 聽拍(資料):
	聽拍資料 = models.TextField()
	def __str__(self):
		return self.聽拍資料
