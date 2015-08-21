# 臺灣言語說明文件

## 專案
* [臺灣言語工具](https://github.com/sih4sing5hong5/tai5-uan5_gian5-gi2_kang1-ku7)
  * 母語parser、寫法轉換、…功能。
  * 翻譯、語音辨識、語音合成等工具整合。
* [臺灣言語資料庫](https://github.com/sih4sing5hong5/tai5-uan5_gian5-gi2_tsu1-liau7-khoo3)
  * 母語資料存放規範
* [臺灣言語服務](https://github.com/sih4sing5hong5/tai5-uan5_gian5-gi2_hok8-bu7)
  * `臺灣言語資料庫`的套件
  * 結果`臺灣言語工具`，做好自動化翻譯、語音合成等功能
  * 提供Web-based的服務
* [臺灣言語平臺](https://github.com/sih4sing5hong5/tai5-uan5_gian5-gi2_phing5-thai5)。
  * 修改`臺灣言語資料庫`的網頁介面

## 編專案
```
pip install recommonmark
cd docs
make html
```

### 臺灣言語資料庫

#### 資料關係

#### 匯入資料

#### 輸出資料
```
from 臺灣言語資料庫.輸出 import 資料輸出工具
語料 = 資料輸出工具()
語料.輸出翻譯語料(self.目錄)
```