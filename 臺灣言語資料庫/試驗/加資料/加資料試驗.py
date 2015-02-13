# -*- coding: utf-8 -*-
from 臺灣言語資料庫.試驗.資料庫試驗 import 資料庫試驗
import json
from 臺灣言語資料庫.欄位資訊 import 字詞
from 臺灣言語資料庫.欄位資訊 import 會使公開
from 臺灣言語資料庫.欄位資訊 import 袂使公開
from 臺灣言語資料庫.欄位資訊 import 語句

class 加資料試驗(資料庫試驗):
	def setUp(self):
		super(加資料試驗, self).setUp()
		self.詞屬性=json.dumps({'詞性':'形容詞'})
		self.詞內容={
			'收錄者':json.dumps({'名':'鄉民','出世年':'1950', '出世地':'臺灣'}),
			'來源':json.dumps({'名':'Dr. Pigu','出世年':'1990', '出世地':'花蓮人'}),
			'版權':會使公開,
			'種類':字詞,
			'語言腔口':'閩南語',
			'語料所在地':'花蓮',
			'著作時間':'2014',
			'屬性':self.詞屬性,
			}
		self.句屬性=json.dumps({'性質':'例句'})
		self.句內容={
			'收錄者':json.dumps({'名':'Dr. Pigu','出世年':'1990', '出世地':'花蓮人'}),
			'來源':json.dumps({'名':'鄉民','出世年':'1950', '出世地':'臺灣'}),
			'版權':袂使公開,
			'種類':語句,
			'語言腔口':'四縣話',
			'語料所在地':'臺灣',
			'著作時間':'195x',
			'屬性':self.句屬性,
			}
	def test_加詞(self):
		原來資料數=self.資料表.objects.all().count()
		self.資料=self.資料表.加一筆(self.詞內容)
		self.assertEqual(self.資料表.objects.all().count(),原來資料數+1)
		self.assertEqual(self.資料.收錄者,self.臺灣人)
		self.assertEqual(self.資料.來源,self.花蓮人)
		self.assertEqual(self.資料.版權,self.會使公開)
		self.assertEqual(self.資料.種類,self.字詞)
		self.assertEqual(self.資料.語言腔口,self.閩南語)
		self.assertEqual(self.資料.語料所在地,self.花蓮)
		self.assertEqual(self.資料.著作時間.著作時間,self.二空一四)
		self.assertEqual(self.資料.屬性,self.詞屬性)
	def test_加句(self):
		原來資料數=self.資料表.objects.all().count()
		self.資料=self.資料表.加一筆(self.句內容)
		self.assertEqual(self.資料表.objects.all().count(),原來資料數+1)
		self.assertEqual(self.資料.收錄者,self.花蓮人)
		self.assertEqual(self.資料.來源,self.臺灣人)
		self.assertEqual(self.資料.版權,self.會使公開)
		self.assertEqual(self.資料.種類,self.語句)
		self.assertEqual(self.資料.語言腔口,self.四縣話)
		self.assertEqual(self.資料.語料所在地,self.臺灣)
		self.assertEqual(self.資料.著作時間.著作時間,self.一九五空年代)
		self.assertEqual(self.資料.屬性,self.句屬性)
	def test_濟个正常語料(self):
		self.test_加詞()
		self.test_加句()
		self.test_加句()
		self.test_加詞()
		self.test_加詞()
		self.test_加句()
		self.test_加句()
	def test_收錄者新字串(self):
	def test_收錄者舊編號(self):
	def test_收錄者新編號(self):
	def test_來源新字串(self):
	def test_來源舊編號(self):
	def test_來源新編號(self):
	def test_版權新字串(self):
	def test_版權舊編號(self):
	def test_版權新編號(self):
	def test_種類新字串(self):
	def test_種類舊編號(self):
	def test_種類新編號(self):
	def test_語言腔口新字串(self):
	def test_語言腔口舊編號(self):
	def test_語言腔口新編號(self):
	def test_著作所在地新字串(self):
	def test_著作所在地舊編號(self):
	def test_著作所在地新編號(self):
	def test_著作時間新字串(self):
	def test_著作時間舊編號(self):
	def test_著作時間新編號(self):
		
	def test_屬性無合法的json(self):
		pass
	def test_屬性毋是字串(self):
		pass
	def test_濟个綜合語料(self):
		self.test_無來源()
		pass