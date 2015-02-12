# -*- coding: utf-8 -*-
from django.test import TestCase
from 臺灣言語資料庫.資料模型 import 版權表
from 臺灣言語資料庫.資料模型 import 種類表
from 臺灣言語資料庫.資料模型 import 來源表
from 臺灣言語資料庫.資料模型 import 語言腔口表
from 臺灣言語資料庫.試驗.資料庫試驗 import 資料庫試驗
import json
from 臺灣言語資料庫.資料模型 import 外語表

class 加外語資料試驗(資料庫試驗):
	def test_外語詞(self):
		原來外語資料數=外語表.objects.all().count()
		屬性=json.dumps({'詞性':'形容詞'})
		外語內容={
			'收錄者':self.臺灣人.pk,
			'來源':self.花蓮人.pk,
			'版權':self.會使公開,
			'種類':self.字詞,
			'語言腔口':self.閩南語,
			'語料所在地':self.花蓮.pk,
			'著作時間':'2014',
			'屬性':屬性,
			'外語語言':self.華語,
			'外語資料':'漂亮'}
		外語表.加一筆(外語內容)
		self.assertEqual(外語表.objects.all().count(),原來外語資料數+1)
		外語=外語表.上新的資料()#objects.order('-pk')
		self.assertEqual(外語.收錄者,self.臺灣人.pk)
		self.assertEqual(外語.來源,self.花蓮人.pk)
		self.assertEqual(外語.版權,self.會使公開.pk)
		self.assertEqual(外語.種類,self.字詞.pk)
		self.assertEqual(外語.語言腔口,self.閩南語.pk)
		self.assertEqual(外語.語料所在地,self.花蓮.pk)
		self.assertEqual(外語.著作時間,'2014')
		self.assertEqual(外語.屬性,屬性)
		self.assertEqual(外語.外語語言,屬性)
		self.assertEqual(外語.外語資料,漂亮)
		
		
	def test_無來源(self):
		pass
	def test_來源編號揣無(self):
		pass
	def test_來源分名佮屬性_資料庫有(self):
		外語內容={
			'收錄者':self.臺灣人,
			'來源名':,
			'來源屬性':,
			'版權':,
			'種類':,
			'語言腔口':,
			'語料所在地':,
			'著作時間':,
			'屬性':,
			'外語語言':,
			'外語資料':}
		
	def test_來源分名佮屬性_資料庫無(self):
		pass