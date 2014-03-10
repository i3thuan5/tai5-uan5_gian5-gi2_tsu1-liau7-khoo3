from django.conf.urls import patterns, url

from 臺灣言語資料庫校對.介面 import 最近改的資料
from 臺灣言語資料庫校對.介面 import 改愛改的資料
from 臺灣言語資料庫校對.介面 import 檢查猶未標的資料
from 臺灣言語資料庫校對.介面 import 定教育部辭典做標準
from 臺灣言語資料庫校對.介面 import 國語改免檢查
from 臺灣言語資料庫校對.介面 import 閩南語狀況

urlpatterns = patterns('',
	url(r'^閩南語狀況$', 閩南語狀況, name='閩南語狀況'),
	url(r'^改愛改的資料$', 改愛改的資料, name='改愛改的資料'),
	url(r'^檢查猶未標的資料$', 檢查猶未標的資料, name='檢查猶未標的資料'),
	url(r'^定教育部辭典做標準$', 定教育部辭典做標準, name='定教育部辭典做標準'),
	url(r'^國語改免檢查$', 國語改免檢查, name='國語改免檢查'),
	url(r'^.*$', 最近改的資料, name='最近改的資料'),
)