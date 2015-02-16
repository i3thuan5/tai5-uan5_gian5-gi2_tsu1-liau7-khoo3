# -*- coding: utf-8 -*-
from 臺灣言語資料庫.試驗.資料庫試驗 import 資料庫試驗
import json
from 臺灣言語資料庫.欄位資訊 import 字詞
from 臺灣言語資料庫.欄位資訊 import 會使公開
from 臺灣言語資料庫.欄位資訊 import 袂使公開
from 臺灣言語資料庫.欄位資訊 import 語句
from 臺灣言語資料庫.資料模型 import 語言腔口表
from 臺灣言語資料庫.資料模型 import 著作所在地表

class 加資料試驗(資料庫試驗):
	def setUp(self):
		super(加資料試驗, self).setUp()
		self.詞屬性=json.dumps({'詞性':'形容詞'})
		self.詞內容={
			'收錄者':json.dumps({'名':'鄉民','出世年':'1950', '出世地':'臺灣'}),
			'來源':json.dumps({'名':'Dr. Pigu','出世年':'1990', '出世地':'花蓮人'}),
			'版權':'會使公開',
			'種類':'字詞',
			'語言腔口':'閩南語',
			'著作所在地':'花蓮',
			'著作年':'2014',
			'屬性':self.詞屬性,
			}
		self.句屬性=json.dumps({'性質':'例句'})
		self.句內容={
			'收錄者':json.dumps({'名':'Dr. Pigu','出世年':'1990', '出世地':'花蓮人'}),
			'來源':json.dumps({'名':'鄉民','出世年':'1950', '出世地':'臺灣'}),
			'版權':'袂使公開',
			'種類':'語句',
			'語言腔口':'四縣話',
			'著作所在地':'臺灣',
			'著作年':'195x',
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
		self.assertEqual(self.資料.著作所在地,self.花蓮)
		self.assertEqual(self.資料.著作年.著作年,self.二空一四)
		self.assertEqual(self.資料.屬性,self.詞屬性)
	def test_加句(self):
		原來資料數=self.資料表.objects.all().count()
		self.資料=self.資料表.加一筆(self.句內容)
		self.assertEqual(self.資料表.objects.all().count(),原來資料數+1)
		self.assertEqual(self.資料.收錄者,self.花蓮人)
		self.assertEqual(self.資料.來源,self.臺灣人)
		self.assertEqual(self.資料.版權,self.袂使公開)
		self.assertEqual(self.資料.種類,self.語句)
		self.assertEqual(self.資料.語言腔口,self.四縣話)
		self.assertEqual(self.資料.著作所在地,self.臺灣)
		self.assertEqual(self.資料.著作年.著作年,self.一九五空年代)
		self.assertEqual(self.資料.屬性,self.句屬性)
	def test_濟个正常語料(self):
		self.test_加詞()
		self.test_加句()
		self.test_加句()
		self.test_加詞()
		self.test_加詞()
		self.test_加句()
		self.test_加句()
	def test_收錄者舊編號(self):
		self.句內容['收錄者']=self.花蓮人.pk
		原來資料數=self.資料表.objects.all().count()
		資料=self.資料表.加一筆(self.句內容)
		self.assertEqual(self.資料表.objects.all().count(),原來資料數+1)
		self.assertEqual(資料.收錄者,self.花蓮人)
		self.assertEqual(資料.來源,self.臺灣人)
		self.assertEqual(資料.版權,self.袂使公開)
		self.assertEqual(資料.種類,self.語句)
		self.assertEqual(資料.語言腔口,self.四縣話)
		self.assertEqual(資料.著作所在地,self.臺灣)
		self.assertEqual(資料.著作年.著作年,self.一九五空年代)
		self.assertEqual(資料.屬性,self.句屬性)
	def test_收錄者新字串(self):
		self.句內容['收錄者']=json.dumps({'名':'Dr. Pigu','出世年':'1990', '出世地':'花蓮人'})
		self.assertRaise(ObjectDoesNotExist,self.資料表.加一筆,self.句內容)
	def test_收錄者新編號(self):
		self.句內容['收錄者']=json.dumps({'名':'Dr. Pigu','出世年':'1990', '出世地':'花蓮人'})
		self.assertRaise(ObjectDoesNotExist,self.資料表.加一筆,self.句內容)
	def test_來源舊編號(self):
		self.句內容['來源']=self.臺灣人.pk
		原來資料數=self.資料表.objects.all().count()
		資料=self.資料表.加一筆(self.句內容)
		self.assertEqual(self.資料表.objects.all().count(),原來資料數+1)
		self.assertEqual(資料.收錄者,self.花蓮人)
		self.assertEqual(資料.來源,self.臺灣人)
		self.assertEqual(資料.版權,self.袂使公開)
		self.assertEqual(資料.種類,self.語句)
		self.assertEqual(資料.語言腔口,self.四縣話)
		self.assertEqual(資料.著作所在地,self.臺灣)
		self.assertEqual(資料.著作年.著作年,self.一九五空年代)
		self.assertEqual(資料.屬性,self.句屬性)
	def test_來源新字串(self):
		self.句內容['來源']=json.dumps({'名':'阿媠','職業':'學生'})
		原來資料數=self.資料表.objects.all().count()
		資料=self.資料表.加一筆(self.句內容)
		self.assertEqual(self.資料表.objects.all().count(),原來資料數+1)
		self.assertEqual(資料.收錄者,self.花蓮人)
		self.assertEqual(資料.來源.名,'阿媠')
		self.assertEqual(json.dumps(資料.來源.屬性),{'職業':'學生'})
		self.assertEqual(資料.版權,self.袂使公開)
		self.assertEqual(資料.種類,self.語句)
		self.assertEqual(資料.語言腔口,self.四縣話)
		self.assertEqual(資料.著作所在地,self.臺灣)
		self.assertEqual(資料.著作年,self.一九五空年代)
		self.assertEqual(資料.屬性,self.句屬性)
	def test_來源新字串無名(self):
		self.句內容['來源']=json.dumps({'姓名':'阿媠','職業':'學生'})
		self.assertRaise(ObjectDoesNotExist,self.資料表.加一筆,self.句內容)
	def test_來源新編號(self):
		self.句內容['來源']=200
		self.assertRaise(ObjectDoesNotExist,self.資料表.加一筆,self.句內容)
	def test_版權舊編號(self):
		self.句內容['版權']=self.袂使公開.pk
		原來資料數=self.資料表.objects.all().count()
		資料=self.資料表.加一筆(self.句內容)
		self.assertEqual(self.資料表.objects.all().count(),原來資料數+1)
		self.assertEqual(資料.收錄者,self.花蓮人)
		self.assertEqual(資料.來源,self.臺灣人)
		self.assertEqual(資料.版權,self.袂使公開)
		self.assertEqual(資料.種類,self.語句)
		self.assertEqual(資料.語言腔口,self.四縣話)
		self.assertEqual(資料.著作所在地,self.臺灣)
		self.assertEqual(資料.著作年,self.一九五空年代)
		self.assertEqual(資料.屬性,self.句屬性)
	def test_版權新字串(self):
		self.句內容['版權']='攏會使'
		self.assertRaise(ObjectDoesNotExist,self.資料表.加一筆,self.句內容)
	def test_版權新編號(self):
		self.句內容['版權']=2815
		self.assertRaise(ObjectDoesNotExist,self.資料表.加一筆,self.句內容)
	def test_種類舊編號(self):
		self.句內容['種類']=self.語句.pk
		原來資料數=self.資料表.objects.all().count()
		資料=self.資料表.加一筆(self.句內容)
		self.assertEqual(self.資料表.objects.all().count(),原來資料數+1)
		self.assertEqual(資料.收錄者,self.花蓮人)
		self.assertEqual(資料.來源,self.臺灣人)
		self.assertEqual(資料.版權,self.袂使公開)
		self.assertEqual(資料.種類,self.語句)
		self.assertEqual(資料.語言腔口,self.四縣話)
		self.assertEqual(資料.著作所在地,self.臺灣)
		self.assertEqual(資料.著作年,self.一九五空年代)
		self.assertEqual(資料.屬性,self.句屬性)
	def test_種類新字串(self)
		self.句內容['種類']='課本'
		self.assertRaise(ObjectDoesNotExist,self.資料表.加一筆,self.句內容)
	def test_種類新編號(self):
		self.句內容['種類']=-5
		self.assertRaise(ObjectDoesNotExist,self.資料表.加一筆,self.句內容)
	def test_語言腔口舊編號(self):
		self.句內容['語言腔口']=self.四縣話.pk
		原來資料數=self.資料表.objects.all().count()
		資料=self.資料表.加一筆(self.句內容)
		self.assertEqual(self.資料表.objects.all().count(),原來資料數+1)
		self.assertEqual(資料.收錄者,self.花蓮人)
		self.assertEqual(資料.來源,self.臺灣人)
		self.assertEqual(資料.版權,self.袂使公開)
		self.assertEqual(資料.種類,self.語句)
		self.assertEqual(資料.語言腔口,self.四縣話)
		self.assertEqual(資料.著作所在地,self.臺灣)
		self.assertEqual(資料.著作年.著作年,self.一九五空年代)
		self.assertEqual(資料.屬性,self.句屬性)
	def test_語言腔口新字串(self):
		self.句內容['語言腔口']='豬豬語'
		原來資料數=self.資料表.objects.all().count()
		資料=self.資料表.加一筆(self.句內容)
		self.assertEqual(self.資料表.objects.all().count(),原來資料數+1)
		self.assertEqual(資料.收錄者,self.花蓮人)
		self.assertEqual(資料.來源,self.臺灣人)
		self.assertEqual(資料.版權,self.袂使公開)
		self.assertEqual(資料.種類,self.語句)
		self.assertEqual(資料.語言腔口.語言腔口,'豬豬語')
		self.assertEqual(資料.著作所在地,self.臺灣)
		self.assertEqual(資料.著作年,self.一九五空年代)
		self.assertEqual(資料.屬性,self.句屬性)
	def test_語言腔口新編號(self):
		self.句內容['語言腔口']=語言腔口表.objects.count()*5
		self.assertRaise(ObjectDoesNotExist,self.資料表.加一筆,self.句內容)
	def test_著作所在地舊編號(self):
		self.句內容['著作所在地']=self.臺灣.pk
		原來資料數=self.資料表.objects.all().count()
		資料=self.資料表.加一筆(self.句內容)
		self.assertEqual(self.資料表.objects.all().count(),原來資料數+1)
		self.assertEqual(資料.收錄者,self.花蓮人)
		self.assertEqual(資料.來源,self.臺灣人)
		self.assertEqual(資料.版權,self.袂使公開)
		self.assertEqual(資料.種類,self.語句)
		self.assertEqual(資料.語言腔口,self.四縣話)
		self.assertEqual(資料.著作所在地,self.臺灣)
		self.assertEqual(資料.著作年,self.一九五空年代)
		self.assertEqual(資料.屬性,self.句屬性)
	def test_著作所在地新字串(self):
		self.句內容['著作所在地']='埔里'
		原來資料數=self.資料表.objects.all().count()
		資料=self.資料表.加一筆(self.句內容)
		self.assertEqual(self.資料表.objects.all().count(),原來資料數+1)
		self.assertEqual(資料.收錄者,self.花蓮人)
		self.assertEqual(資料.來源,self.臺灣人)
		self.assertEqual(資料.版權,self.袂使公開)
		self.assertEqual(資料.種類,self.語句)
		self.assertEqual(資料.語言腔口,self.四縣話)
		self.assertEqual(資料.著作所在地.著作所在地,'埔里')
		self.assertEqual(資料.著作年,self.一九五空年代)
		self.assertEqual(資料.屬性,self.句屬性)
	def test_著作所在地新編號(self):
		self.句內容['著作所在地']=著作所在地表.objects.order('-pk').first().pk+1
		原來資料數=self.資料表.objects.all().count()
		資料=self.資料表.加一筆(self.句內容)
		self.assertEqual(self.資料表.objects.all().count(),原來資料數+1)
		self.assertEqual(資料.收錄者,self.花蓮人)
		self.assertEqual(資料.來源,self.臺灣人)
		self.assertEqual(資料.版權,self.袂使公開)
		self.assertEqual(資料.種類,self.語句)
		self.assertEqual(資料.語言腔口,self.四縣話)
		self.assertEqual(資料.著作所在地,self.臺灣)
		self.assertEqual(資料.著作年,self.一九五空年代)
		self.assertEqual(資料.屬性,self.句屬性)
	def test_著作年舊編號(self):
		self.句內容['著作年']=self.一九五空年代.pk
		原來資料數=self.資料表.objects.all().count()
		資料=self.資料表.加一筆(self.句內容)
		self.assertEqual(self.資料表.objects.all().count(),原來資料數+1)
		self.assertEqual(資料.收錄者,self.花蓮人)
		self.assertEqual(資料.來源,self.臺灣人)
		self.assertEqual(資料.版權,self.袂使公開)
		self.assertEqual(資料.種類,self.語句)
		self.assertEqual(資料.語言腔口,self.四縣話)
		self.assertEqual(資料.著作所在地,self.臺灣)
		self.assertEqual(資料.著作年,self.一九五空年代)
		self.assertEqual(資料.屬性,self.句屬性)
	def test_著作年新字串(self):
		self.句內容['著作年']='19xx'
		原來資料數=self.資料表.objects.all().count()
		資料=self.資料表.加一筆(self.句內容)
		self.assertEqual(self.資料表.objects.all().count(),原來資料數+1)
		self.assertEqual(資料.收錄者,self.花蓮人)
		self.assertEqual(資料.來源,self.臺灣人)
		self.assertEqual(資料.版權,self.袂使公開)
		self.assertEqual(資料.種類,self.語句)
		self.assertEqual(資料.語言腔口,self.四縣話)
		self.assertEqual(資料.著作所在地,self.臺灣)
		self.assertEqual(資料.著作年.著作年,'19xx')
		self.assertEqual(資料.屬性,self.句屬性)
	def test_著作年新編號(self):
		self.句內容['著作年']=333
		self.assertRaise(ValueError,self.資料表.加一筆,self.句內容)
	def test_屬性無合法的json(self):
		self.句內容['屬性']='{[}'
		self.assertRaise(ValueError,self.資料表.加一筆,self.句內容)
	def test_屬性毋是字串(self):
		self.句內容['屬性']=33
		self.assertRaise(TypeError,self.資料表.加一筆,self.句內容)
	def test_濟个綜合語料(self):
		self.句內容['來源']=json.dumps({'名':'阿媠','職業':'學生'})
		self.句內容['版權']=self.袂使公開.pk
		self.句內容['語言腔口']='豬豬語'
		self.句內容['著作所在地']='員林'
		原來資料數=self.資料表.objects.all().count()
		資料=self.資料表.加一筆(self.句內容)
		self.assertEqual(self.資料表.objects.all().count(),原來資料數+1)
		self.assertEqual(資料.收錄者,self.花蓮人)
		self.assertEqual(資料.來源.名,'阿媠')
		self.assertEqual(json.dumps(資料.來源.屬性),{'職業':'學生'})
		self.assertEqual(資料.版權,self.袂使公開)
		self.assertEqual(資料.種類,self.語句)
		self.assertEqual(資料.語言腔口.語言腔口,'豬豬語')
		self.assertEqual(資料.著作所在地.著作所在地,'員林')
		self.assertEqual(資料.著作年,self.一九五空年代)
		self.assertEqual(資料.屬性,self.句屬性)
		