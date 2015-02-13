# -*- coding: utf-8 -*-
from 臺灣言語資料庫.試驗.資料庫試驗 import 資料庫試驗
import json
from 臺灣言語資料庫.資料模型 import 外語表
from 臺灣言語資料庫.欄位資訊 import 字詞
from 臺灣言語資料庫.欄位資訊 import 會使公開
from 臺灣言語資料庫.欄位資訊 import 袂使公開
from 臺灣言語資料庫.欄位資訊 import 語句

class 加外語資料試驗(資料庫試驗):
	def setUp(self):
		super(加外語資料試驗, self).setUp()
		self.外語詞屬性=json.dumps({'詞性':'形容詞'})
		self.外語詞內容={
			'收錄者':json.dumps({'名':'鄉民','出世年':'1950', '出世地':'臺灣'}),
			'來源':json.dumps({'名':'Dr. Pigu','出世年':'1990', '出世地':'花蓮人'}),
			'版權':會使公開,
			'種類':字詞,
			'語言腔口':'閩南語',
			'語料所在地':'花蓮',
			'著作時間':'2014',
			'屬性':self.外語詞屬性,
			'外語語言':'華語',
			'外語資料':'漂亮'}
		self.外語句屬性=json.dumps({'性質':'例句'})
		self.外語句內容={
			'收錄者':json.dumps({'名':'Dr. Pigu','出世年':'1990', '出世地':'花蓮人'}),
			'來源':json.dumps({'名':'鄉民','出世年':'1950', '出世地':'臺灣'}),
			'版權':袂使公開,
			'種類':語句,
			'語言腔口':'四縣話',
			'語料所在地':'臺灣',
			'著作時間':'2015',
			'屬性':self.外語句屬性,
			'外語語言':'英語',
			'外語資料':'She is beautiful.'}
	def test_外語詞(self):
		原來外語資料數=外語表.objects.all().count()
		外語=外語表.加一筆(self.外語詞內容)
		self.assertEqual(外語表.objects.all().count(),原來外語資料數+1)
		self.assertEqual(外語.收錄者,self.臺灣人)
		self.assertEqual(外語.來源,self.花蓮人)
		self.assertEqual(外語.版權,self.會使公開)
		self.assertEqual(外語.種類,self.字詞)
		self.assertEqual(外語.語言腔口,self.閩南語)
		self.assertEqual(外語.語料所在地,self.花蓮)
		self.assertEqual(外語.著作時間.著作時間,'2014')
		self.assertEqual(外語.屬性,self.外語詞屬性)
		self.assertEqual(外語.外語語言,self.華語)
		self.assertEqual(外語.外語資料,'漂亮')
	def test_外語句(self):
		原來外語資料數=外語表.objects.all().count()
		外語=外語表.加一筆(self.外語句內容)
		self.assertEqual(外語表.objects.all().count(),原來外語資料數+1)
		self.assertEqual(外語.收錄者,self.花蓮人)
		self.assertEqual(外語.來源,self.臺灣人)
		self.assertEqual(外語.版權,self.會使公開)
		self.assertEqual(外語.種類,self.語句)
		self.assertEqual(外語.語言腔口,self.四縣話)
		self.assertEqual(外語.語料所在地,self.臺灣)
		self.assertEqual(外語.著作時間.著作時間,'2015')
		self.assertEqual(外語.屬性,self.外語句屬性)
		self.assertEqual(外語.外語語言,self.英語)
		self.assertEqual(外語.外語資料,'She is beautiful.')
	def test_濟个正常語料(self):
		self.test_外語詞()
		self.test_外語句()
		self.test_外語句()
		self.test_外語詞()
		self.test_外語詞()
		self.test_外語句()
		self.test_外語句()
	def test_無來源(self):
		pass
	def test_來源編號揣無(self):
		pass
	def test_來源分名佮屬性_資料庫有(self):
		pass
	def test_來源分名佮屬性_資料庫無(self):
		pass
	def test_濟个綜合語料(self):
		self.test_無來源()
		pass