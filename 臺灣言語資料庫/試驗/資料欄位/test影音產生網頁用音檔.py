import io
from unittest.mock import patch
import wave

from django.test.testcases import TestCase


from 臺灣言語資料庫.資料模型 import 影音表
from 臺灣言語資料庫.資料模型 import 來源表
from 臺灣言語資料庫.資料模型 import 版權表


class 影音產生網頁用音檔(TestCase):

    def setUp(self):
        self.句檔案 = io.BytesIO()
        with wave.open(self.句檔案, 'wb') as 音檔:
            音檔.setnchannels(1)
            音檔.setframerate(16000)
            音檔.setsampwidth(2)
            音檔.writeframesraw(b'sui2' * 80000)
        詞內容 = {
            '收錄者': 來源表.objects.get_or_create(名='系統管理員')[0],
            '來源': {'名': 'Konn', },
            '版權': 版權表.objects.get_or_create(版權='會使公開')[0],
            '種類': '語句',
            '語言腔口': '閩南語',
            '著作所在地': '花蓮',
            '著作年': '2016',
            '原始影音資料': self.句檔案,
        }
        self.資料 = 影音表.加資料(詞內容)

    def tearDown(self):
        self.句檔案.close()

    @patch('libavwrapper.avconv.AVConv.run')
    def test_有走avconv(self, avconvRunMock):
        avconvRunMock.return_value.wait.return_value = 0
        self.資料.網頁影音資料()
        avconvRunMock.assert_called_once_with()

    @patch('subprocess.Popen.wait')
    def test_有等avconv(self, waitMock):
        waitMock.return_value = 0
        self.資料.網頁影音資料()
        waitMock.assert_called_once_with()

    @patch('subprocess.Popen.wait')
    def test_無裝avconv(self, waitMock):
        waitMock.return_value = 1
        self.assertRaises(OSError, self.資料.網頁影音資料)
        waitMock.assert_called_once_with()

    @patch('subprocess.Popen.wait')
    def test_avconv失敗袂使有資料(self, waitMock):
        waitMock.return_value = 1
        句檔案 = io.BytesIO(b'sui2')
        self.句內容.update({
            '原始影音資料': 句檔案,
        })
        self.assertRaises(OSError, self.資料.網頁影音資料)
        self.assertEqual(影音表.objects.all().count(), 0)

    def test_網頁資料內容有物件(self):
        self.資料.影音資料.open()
        原始大小 = len(self.資料.原始影音資料.read())
        self.資料.影音資料.close()
        網頁大小 = len(self.資料.網頁影音資料())
        self.assertAlmostEqual(網頁大小, 原始大小 / 2, delta=網頁大小 * 0.1)
