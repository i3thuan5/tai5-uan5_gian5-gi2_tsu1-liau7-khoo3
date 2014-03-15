from django.conf.urls import patterns, url
from 臺灣言語資料庫服務.服務 import 服務

__服務=服務()
urlpatterns = patterns('',
	url(r'^自動標音/(?P<查詢腔口>\.+)/(?P<查詢語句>\.+)$', __服務.自動標音, name='自動標音'),
)