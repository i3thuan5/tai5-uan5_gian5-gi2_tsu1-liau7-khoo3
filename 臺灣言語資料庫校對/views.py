from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.views import generic
from django.shortcuts import get_object_or_404
from django.http.response import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from 臺灣言語資料庫.models import 編修
from 臺灣言語資料庫.models import 文字
from 臺灣言語資料庫.models import 關係
from 臺灣言語資料庫.models import 演化
from 臺灣言語資料庫校對.資料分類 import 資料分類

__資料分類 = 資料分類()
def 最近改的資料(request):
# 	編修.objects.create().save()
# 	文字a=文字(年代=22)
# 	文字a.save()
# 	print(文字a.流水號)
# 	關係.objects.create(甲流水號=文字a.流水號,
# 					乙流水號=文字a.流水號,)
	全部資料 = 編修.objects.exclude(狀況='正常').order_by('-修改時間')[:100]
# 	全部資料 = 編修.objects.filter(狀況='正常').filter(文字__年代=22)
	版 = loader.get_template('臺灣言語資料庫/全部資料.html')
	文 = RequestContext(request, {
		'全部資料': 全部資料,
	})
	return HttpResponse(版.render(文))
def 檢查猶未標的資料():
	pass
def 改愛改的資料(request):
	愛改資料 = __資料分類.揣出愛改的資料()[:1]
	if 愛改資料.count() > 0:
		文 = RequestContext(request, {
			'愛改資料': 愛改資料[0],
		})
	else:
		文 = RequestContext(request)
	版 = loader.get_template('臺灣言語資料庫校對/愛改.html')
	return HttpResponse(版.render(文))
