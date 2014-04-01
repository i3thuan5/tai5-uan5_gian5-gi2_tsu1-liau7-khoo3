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