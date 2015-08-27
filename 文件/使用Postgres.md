# 使用Postgres

## 在Ubuntu14.04/Mint17上快速設定環境
```bash
sudo apt-get install -y libpq-dev python3-dev postgresql postgresql-contrib
sudo -u postgres createuser --superuser $USER
sudo -u postgres createdb $USER
psql
	\password Taiwanese(可自訂)
```

## Django專案設定
```
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
