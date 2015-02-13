# -*- coding: utf-8 -*-
from 臺灣言語資料庫.試驗.加資料.加資料試驗 import 加資料試驗
from 臺灣言語資料庫.資料模型 import 外語表

class 加外語資料試驗(加資料試驗):
	def setUp(self):
		super(加外語資料試驗, self).setUp()
		self.資料表=外語表
		self.詞內容.update({
			'外語語言':'華語',
			'外語資料':'漂亮'
		})
		self.句內容.update({
			'外語語言':'英語',
			'外語資料':'She is beautiful.'
		})
	def test_加詞(self):
		super(加外語資料試驗, self).test_加詞()
		self.assertEqual(self.資料.外語語言,self.華語)
		self.assertEqual(self.資料.外語資料,'漂亮')
	def test_加句(self):
		super(加外語資料試驗, self).test_加句()
		self.assertEqual(self.資料.外語語言,self.英語)
		self.assertEqual(self.資料.外語資料,'She is beautiful.')
