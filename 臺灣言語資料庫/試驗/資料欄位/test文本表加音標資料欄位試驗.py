# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test import TransactionTestCase
from django.db.migrations.executor import MigrationExecutor
from django.db import connection
from 臺灣言語資料庫.資料模型 import 來源表
from django.core.exceptions import ObjectDoesNotExist
from 臺灣言語資料庫.資料模型 import 來源屬性表
from 臺灣言語資料庫.資料模型 import 文本表


class 文本表加音標資料欄位試驗(TransactionTestCase):
    app名 = '臺灣言語資料庫'

    def setUp(self):
        self.executor = MigrationExecutor(connection)
        self.executor.migrate([(self.app名, '0003_auto_20151009_0731_版權加長度')])

    def 徙資料庫(self, apps):
        self.executor.migrate([(self.app名, '0004_文本表_音標資料')])

    def test_原本屬性有音標(self):
        文本表.加資料({
            '收錄者': {'名': 'Dr. Pigu'},
            '來源': {'名': '鄉民'},
            '版權': '公開',
            '種類': '字詞',
            '語言腔口': '臺語',
            '著作所在地': '臺灣',
            '著作年': '2016',
            '文本資料': '媠',
            '屬性': {'音標': 'sui2'},
        })
        self.徙資料庫()
        文本 = 文本表.objects.get(文本資料='媠')
        self.assertEqual(文本.音標資料, 'sui2')

    def test_屬性的音標會無去(self):
        文本表.加資料({
            '收錄者': {'名': 'Dr. Pigu'},
            '來源': {'名': '鄉民'},
            '版權': '公開',
            '種類': '字詞',
            '語言腔口': '臺語',
            '著作所在地': '臺灣',
            '著作年': '2016',
            '文本資料': '媠',
            '屬性': {'音標': 'sui2'},
        })
        self.徙資料庫()
        文本 = 文本表.objects.get(文本資料='媠')
        self.assertEqual(文本.屬性.count(), 0)

    def test_原本屬性無音標(self):
        文本表.加資料({
            '收錄者': {'名': 'Dr. Pigu'},
            '來源': {'名': '鄉民'},
            '版權': '公開',
            '種類': '字詞',
            '語言腔口': '臺語',
            '著作所在地': '臺灣',
            '著作年': '2016',
            '文本資料': '媠',
            '屬性': {},
        })
        self.徙資料庫()
        文本 = 文本表.objects.get(文本資料='媠')
        self.assertEqual(文本.音標資料, '')
