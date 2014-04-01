# -*- coding: utf-8 -*-
from django.test import TestCase
from 臺灣言語資料庫.模型 import 文字
from 臺灣言語資料庫.模型 import 關係

# Create your tests here.
class 資料庫測試(TestCase):
	def test_揣文字編修(self):
		文字物件=文字(年代=22)
		文字物件.save()
		關係物件=關係.objects.create(甲流水號=文字物件.流水號,
					乙流水號=文字物件.流水號,)
		self.assertEqual(文字物件.流水號.揣文字編修(),文字物件.流水號)
		self.assertEqual(關係物件.流水號.揣文字編修(),文字物件.流水號)
	def test_提文字組合(self):
		文字你=文字.objects.create(年代=103,型體='你',音標='li2')
		文字好=文字.objects.create(年代=103,型體='好',音標='ho2')
		文字你好=文字.objects.create(年代=103,組合=
			'#,'+str(文字你.流水號.流水號)+','+str(文字好.流水號.流水號)+',#')
		文字你好你好=文字.objects.create(年代=103,組合=
			'#,'+str(文字你.流水號.流水號)+','+str(文字你好.流水號.流水號)+',#')
		self.assertEqual(文字你.組合文字()[0],['你'])
		self.assertEqual(文字你.組合文字()[1],['li2'])
		self.assertEqual(文字你好.組合文字()[0],['你','好'])
		self.assertEqual(文字你好.組合文字()[1],['li2','ho2'])
		self.assertEqual(文字你好你好.組合文字()[0],['你','你','好'])
		self.assertEqual(文字你好你好.組合文字()[1],['li2','li2','ho2'])