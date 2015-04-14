# -*- coding: utf-8 -*-
from django.test import TestCase
from 臺灣言語資料庫.試驗.加資料.加資料試驗 import 加資料試驗
from 臺灣言語資料庫.資料模型 import 文本表
from django.core.exceptions import ValidationError


class 加文本資料試驗(TestCase, 加資料試驗):
	def setUp(self):
		self.加初始資料()
		self.資料表 = 文本表
		self.詞內容.update({
			'文本資料':'媠',
		})
		self.句內容.update({
			'文本資料':'伊誠媠。',
		})
	def test_加詞(self):
		super(加文本資料試驗, self).test_加詞()
		self.assertEqual(self.資料.文本資料, '媠')
	def test_加句(self):
		super(加文本資料試驗, self).test_加句()
		self.assertEqual(self.資料.文本資料, '伊誠媠。')
	def test_無資料(self):
		self.詞內容.pop('文本資料')
		self.assertRaises(KeyError, super(加文本資料試驗, self).test_加詞)
		self.assertEqual(self.資料表.objects.all().count(), 0)
		self.句內容.pop('文本資料')
		self.assertRaises(KeyError, super(加文本資料試驗, self).test_加句)
		self.assertEqual(self.資料表.objects.all().count(), 0)
	def test_資料毋是字串(self):
		self.句內容['文本資料'] = 2005
		self.assertRaises(TypeError, self.資料表.加資料, self.句內容)
		self.assertEqual(self.資料表.objects.all().count(), 0)
		self.句內容['文本資料'] = None
		self.assertRaises(TypeError, self.資料表.加資料, self.句內容)
		self.assertEqual(self.資料表.objects.all().count(), 0)
		self.句內容['文本資料'] = [' 南投縣噶哈巫文教協會', '眉溪四庄重建工作站']
		self.assertRaises(TypeError, self.資料表.加資料, self.句內容)
		self.assertEqual(self.資料表.objects.all().count(), 0)
	def test_資料是空的(self):
		self.句內容['文本資料'] = ''
		self.assertRaises(ValidationError, self.資料表.加資料, self.句內容)
		self.assertEqual(self.資料表.objects.all().count(), 0)
