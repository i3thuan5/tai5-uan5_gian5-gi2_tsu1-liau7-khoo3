from django.test.testcases import TestCase
from os.path import dirname, abspath, join
from unittest.mock import patch, call
from 臺灣言語資料庫.資料模型 import 文本表
from 臺灣言語資料庫.匯出入 import 匯出入工具
from 臺灣言語資料庫.資料模型 import 來源表


class 匯入試驗(TestCase):

    def setUp(self):
        self.匯入工具 = 匯出入工具()

    @patch('臺灣言語資料庫.資料模型.文本表.加資料')
    def test_下層攏愛做著(self, 加資料mocka):
        self.匯入工具.匯入檔案(self._提yaml資料('異用字.yaml'))
        self.assertEqual(加資料mocka.call_count, 2)

    @patch('臺灣言語資料庫.資料模型.文本表.加資料')
    def test_文本資料(self, 加資料mocka):
        self.匯入工具.匯入檔案(self._提yaml資料('異用字.yaml'))
        加資料mocka.assert_has_calls([
            call({
                '收錄者': 來源表.objects.get(名='系統管理者'),
                '來源': {'名': '教育部閩南語辭典'},
                '版權': '姓名標示-禁止改作 3.0 台灣',
                '種類': '字詞',
                '著作年': '2015',
                '著作所在地': '臺灣',
                '語言腔口': '閩南語',
                '文本資料': '蜀',
            }),
            call({
                '收錄者': 來源表.objects.get(名='系統管理者'),
                '來源': {'名': '教育部閩南語辭典'},
                '版權': '姓名標示-禁止改作 3.0 台灣',
                '種類': '字詞',
                '著作年': '2015',
                '著作所在地': '臺灣',
                '語言腔口': '閩南語',
                '文本資料': '落翅仔',
            }),
        ], any_order=True)

    @patch('臺灣言語資料庫.資料模型.文本表.校對做')
    def test_文本資料校對數量(self, 校對做mocka):
        self.匯入工具.匯入檔案(self._提yaml資料('異用字.yaml'))
        self.assertGreaterEqual(校對做mocka.call_count, 2)

    def test_文本資料校對資料(self):
        self.匯入工具.匯入檔案(self._提yaml資料('異用字.yaml'))
        self.assertEqual(文本表.objects.filter(文本資料='一').count(), 1)
        self.assertEqual(文本表.objects.filter(文本資料='落翼仔').count(), 2)

    @patch('臺灣言語資料庫.資料模型.外語表.加資料')
    def test_外語資料(self, 加資料mocka):
        self.匯入工具.匯入檔案(self._提yaml資料('xls整理.yaml'))
        加資料mocka.assert_called_once_with({
            '收錄者': 來源表.objects.get(名='系統管理者'),
            '來源': {'名': '教育部閩南語辭典'},
            '版權': '姓名標示-禁止改作 3.0 台灣',
            '種類': '語句',
            '著作年': '2015',
            '著作所在地': '臺灣',
            '語言腔口': '閩南語',
            '外語語言': '華語',
            '外語資料': '鼓膜破了。',
        })

    @patch('臺灣言語資料庫.資料模型.外語表.翻母語')
    def test_翻母語(self, 翻母語mocka):
        self.匯入工具.匯入檔案(self._提yaml資料('xls整理.yaml'))
        翻母語mocka.assert_called_once_with({
            '收錄者': 來源表.objects.get(名='系統管理者'),
            '來源': {'名': '教育部閩南語辭典'},
            '版權': '姓名標示-禁止改作 3.0 台灣',
            '種類': '語句',
            '著作年': '2015',
            '著作所在地': '臺灣',
            '語言腔口': '閩南語',
            '文本資料': '耳鏡破去矣。',
            '屬性': {'音標': 'hinn7-kiann3 phua3-0khi3-0ah4 .'}
        })

    def test_翻母語語料(self):
        self.匯入工具.匯入檔案(self._提yaml資料('xls整理.yaml'))
        self.assertEqual(文本表.objects.filter(文本資料='耳鏡破去矣。').count(), 1)

    def _提yaml資料(self, 檔名):
        return join(dirname(abspath(__file__)), '資料', 檔名)
