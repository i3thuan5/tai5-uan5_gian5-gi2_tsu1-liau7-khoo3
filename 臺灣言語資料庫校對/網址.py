from django.conf.urls import patterns, url

from 臺灣言語資料庫校對.介面 import 最近改的資料
from 臺灣言語資料庫校對.介面 import 改愛改的資料
from 臺灣言語資料庫校對.介面 import 檢查改的資料
from 臺灣言語資料庫校對.介面 import 檢查猶未標的資料
from 臺灣言語資料庫校對.介面 import 定教育部辭典做標準
from 臺灣言語資料庫校對.介面 import 國語改免檢查
from 臺灣言語資料庫校對.介面 import 閩南語狀況
from 臺灣言語資料庫校對.介面 import 自動改有國語語句的資料
from 臺灣言語資料庫校對.其他介面 import 揣出一字全羅

urlpatterns = patterns('',
	url(r'^閩南語狀況$', 閩南語狀況, name='閩南語狀況'),
	
	url(r'^改愛改的資料$', 改愛改的資料, name='改愛改的資料'),
	url(r'^檢查改的資料/(?P<pk>\d+)$', 檢查改的資料, name='檢查改的資料'),
	
	url(r'^定教育部辭典做標準$', 定教育部辭典做標準, name='定教育部辭典做標準'),
	url(r'^檢查猶未標的資料$', 檢查猶未標的資料, name='檢查猶未標的資料'),
	url(r'^國語改免檢查$', 國語改免檢查, name='國語改免檢查'),
	url(r'^自動改有國語語句的資料$', 自動改有國語語句的資料, name='自動改有國語語句的資料'),
	
	url(r'^揣出一字全羅$', 揣出一字全羅, name='揣出一字全羅'),
	url(r'^.*$', 最近改的資料, name='最近改的資料'),
)