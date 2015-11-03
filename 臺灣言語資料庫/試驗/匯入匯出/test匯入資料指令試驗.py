from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase
import io
from unittest.mock import patch


class 匯入資料指令試驗(TestCase):

    @patch('臺灣言語資料庫.匯出入.匯出入工具._匯入物件')
    @patch('urllib.request.urlopen')
    def test_成功匯入(self, urlopenMocka, 匯入物件mocka):
        with io.StringIO() as out:
            call_command('匯入資料', 'http://意傳.台灣/臺灣言語資料庫.yaml', stdout=out)
            self.assertIn('「臺灣言語資料庫.yaml」成功匯入', out.getvalue())

    @patch('臺灣言語資料庫.匯出入.匯出入工具._匯入物件')
    @patch('urllib.request.urlopen')
    def test_預設愛匯入影音(self, urlopenMocka, 匯入物件mocka):
        with io.StringIO() as out:
            call_command('匯入資料', 'http://意傳.台灣/臺灣言語資料庫.yaml', stdout=out)
        匯入物件mocka.assert_called_once_with(
            urlopenMocka.return_value.__enter__.return_value, None, True
        )

    @patch('臺灣言語資料庫.匯出入.匯出入工具._匯入物件')
    @patch('urllib.request.urlopen')
    def test_莫匯入影音(self, urlopenMocka, 匯入物件mocka):
        with io.StringIO() as out:
            call_command(
                '匯入資料',
                'http://意傳.台灣/臺灣言語資料庫.yaml',
                '--莫匯入影音',
                stdout=out
            )
        匯入物件mocka.assert_called_once_with(
            urlopenMocka.return_value.__enter__.return_value, None, False
        )

    def test_無網址(self):
        with self.assertRaises(CommandError):
            call_command('匯入資料')
