# -*- coding: utf-8 -*-
from django.db import models
import json
	
class 來源表(models.Model):
	名 = models.CharField(max_length=100)
	屬性 = models.TextField()  # 出世年、出世地、…

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
	class Meta:
		abstract = True
	收錄者 = models.ForeignKey(來源表, related_name='+')
	收錄時間 = models.DateTimeField(auto_now_add=True)
	來源 = models.ForeignKey(來源表, related_name='+')
	版權 = models.ForeignKey(版權表, related_name='+')
	種類 = models.ForeignKey(種類表, related_name='+')
	語言腔口 = models.ForeignKey(語言腔口表, related_name='+')
	著作所在地 = models.ForeignKey(著作所在地表, related_name='+')
	著作年 = models.ForeignKey(著作年表, related_name='+')
	屬性 = models.TextField()  # 冊名,詞性,分類,…
	def 編號(self):
		return self.pk
	def _加基本內容(self, 內容):
		if isinstance(內容['收錄者'],int):
			self.收錄者 = 內容['收錄者']
		else:
			raise 來源表.DoesNotExist('收錄者愛是編號')
		if isinstance(內容['來源'],int):#######
			self.來源 = 內容['來源']
		else:
			名=內容['來源'].pop('名')
			self.來源=來源表.object.get(名=名,屬性=內容['來源']['屬性'])
		if isinstance(內容['版權'],int):
			self.版權 = 內容['版權']
		else:
			self.版權=版權表.object.get(版權=內容['版權'])
		if isinstance(內容['種類'],int):
			self.種類 = 內容['種類']
		else:
			self.種類=種類表.object.get(種類=內容['種類'])
		if isinstance(內容['語言腔口'],int):
			self.語言腔口 = 內容['語言腔口']
		else:
			self.語言腔口=語言腔口表.object.get_or_create(語言腔口 = 內容['語言腔口'])[0]
		if isinstance(內容['著作所在地'],int):
			self.著作所在地 = 內容['著作所在地']
		else:
			self.著作所在地=著作所在地表.object.get_or_create(著作所在地 = 內容['著作所在地'])[0]
		if isinstance(內容['著作年'],int):
			self.著作年 = 內容['著作年']
		else:
			self.著作年=著作年表.object.get_or_create(著作年 = 內容['著作年'])[0]
		json.loads(內容['屬性'])
		self.屬性 = 內容['屬性']

class 資料類型表(models.Model):
# 	外語、文本、影音、聽拍
	類型 = models.CharField(max_length=20)

class 外語表(資料表):
	外語語言 = models.ForeignKey(語言腔口表, related_name='+')
	外語資料 = models.TextField()
	def __str__(self):
		return self.外語資料
	@classmethod
	def 加一筆(self, 內容):
		外語 = self()
		外語._加基本內容(內容)
		外語.外語語言 = 內容['外語語言']
		外語.外語資料 = 內容['外語資料']
		return 外語.save()

class 文本表(資料表):
	文本資料 = models.TextField()
	def __str__(self):
		return self.文本資料
	@classmethod
	def 加一筆(self, 內容):
		文本 = self()
		文本._加基本內容(內容)
		文本.文本資料 = 內容['文本資料']
		return 文本.save()

class 影音表(資料表):
	原始影音資料 = models.FileField()
	網頁影音資料 = models.FileField()
	def __str__(self):
		return str(self.原始資料)
	@classmethod
	def 加一筆(self, 內容):
		影音 = self()
		影音._加基本內容(內容)
		影音.原始影音資料 = 內容['原始影音資料']
# 		影音.網頁影音資料 = 
		return 影音.save()

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
	@classmethod
	def 加一筆(self, 內容):
		聽拍 = self()
		聽拍._加基本內容(內容)
		聽拍.規範 = 內容['規範']
		聽拍資料內容=json.loads(內容['聽拍資料'])
		for 一句 in 聽拍資料內容:
			if '內容' not in 一句:
				raise ValueError('逐句聽拍資料攏愛有「內容」欄位')
		聽拍.聽拍資料 = 內容['聽拍資料']
		return 聽拍.save()
