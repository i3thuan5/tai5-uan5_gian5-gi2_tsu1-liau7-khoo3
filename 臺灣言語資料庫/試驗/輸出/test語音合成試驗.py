from django.test.testcases import TestCase
import gzip
import io
from os import listdir
from os.path import join, dirname, isfile, isdir
from shutil import rmtree
from unittest.mock import patch
import wave
from 臺灣言語資料庫.資料模型 import 版權表
from 臺灣言語資料庫.欄位資訊 import 會使公開
from 臺灣言語資料庫.欄位資訊 import 字詞
from 臺灣言語資料庫.資料模型 import 來源表
from 臺灣言語資料庫.資料模型 import 外語表
from 臺灣言語資料庫.資料模型 import 文本表
from 臺灣言語資料庫.資料模型 import 影音表
from 臺灣言語資料庫.輸出 import 資料輸出工具


class 語音合成試驗(TestCase):

    def setUp(self):
        版權表.objects.create(版權=會使公開)
        Pigu = 來源表.objects.create(名='Dr. Pigu')
        self.資料內容 = {
            '收錄者': Pigu.編號(),
            '來源': Pigu.編號(),
            '版權': '會使公開',
            '種類': '語句',
            '語言腔口': '閩南語',
            '著作所在地': '花蓮',
            '著作年': '2015',
        }

        self.語料 = 資料輸出工具()
        self.目錄 = join(dirname(__file__), '結果目錄')

    def tearDown(self):
        if isdir(self.目錄):
            rmtree(self.目錄)

    def test_揣出指定語者的語音語料(self):
        self.語料.輸出指定語者語音合成語料(self.目錄, 語者)
        self.assertEqual(len(listdir(self.目錄)), 0)
        self.fail()

    def test_揣出指定語者的語音語料轉檔調整頻率(self):
        self.語料.輸出指定語者語音合成語料(self.目錄, 語者)
        self.assertEqual(len(listdir(self.目錄)), 0)
        self.fail()

    def test_揣出指定語者的語音語料調整聲道(self):
        self.語料.輸出指定語者語音合成語料(self.目錄, 語者)
        self.assertEqual(len(listdir(self.目錄)), 0)
        self.fail()

    @patch('臺灣言語資料庫.輸出.資料輸出工具.輸出指定語者語音合成語料')
    def test_無語料就啥物攏無(self, 語者語音合成語料mock):
        self.語料.輸出語音合成語料(self.目錄)
        self.assertEqual(len(listdir(self.目錄)), 0)
        self.assertEqual(語者語音合成語料mock.call_count, 0)

    @patch('臺灣言語資料庫.輸出.資料輸出工具.輸出指定語者語音合成語料')
    def test_揣出逐個語言上濟的語音語料孤人(self,語者語音合成語料mock):
        self.語料.輸出語音合成語料(self.目錄)
        語者語音合成語料mock.assert_called_once_with()
        self.fail()

    @patch('臺灣言語資料庫.輸出.資料輸出工具.輸出指定語者語音合成語料')
    def test_揣出逐個語言上濟的語音語料雙人(self,語者語音合成語料mock):
        self.語料.輸出語音合成語料(self.目錄)
        self.assertEqual(len(listdir(self.目錄)), 0)
        語者語音合成語料mock.assert_called_once_with()
        self.fail()

    def 加一筆影音資料(self):
        影音資料 = io.BytesIO()
        with wave.open(影音資料, 'wb') as 音檔:
            音檔.setnchannels(1)
            音檔.setframerate(16000)
            音檔.setsampwidth(2)
            音檔.writeframesraw(b'0' * 100)
        影音內容 = {'原始影音資料': 影音資料}
        影音內容.update(self.資料內容)
        return 影音表.加資料(影音內容)
