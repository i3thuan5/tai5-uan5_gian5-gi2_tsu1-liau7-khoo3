# -*- coding: utf-8 -*-
from 臺灣言語資料庫.試驗.加資料.加資料試驗 import 加資料試驗
from 臺灣言語資料庫.資料模型 import 文本表

class 加文本資料試驗(加資料試驗):
	def setUp(self):
		super(加文本資料試驗, self).setUp()
		self.資料表=文本表
		self.詞內容.update({
			'文本資料':'媠',
		})
		self.句內容.update({
			'文本資料':'伊誠媠。',
		})
	def test_加詞(self):
		super(加文本資料試驗, self).test_加詞()
		self.assertEqual(self.資料.文本資料,'媠')
	def test_加句(self):
		super(加文本資料試驗, self).test_加句()
		self.assertEqual(self.資料.文本資料,'伊誠媠。')
	def test_無資料(self):
		self.詞內容.pop('文本資料')
		self.assertRaise(KeyError,super(加文本資料試驗, self).test_加詞)
		self.句內容.pop('文本資料')
		self.assertRaise(KeyError,super(加文本資料試驗, self).test_加句)
