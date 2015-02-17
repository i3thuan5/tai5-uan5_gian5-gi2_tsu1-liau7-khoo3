# -*- coding: utf-8 -*-
from 臺灣言語資料庫.試驗.資料庫試驗 import 資料庫試驗

class 加關係試驗(資料庫試驗):
	def setUp(self):
		super(加關係試驗, self).setUp()
	def test_加詞(self):
		原本資料 = self.原本資料表.加一筆(self.原本資料內容一)
		self.加詞(原本資料)
	def test_加句(self):
		原本資料 = self.原本資料表.加一筆(self.原本資料內容二)
		self.加句(原本資料)
	def test_濟个正常語料(self):
		原本資料詞 = self.原本資料表.加一筆(self.原本資料內容一)
		self.加詞(原本資料詞)
		原本資料句 = self.原本資料表.加一筆(self.原本資料內容二)
		self.加句(原本資料句)
		self.加句(原本資料句)
		self.加詞(原本資料詞)
		self.加詞(原本資料詞)
		self.加句(原本資料句)
		原本資料句 = self.原本資料表.加一筆(self.原本資料內容二)
		self.加句(原本資料句)
	def test_無仝種類(self):
		原本資料詞 = self.原本資料表.加一筆(self.原本資料內容一)
		原本資料句 = self.原本資料表.加一筆(self.原本資料內容二)
		self.影音內容一['種類'] = '語句'
		self.影音內容二['種類'] = '字詞'
		self.assertRaise(ValueError, self.加詞, 原本資料詞)
		self.assertRaise(ValueError, self.加句, 原本資料句)
	def test_無種類(self):
		原本資料詞 = self.原本資料表.加一筆(self.原本資料內容一)
		原本資料句 = self.原本資料表.加一筆(self.原本資料內容二)
		self.影音內容一.pop('種類')
		self.影音內容二.pop('種類')
		self.assertRaise(KeyError, self.加詞, 原本資料詞)
		self.assertRaise(KeyError, self.加句, 原本資料句)
	def test_無仝語言腔口(self):
		原本資料詞 = self.原本資料表.加一筆(self.原本資料內容一)
		原本資料句 = self.原本資料表.加一筆(self.原本資料內容二)
		self.影音內容一['語言腔口'] = '泰雅話'
		self.影音內容二['語言腔口'] = '泰雅話'
		self.assertRaise(ValueError, self.加詞, 原本資料詞)
		self.assertRaise(ValueError, self.加句, 原本資料句)
	def test_無語言腔口(self):
		原本資料詞 = self.原本資料表.加一筆(self.原本資料內容一)
		原本資料句 = self.原本資料表.加一筆(self.原本資料內容二)
		self.影音內容一.pop('語言腔口')
		self.影音內容二.pop('語言腔口')
		self.assertRaise(KeyError, self.加詞, 原本資料詞)
		self.assertRaise(KeyError, self.加句, 原本資料句)
	def test_無仝種類佮語言腔品(self):
		原本資料詞 = self.原本資料表.加一筆(self.原本資料內容一)
		原本資料句 = self.原本資料表.加一筆(self.原本資料內容二)
		self.assertRaise(ValueError, self.加詞, 原本資料句)
		self.assertRaise(ValueError, self.加句, 原本資料詞)
