# -*- coding: utf-8 -*-
from django.db import models
	
class 來源表(models.Model):
	名 = models.CharField(max_length=100)
	屬性 = models.TextField() #出世年、出世地、…

class 版權表(models.Model):
# 	會使公開，袂使公開
	版權 = models.CharField(max_length=20)

class 種類表(models.Model):
# 	字詞 = '字詞'
# 	語句 = '語句'
	種類 = models.CharField(max_length=100)

class 語言腔口表(models.Model):
# 	閩南語、閩南語永靖腔、客話四縣腔、泰雅seediq…
	語言腔口 = models.CharField(max_length=50)

class 著作所在地表(models.Model):
# 	臺灣、員林、…
	著作所在地 = models.CharField(max_length=50)

class 著作年表(models.Model):
# 	1952、19xx、…
	著作年 = models.CharField(max_length=20)

class 資料表(models.Model):
	收錄者 = models.ForeignKey(來源表, related_name='收的資料')
	收錄時間 = models.DateTimeField(auto_now_add=True)
	來源 = models.ForeignKey(來源表, related_name='做的資料')
	版權 = models.ForeignKey(版權表, related_name='+')
	種類 = models.ForeignKey(種類表, related_name='全部資料')
	語言腔口 = models.ForeignKey(語言腔口表, related_name='全部資料')
	著作所在地 = models.ForeignKey(著作所在地表, related_name='全部資料')
	著作年 = models.ForeignKey(著作年表, related_name='全部資料')
	屬性 = models.TextField() #冊名,詞性,分類,…
	def 編號(self):
		return self.pk
	class Meta:
		abstract = True

class 資料類型表(models.Model):
# 	外語、文本、影音、聽拍
	類型 = models.CharField(max_length=20)

class 外語表(資料表):
	外語語言 = models.ForeignKey(語言腔口表, related_name='+')
	外語資料 = models.TextField()
	def __str__(self):
		return self.外語資料

class 文本表(資料表):
	文本資料 = models.TextField()
	def __str__(self):
		return self.文本資料

class 影音表(資料表):
	原始影音資料 = models.FileField()
	網頁影音資料 = models.FileField()
	def __str__(self):
		return str(self.原始資料)

class 聽拍規範表(models.Model):
	規範名 = models.CharField(max_length=20, unique=True)
	範例 = models.TextField()
	說明 = models.TextField()

class 聽拍表(資料表):
# 	語者詳細資料記佇屬性內底，逐句話記是佗一个語者
	規範 = models.ForeignKey(聽拍規範表, related_name='全部資料')
	聽拍資料 = models.TextField()
	def __str__(self):
		return self.聽拍資料
