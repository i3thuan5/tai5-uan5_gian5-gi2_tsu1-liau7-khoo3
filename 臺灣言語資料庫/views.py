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

def 頭頁(request):
# 	編修.objects.create().save()
	文字a=文字(年代=22)
	文字a.save()
	揣著資料 = 編修.objects.order_by('流水號')
	字串=''
	for 資料 in 揣著資料:
		字串=str(資料.__dict__)
		print(資料.文字)
		for 文字逝 in 資料.文字.all():
			print(文字逝.年代)
		print(資料.__dict__)
	return HttpResponse(字串)