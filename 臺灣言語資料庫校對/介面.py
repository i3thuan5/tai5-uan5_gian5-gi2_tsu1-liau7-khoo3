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
from 臺灣言語資料庫.模型 import 編修
from 臺灣言語資料庫.模型 import 文字
from 臺灣言語資料庫.模型 import 關係
from 臺灣言語資料庫.模型 import 演化
from 臺灣言語資料庫校對.資料分類 import 資料分類
from 臺灣言語資料庫.腔口資訊 import 閩南語
from itertools import chain
from 臺灣言語工具.斷詞.型音辭典 import 型音辭典
from 臺灣言語工具.字詞組集句章.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.字詞組集句章.解析整理.字物件篩仔 import 字物件篩仔

__資料分類 = 資料分類()
def 最近改的資料(request):
# 	編修.objects.create().save()
# 	文字a=文字(年代=22)
# 	文字a.save()
# 	print(文字a.流水號)
# 	關係.objects.create(甲流水號=文字a.流水號,
# 					乙流水號=文字a.流水號,)
	全部資料 = 編修.objects.exclude(狀況 = '正常').order_by('-修改時間')[:100]
	版 = loader.get_template('臺灣言語資料庫/全部資料.html')
	文 = RequestContext(request, {
		'全部資料': 全部資料,
	})
	return HttpResponse(版.render(文))
def 檢查猶未標的資料(request):
	標準資料, 愛檢查的資料=__資料分類.揣出檢查字音的資料(閩南語, 來源 = ['教育部臺灣閩南語常用詞辭典', '駱嘉鵬老師對應表'])
	全部資料=chain(標準資料[:10], 愛檢查的資料[:10])
	分析器 = 拆文分析器()
	篩仔=字物件篩仔()
	辭典 = 型音辭典(1)
	for 標準 in 標準資料:
		文=標準.文字.first()
		組物件=分析器.產生對齊組(文.型體,文.音標)
		字陣列=篩仔.篩出字物件(組物件)
		for 字物件 in 字陣列:
			詞物件=分析器.建立詞物件('')
			詞物件.內底字.append(字物件)
			辭典.加詞(詞物件)
	for 愛檢查 in 愛檢查的資料[:50]:
		文=愛檢查.文字.first()
		組物件=分析器.產生對齊組(文.型體,文.音標)
		字陣列 = 篩仔.篩出字物件(組物件)
		資料攏著=True
		for 字物件 in 字陣列:
			詞物件=分析器.建立詞物件('')
			詞物件.內底字.append(字物件)
			查著的資料 = 辭典.查詞(詞物件)
			if len(查著的資料[0]) == 0:
				資料攏著=False
				break
		print(組物件,資料攏著)
	版 = loader.get_template('臺灣言語資料庫/全部資料.html')
	文 = RequestContext(request, {
		'全部資料': 全部資料,
	})
	return HttpResponse(版.render(文))
def 改愛改的資料(request):
	愛改資料 = __資料分類.揣出愛改的資料()
	文 = RequestContext(request, {
		'愛改資料': 愛改資料.first(),
		})
	版 = loader.get_template('臺灣言語資料庫校對/愛改.html')
	return HttpResponse(版.render(文))
