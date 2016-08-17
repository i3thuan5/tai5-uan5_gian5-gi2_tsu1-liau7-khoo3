# -*- coding: utf-8 -*-
from django.test import TestCase
from 臺灣言語資料庫.試驗.加資料.加資料試驗 import 加資料試驗
from 臺灣言語資料庫.資料模型 import 聽拍表
from 臺灣言語資料庫.資料模型 import 聽拍規範表
import json
from django.core.exceptions import ObjectDoesNotExist, ValidationError


class 加聽拍資料試驗(TestCase, 加資料試驗):

    def setUp(self):
        self.加初始資料佮設定變數()
        self.資料表 = 聽拍表
        self.中研院聽拍資料庫 = 聽拍規範表.objects.create(
            規範名='中研院聽拍資料庫',
            範例='你好：li1 ho2',
            說明='記錄實際口說的聲調',
        )
        self.詞內容.update({
            '規範': '中研院聽拍資料庫',
            '聽拍資料': [
                        {'語者': '阿宏', '內容': 'li1', '開始時間': 0.0, '結束時間': 1.2},
                        {'語者': '阿莉', '內容': 'ho2', '開始時間': 1.2, '結束時間': 2.0},
                        ]
        })
        self.句內容.update({
            '規範': '中研院聽拍資料庫',
            '聽拍資料': [
                        {'內容': '請問車頭按怎行？'},
                        {'內容': '直直行就到矣。'},
                        ]
        })

    def 屬性加語者資料(self):
        self.詞內容['屬性'].update({
            '人數': ['2'],
            '語者': {
                '阿宏': {'性別': '查埔', '年紀': '25'},
                '阿莉': {'性別': '查某', '年紀': '25'},
            }
        })

    def test_加詞(self):
        super(加聽拍資料試驗, self).test_加詞()
        self.assertEqual(self.資料.規範, self.中研院聽拍資料庫)
        self.assertEqual(json.loads(self.資料.聽拍資料), [
            {'語者': '阿宏', '內容': 'li1', '開始時間': 0.0, '結束時間': 1.2},
            {'語者': '阿莉', '內容': 'ho2', '開始時間': 1.2, '結束時間': 2.0},
        ])
        self.比較屬性(self.資料, {
            '詞性': '形容詞',
        })

    def test_加句(self):
        super(加聽拍資料試驗, self).test_加句()
        self.assertEqual(self.資料.規範, self.中研院聽拍資料庫)
        self.assertEqual(json.loads(self.資料.聽拍資料),
                         [
            {'內容': '請問車頭按怎行？'},
            {'內容': '直直行就到矣。'},
        ]
        )

    def test_規範舊編號(self):
        self.詞內容['規範'] = self.中研院聽拍資料庫.pk
        self.資料 = self.資料表.加資料(self.詞內容)
        self.assertEqual(self.資料.規範, self.中研院聽拍資料庫)
        self.assertEqual(json.loads(self.資料.聽拍資料), [
            {'語者': '阿宏', '內容': 'li1', '開始時間': 0.0, '結束時間': 1.2},
            {'語者': '阿莉', '內容': 'ho2', '開始時間': 1.2, '結束時間': 2.0},
        ])
        self.比較屬性(self.資料, {
            '詞性': '形容詞',
        })

    def test_規範舊物件(self):
        self.詞內容['規範'] = self.中研院聽拍資料庫
        self.資料 = self.資料表.加資料(self.詞內容)
        self.assertEqual(self.資料.規範, self.中研院聽拍資料庫)
        self.assertEqual(json.loads(self.資料.聽拍資料), [
            {'語者': '阿宏', '內容': 'li1', '開始時間': 0.0, '結束時間': 1.2},
            {'語者': '阿莉', '內容': 'ho2', '開始時間': 1.2, '結束時間': 2.0},
        ])
        self.比較屬性(self.資料, {
            '詞性': '形容詞',
        })

    def test_規範新字串(self):
        self.句內容['規範'] = '新聽拍方法'
        self.assertRaises(ObjectDoesNotExist, self.資料表.加資料, self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)

    def test_規範新編號(self):
        self.句內容['規範'] = 109
        self.assertRaises(ObjectDoesNotExist, self.資料表.加資料, self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)

    def test_規範毋是字串佮編號(self):
        self.句內容['規範'] = 2015.0217
        with self.assertRaises(ValueError):
            self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)
        self.句內容['規範'] = ['「忘了母語，我還會記得怎麼奔跑嗎？」']
        with self.assertRaises(ValueError):
            self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)
        self.句內容['規範'] = None
        with self.assertRaises(ValidationError):
            self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)

    def test_無聽拍資料(self):
        self.詞內容.pop('聽拍資料')
        self.assertRaises(KeyError, super(加聽拍資料試驗, self).test_加詞)
        self.assertEqual(self.資料表.objects.all().count(), 0)
        self.句內容.pop('聽拍資料')
        self.assertRaises(KeyError, super(加聽拍資料試驗, self).test_加句)
        self.assertEqual(self.資料表.objects.all().count(), 0)

    def test_聽拍資料無內容欄位(self):
        self.詞內容['聽拍資料'] = [
            {'語者': '阿宏', '開始時間': 0.0, '結束時間': 1.2},
            {'語者': '阿莉', '開始時間': 1.2, '結束時間': 2.0},
        ]
        self.assertRaises(KeyError, super(加聽拍資料試驗, self).test_加詞)
        self.assertEqual(self.資料表.objects.all().count(), 0)

    def test_空的聽拍資料(self):
        self.詞內容['聽拍資料'] = []
        self.資料 = self.資料表.加資料(self.詞內容)
        self.assertEqual(self.資料.規範, self.中研院聽拍資料庫)
        self.assertEqual(json.loads(self.資料.聽拍資料), [
        ])
        self.比較屬性(self.資料, {
            '詞性': '形容詞',
        })

    def test_聽拍資料用字串(self):
        self.詞內容['聽拍資料'] = json.dumps(self.詞內容['聽拍資料'])
        self.test_加詞()
        self.句內容['聽拍資料'] = json.dumps(self.句內容['聽拍資料'])
        self.test_加句()

    def test_聽拍資料毋是字串佮物件(self):
        self.句內容['聽拍資料'] = 2015
        with self.assertRaises(ValueError):
            self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)
        self.句內容['聽拍資料'] = None
        with self.assertRaises(ValueError):
            self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)
        self.句內容['聽拍資料'] = {'牛睏山部落的織布機課程', '守城社區的母語課程'}
        with self.assertRaises(ValueError):
            self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)
        self.句內容['聽拍資料'] = ['牛睏山部落的織布機課程', '守城社區的母語課程']
        with self.assertRaises(ValueError):
            self.資料表.加資料(self.句內容)
        self.assertEqual(self.資料表.objects.all().count(), 0)

    def test_屬性加語者資料(self):
        self.屬性加語者資料()
        self.資料 = self.資料表.加資料(self.詞內容)
        self.assertEqual(self.資料.規範, self.中研院聽拍資料庫)
        self.assertEqual(json.loads(self.資料.聽拍資料), [
            {'語者': '阿宏', '內容': 'li1', '開始時間': 0.0, '結束時間': 1.2},
            {'語者': '阿莉', '內容': 'ho2', '開始時間': 1.2, '結束時間': 2.0},
        ])
        self.比較屬性(self.資料, {
            '詞性': '形容詞',
            '人數': ['2'],
            '語者': {
                '阿宏': {'性別': '查埔', '年紀': '25'},
                '阿莉': {'性別': '查某', '年紀': '25'},
            }
        })
