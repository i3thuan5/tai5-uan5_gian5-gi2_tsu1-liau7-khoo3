import yaml
from 臺灣言語資料庫.資料模型 import 文本表
from 臺灣言語資料庫.資料模型 import 來源表
from 臺灣言語資料庫.資料模型 import 版權表


class 匯出入工具:

    def __init__(self):
        self.收錄者 = 來源表.objects.get_or_create(名='系統管理者')[0]

    def 匯入檔案(self, 檔名):
        with open(檔名) as 檔案:
            self._匯入物件(yaml.load(檔案))

    def _匯入物件(self, 資料物件):
        版權表.objects.get_or_create(版權=資料物件['版權'])
        self._遞迴匯入物件(
            資料物件,
            {'收錄者': self.收錄者},
            None
        )

    def _遞迴匯入物件(self, 資料物件, 原本狀態, 頂懸層語料):
        這馬狀態 = {}
        這馬狀態.update(原本狀態)
        下層物件陣列 = None
        for 欄位, 內容 in 資料物件.items():
            if 欄位 == '下層':
                下層物件陣列 = 內容
            else:
                這馬狀態[欄位] = 內容
        這層語料 = self._加入資料庫(這馬狀態, 頂懸層語料)
        if 下層物件陣列:
            for 下層物件 in 下層物件陣列:
                if '相關資料組' in 下層物件:
                    self._匯入相關資料陣列(下層物件['相關資料組'], 這馬狀態, 這層語料)
                else:
                    self._遞迴匯入物件(下層物件, 這馬狀態, 這層語料)

    def _匯入相關資料陣列(self, 相關資料陣列, 原本狀態, 頂懸層語料):
        for 相關資料 in 相關資料陣列:
            這馬狀態 = {}
            這馬狀態.update(原本狀態)
            這馬狀態.update(相關資料)
            頂懸層語料 = self._加入資料庫(這馬狀態, 頂懸層語料)

    def _加入資料庫(self, 這馬狀態, 頂懸層語料):
        if '文本資料' in 這馬狀態:
            if 頂懸層語料 is None:
                return 文本表.加資料(這馬狀態)
            else:
                return 頂懸層語料.校對做(這馬狀態)
        return 頂懸層語料
