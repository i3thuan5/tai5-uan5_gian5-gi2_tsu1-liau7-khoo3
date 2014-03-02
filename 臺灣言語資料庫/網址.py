from django.conf.urls import patterns, url

from 臺灣言語資料庫.views import 頭頁

urlpatterns = patterns('',
	url(r'^.*$', 頭頁, name='頭頁'),
)