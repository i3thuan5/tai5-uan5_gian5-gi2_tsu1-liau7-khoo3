# 臺灣言語資料庫

[![Build Status](https://travis-ci.org/sih4sing5hong5/tai5-uan5_gian5-gi2_tsu1-liau7-khoo3.svg?branch=master)](https://travis-ci.org/sih4sing5hong5/tai5-uan5_gian5-gi2_tsu1-liau7-khoo3)
[![Coverage Status](https://coveralls.io/repos/sih4sing5hong5/tai5-uan5_gian5-gi2_tsu1-liau7-khoo3/badge.svg)](https://coveralls.io/r/sih4sing5hong5/tai5-uan5_gian5-gi2_tsu1-liau7-khoo3)

提供收集語料介面的django函式庫

希望能方便語言學習、研究。

感謝您的使用與推廣～～勞力！承蒙！

##安裝方法
設置環境
```bash
sudo apt-get install -y python3 python-virtualenv lib
virtualenv venv --python python3 # 設置環境檔
```
載入環境，每次使用前必須執行
```bash
. venv/bin/activate 
```
安裝
```bash
pip install tai5-uan5_gian5-gi2_tsu1-liau7-khoo3
pip install Django git+https://github.com/conrado/libavwrapper@6409123ee24df823a5ee0bac7a08043e6b317721#egg=libavwrapper
```
開發
```
bash 走試驗.sh
```

## 使用Postgres

### 在Ubuntu上快速設定
```bash
sudo apt-get install -y libpq-dev python3-dev postgresql postgresql-contrib
sudo -u postgres createuser --superuser $USER
sudo -u postgres createdb $USER
psql
	\password Taiwanese(可自訂)
pip install psycopg2
```
在的`setting.py`改
```python3
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '$USER', # Linux's username
        'USER': '$USER', # Linux's username
        'PASSWORD': 'Taiwanese', # 剛輸入的密碼
        'HOST': 'localhost',
        'PORT': '',
    }
}
```
最後初使化資料庫
```
python manage.py migrate
```

### 清掉全部資料
使用`psql`，然後輸入
```
drop schema public cascade;
create schema public;
```
愛記得閣初使化資料庫
```
python manage.py migrate
```

## 授權說明
本程式乃自由軟體，您必須遵照SocialCalc設計的通用公共授權（Common Public Attribution License, CPAL)來修改和重新發佈這一程式，詳情請參閱條文。授權大略如下，若有歧異，以授權原文為主：

	１．得使用、修改、複製並發佈此程式碼，且必須以通用公共授權發行；
	２．任何以程式碼衍生的執行檔或網路服務，必須公開該程式碼；
	３．將此程式的原始碼當函式庫引用入商業軟體，且不需公開非關此函式庫的任何程式碼

此開放原始碼、共享軟體或說明文件之使用或散佈不負擔保責任，並拒絕負擔因使用上述軟體或說明文件所致任何及一切賠償責任或損害。

緣起於本土文化推廣與傳承，非常歡迎各界用於商業軟體，但希望在使用之餘，能夠提供建議、錯誤回報或修補，回饋給這塊土地。


## 其他專案
* [臺灣言語工具](https://github.com/sih4sing5hong5/tai5-uan5_gian5-gi2_kang1-ku7)
* [臺灣言語平臺](https://github.com/sih4sing5hong5/tai5-uan5_gian5-gi2_phing5-thai5)。
