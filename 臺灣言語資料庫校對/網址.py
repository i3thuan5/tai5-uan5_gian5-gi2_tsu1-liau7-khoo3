from django.conf.urls import patterns, url

from 臺灣言語資料庫校對.介面 import 最近改的資料
from 臺灣言語資料庫校對.介面 import 改愛改的資料
from 臺灣言語資料庫校對.介面 import 檢查猶未標的資料
from 臺灣言語資料庫校對.介面 import 定教育部辭典做標準

urlpatterns = patterns('',
	url(r'^改愛改的資料$', 改愛改的資料, name='改愛改的資料'),
	url(r'^檢查猶未標的資料$', 檢查猶未標的資料, name='檢查猶未標的資料'),
	url(r'^定教育部辭典做標準$', 定教育部辭典做標準, name='定教育部辭典做標準'),
	url(r'^.*$', 最近改的資料, name='最近改的資料'),
)