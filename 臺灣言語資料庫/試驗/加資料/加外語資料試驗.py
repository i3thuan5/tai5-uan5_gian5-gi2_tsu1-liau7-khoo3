# -*- coding: utf-8 -*-
from 臺灣言語資料庫.試驗.加資料.加資料試驗 import 加資料試驗
from 臺灣言語資料庫.資料模型 import 外語表
from django.core.exceptions import ObjectDoesNotExist

class 加外語資料試驗(加資料試驗):
	def setUp(self):
		super(加外語資料試驗, self).setUp()
		self.資料表 = 外語表
		self.詞內容.update({
			'外語語言':'華語',
			'外語資料':'漂亮',
		})
		self.句內容.update({
			'外語語言':'英語',
			'外語資料':'She is beautiful.',
		})
	def test_加詞(self):
		super(加外語資料試驗, self).test_加詞()
		self.assertEqual(self.資料.外語語言, self.華語)
		self.assertEqual(self.資料.外語資料, '漂亮')
	def test_加句(self):
		super(加外語資料試驗, self).test_加句()
		self.assertEqual(self.資料.外語語言, self.英語)
		self.assertEqual(self.資料.外語資料, 'She is beautiful.')
	def test_外語語言舊編號(self):
		self.詞內容['外語語言'] = self.華語.pk
		super(加外語資料試驗, self).test_加詞()
		self.assertEqual(self.資料.外語語言, self.華語)
		self.assertEqual(self.資料.外語資料, '漂亮')
		self.句內容['外語語言'] = self.英語.pk
		super(加外語資料試驗, self).test_加句()
		self.assertEqual(self.資料.外語語言, self.英語)
		self.assertEqual(self.資料.外語資料, 'She is beautiful.')
	def test_外語語言新字串(self):
		self.詞內容['外語語言'] = '埔里噶哈巫'
		super(加外語資料試驗, self).test_加詞()
		self.assertEqual(self.資料.外語語言.語言腔口, '埔里噶哈巫')
		self.assertEqual(self.資料.外語資料, '漂亮')
		self.句內容['外語語言'] = '日語'
		super(加外語資料試驗, self).test_加句()
		self.assertEqual(self.資料.外語語言.語言腔口, '日語')
		self.assertEqual(self.資料.外語資料, 'She is beautiful.')
	def test_外語語言新編號(self):
		self.詞內容['外語語言'] = 1115
		self.assertRaises(ObjectDoesNotExist, super(加外語資料試驗, self).test_加詞)
		self.句內容['外語語言'] = 1231
		self.assertRaises(ObjectDoesNotExist, super(加外語資料試驗, self).test_加句)
	def test_外語語言毋是數字佮字串(self):
		self.詞內容['外語語言'] = [1115]
		self.assertRaises(TypeError, super(加外語資料試驗, self).test_加詞)
		self.句內容['外語語言'] = 1231.23
		self.assertRaises(TypeError, super(加外語資料試驗, self).test_加句)
	def test_無語言(self):
		self.詞內容.pop('外語語言')
		self.assertRaises(KeyError, super(加外語資料試驗, self).test_加詞)
		self.句內容.pop('外語語言')
		self.assertRaises(KeyError, super(加外語資料試驗, self).test_加句)
	def test_無資料(self):
		self.詞內容.pop('外語資料')
		self.assertRaises(KeyError, super(加外語資料試驗, self).test_加詞)
		self.句內容.pop('外語資料')
		self.assertRaises(KeyError, super(加外語資料試驗, self).test_加句)
	def test_毋是字串(self):
		self.詞內容['外語資料'] = 1228
		self.assertRaises(TypeError, super(加外語資料試驗, self).test_加詞)
		self.句內容['外語資料'] = ['沒辦法']
		self.assertRaises(TypeError, super(加外語資料試驗, self).test_加句)
		self.詞內容['外語資料'] = None
		self.assertRaises(TypeError, super(加外語資料試驗, self).test_加詞)
		self.句內容['外語資料'] = {}
		self.assertRaises(TypeError, super(加外語資料試驗, self).test_加句)
