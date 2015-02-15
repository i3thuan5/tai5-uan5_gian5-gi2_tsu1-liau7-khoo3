# -*- coding: utf-8 -*-
from 臺灣言語資料庫.試驗.加資料.加資料試驗 import 加資料試驗
from 臺灣言語資料庫.資料模型 import 聽拍表

class 加聽拍資料試驗(加資料試驗):
	def setUp(self):
		super(加聽拍資料試驗, self).setUp()
		self.資料表=聽拍表
		self.詞內容.update({
			'規範':'華語',
			'聽拍資料':'漂亮'
		})
		self.句內容.update({
			'規範':'英語',
			'聽拍資料':'She is beautiful.'
		})
	def test_加詞(self):
		super(加聽拍資料試驗, self).test_加詞()
		self.assertEqual(self.資料.規範,)
		self.assertEqual(self.資料.聽拍資料,'漂亮')
	def test_加句(self):
		super(加聽拍資料試驗, self).test_加句()
		self.assertEqual(self.資料.規範,)
		self.assertEqual(self.資料.聽拍資料,'She is beautiful.')
	def test_規範用字串(self):
		self.句內容['規範']='中研院聽拍資料庫'
		self.assertRaise(ObjectDoesNotExist,self.資料表.加一筆,self.句內容)
	def test_規範新編號(self):
		self.句內容['規範']=109
		self.assertRaise(ObjectDoesNotExist,self.資料表.加一筆,self.句內容)
	def test_無資料(self):
		self.詞內容.pop('聽拍資料')
		self.assertRaise(KeyError,super(加聽拍資料試驗, self).test_加詞)
		self.句內容.pop('聽拍資料')
		self.assertRaise(KeyError,super(加聽拍資料試驗, self).test_加句)
