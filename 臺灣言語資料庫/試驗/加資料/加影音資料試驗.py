# -*- coding: utf-8 -*-
from 臺灣言語資料庫.試驗.加資料.加資料試驗 import 加資料試驗
from 臺灣言語資料庫.資料模型 import 影音表
import io
import wave

class 加影音資料試驗(加資料試驗):
	def setUp(self):
		super(加影音資料試驗, self).setUp()
		self.資料表=影音表
		self.詞檔案=io.BytesIO()
		音檔=wave.open(self.詞檔案,'wb')
		音檔.setnchannels(1)
		音檔.setframerate(16000)
		音檔.setsampwidth(2)
		音檔.writeframesraw(b'0'*100)
		音檔.close()
		self.句檔案=io.BytesIO()
		音檔=wave.open(self.句檔案,'wb')
		音檔.setnchannels(1)
		音檔.setframerate(16000)
		音檔.setsampwidth(2)
		音檔.writeframesraw(b'0'*100)
		音檔.close()
		self.詞內容.update({
			'原始影音資料':self.詞檔案,
		})
		self.句內容.update({
			'原始影音資料':self.句檔案,
		})
	def test_加詞(self):
		super(加影音資料試驗, self).test_加詞()
		self.assertEqual(self.資料.原始影音資料.read(),self.詞檔案.getvalue())
# 		self.assertEqual(self.資料.網頁影音資料,)
	def test_加句(self):
		super(加影音資料試驗, self).test_加句()
		self.assertEqual(self.資料.原始影音資料.read(),self.句檔案.getvalue())
# 		self.assertEqual(self.資料.網頁影音資料,)
	def test_無資料(self):
		self.詞內容.pop('原始影音資料')
		self.assertRaises(KeyError,super(加影音資料試驗, self).test_加詞)
		self.句內容.pop('原始影音資料')
		self.assertRaises(KeyError,super(加影音資料試驗, self).test_加句)
