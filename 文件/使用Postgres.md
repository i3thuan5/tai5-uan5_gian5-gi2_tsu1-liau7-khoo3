# 使用Postgres

## 在Ubuntu14.04/Mint17上快速設定環境
設定資料庫使用者和密碼
```bash
sudo -u postgres createuser --superuser $USER
sudo -u postgres createdb $USER
psql
	\password
```

## 在MAC上快速設定環境
設定資料庫使用者和密碼
```bash
psql
	\password
```

## Django專案設定
在`setting.py`改
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

## 初使化資料庫
```
python manage.py migrate
```

## 資料備份
匯出做檔案
```bash
pg_dump $USER -O | gzip > 臺灣言語資料庫`date +%m%d`.sql.gz
```
檔案匯入
```bash
zcat 臺灣言語資料庫20150903.sql.gz | psql $USER
```

## 清掉全部資料
使用`psql`，然後輸入
```
drop schema public cascade;
create schema public;
```
愛記得閣初使化資料庫
```
python manage.py migrate
```
