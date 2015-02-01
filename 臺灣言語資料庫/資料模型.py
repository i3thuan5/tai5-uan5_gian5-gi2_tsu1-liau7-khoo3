# -*- coding: utf-8 -*-
from django.db import models
from 臺灣言語資料庫.欄位資訊 import 文字種類

class 款(models.Model):
# 	字詞 = '字詞'
# 	語句 = '語句'
	種類 = models.CharField(max_length=100)

class 作者(models.Model):
	作者名 = models.CharField(max_length=100)
	出世年= models.CharField(max_length=10)
	出世地 = models.CharField(max_length=100)

class 權(models.Model):
# 	會使公開，袂使公開
	版權 = models.CharField(max_length=20)
	
class 資料(models.Model):
	款 = models.ForeignKey(款, related_name='全部資料')
	收錄者 = models.ForeignKey(作者, related_name='收的資料')
	收錄時間 = models.DateTimeField(auto_now_add=True)
	作者 = models.ForeignKey(作者, related_name='做的資料')
	腔口 = models.CharField(max_length=100)
	地區 = models.CharField(max_length=100)
	年代 = models.CharField(max_length=10)
	權 = models.ForeignKey(權, related_name='+')
	屬性 = models.TextField() #冊名,詞性,分類,…
	class Meta:
		abstract = True

class 文本(資料):
	文本資料 = models.TextField()
	def __str__(self):
		return self.文本資料

class 影音(資料):
	原始資料 = models.FileField()
	網頁資料 = models.FileField()
	def __str__(self):
		return str(self.原始資料)

class 聽拍(資料):
	聽拍資料 = models.TextField()
	def __str__(self):
		return self.聽拍資料
