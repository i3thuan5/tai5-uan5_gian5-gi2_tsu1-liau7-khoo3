# -*- coding: utf-8 -*-
import codecs
from django.test import TestCase
import io
import json
from unittest.mock import patch
import wave


from 臺灣言語資料庫.試驗.加資料.加資料試驗 import 加資料試驗
from 臺灣言語資料庫.資料模型 import 影音表

class 加影音資料試驗(TestCase, 加資料試驗):
	def setUp(self):
		self.加初始資料()
		self.資料表 = 影音表
		self.詞檔案 = io.BytesIO()
		音檔 = wave.open(self.詞檔案, 'wb')
		音檔.setnchannels(1)
		音檔.setframerate(16000)
		音檔.setsampwidth(2)
		音檔.writeframesraw(b'0' * 100)
		音檔.close()
		self.句檔案 = io.BytesIO()
		音檔 = wave.open(self.句檔案, 'wb')
		音檔.setnchannels(1)
		音檔.setframerate(16000)
		音檔.setsampwidth(2)
		音檔.writeframesraw(b'sui2' * 80000)
		音檔.close()
		self.詞內容.update({
			'原始影音資料':self.詞檔案,
		})
		self.句內容.update({
			'原始影音資料':self.句檔案,
		})
	def test_加詞(self):
		super(加影音資料試驗, self).test_加詞()
		self.資料.原始影音資料. open()
		self.assertEqual(self.資料.原始影音資料.read(), self.詞檔案.getvalue())
		self.資料.原始影音資料. close()
# 		self.assertEqual(self.資料.網頁影音資料,)
	def test_加句(self):
		super(加影音資料試驗, self).test_加句()
		self.資料.原始影音資料. open()
		self.assertEqual(self.資料.原始影音資料.read(), self.句檔案.getvalue())
		self.資料.原始影音資料. close()
# 		self.assertEqual(self.資料.網頁影音資料,)
	def test_無資料(self):
		self.詞內容.pop('原始影音資料')
		self.assertRaises(KeyError, super(加影音資料試驗, self).test_加詞)
		self.assertEqual(self.資料表.objects.all().count(), 0)
		self.句內容.pop('原始影音資料')
		self.assertRaises(KeyError, super(加影音資料試驗, self).test_加句)
		self.assertEqual(self.資料表.objects.all().count(), 0)
	# 	照django.File傳AttributeError
	def test_影音資料毋是檔案(self):
		self.句內容['原始影音資料'] = 2015
		self.assertRaises(TypeError, self.資料表.加資料, self.句內容)
		self.assertEqual(self.資料表.objects.all().count(), 0)
		self.句內容['原始影音資料'] = None
		self.assertRaises(TypeError, self.資料表.加資料, self.句內容)
		self.assertEqual(self.資料表.objects.all().count(), 0)
		self.句內容['原始影音資料'] = codecs.encode('牛睏山部落的織布機課程、守城社區的母語課程')
		self.assertRaises(TypeError, self.資料表.加資料, self.句內容)
		self.assertEqual(self.資料表.objects.all().count(), 0)
		self.句內容['原始影音資料'] = '牛睏山部落的織布機課程、守城社區的母語課程'
		self.assertRaises(TypeError, self.資料表.加資料, self.句內容)
		self.assertEqual(self.資料表.objects.all().count(), 0)
	# 檔案無法度轉json字串，所以這愛改做無檔案的error
	def test_規個內容用字串(self):
		self.詞內容.pop('原始影音資料')
		self.詞內容 = json.dumps(self.詞內容)
		self.assertRaises(KeyError, super(加影音資料試驗, self).test_加詞)
		self.assertEqual(self.資料表.objects.all().count(), 0)
		self.句內容.pop('原始影音資料')
		self.句內容 = json.dumps(self.句內容)
		self.assertRaises(KeyError, super(加影音資料試驗, self).test_加句)
		self.assertEqual(self.資料表.objects.all().count(), 0)
	def test_網頁資料內容有物件(self):
		資料 = self.資料表.加資料(self.句內容)
		資料.原始影音資料. open()
		原始大小 = len(資料.原始影音資料.read())
		資料.原始影音資料. close()
		資料.網頁影音資料. open()
		網頁大小 = len(資料.網頁影音資料.read())
		資料.網頁影音資料. close()
		self.assertAlmostEqual(網頁大小, 原始大小 / 2, delta=網頁大小 * 0.1)
	@patch('libavwrapper.avconv.AVConv.run')
	def test_有走avconv(self, avconvRunMock):
		avconvRunMock.return_value.wait.return_value = 0
		self.資料表.加資料(self.句內容)
		avconvRunMock.assert_called_once_with()
	@patch('subprocess.Popen.wait')
	def test_有等avconv(self, waitMock):
		waitMock.return_value = 0
		self.資料表.加資料(self.句內容)
		waitMock.assert_called_once_with()
	@patch('subprocess.Popen.wait')
	def test_無裝avconv(self, waitMock):
		waitMock.return_value = 1
		self.assertRaises(OSError, self.資料表.加資料, self.句內容)
		waitMock.assert_called_once_with()
	@patch('subprocess.Popen.wait')
	def test_avconv失敗袂使有資料(self, waitMock):
		waitMock.return_value = 1
		句檔案 = io.BytesIO(b'sui2')
		self.句內容.update({
			'原始影音資料':句檔案,
		})
		self.assertRaises(OSError, self.資料表.加資料, self.句內容)
		self.assertEqual(影音表.objects.all().count(), 0)

