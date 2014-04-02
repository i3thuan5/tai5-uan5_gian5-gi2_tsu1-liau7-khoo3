# -*- coding: utf-8 -*-
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
from 臺灣言語資料庫.欄位資訊 import 免改
from 臺灣言語資料庫.欄位資訊 import 愛改
from 臺灣言語工具.字詞組集句章.基本元素.公用變數 import 標點符號
from 臺灣言語資料庫.欄位資訊 import 標準
from 臺灣言語資料庫.欄位資訊 import 免檢查
from django.db.models import Count
import Pyro4
from 臺灣言語工具.字詞組集句章.解析整理.物件譀鏡 import 物件譀鏡
import sys
import traceback
from 臺灣言語工具.字詞組集句章.解析整理.轉物件音家私 import 轉物件音家私
from 臺灣言語工具.字詞組集句章.音標系統.閩南語.臺灣閩南語羅馬字拼音 import 臺灣閩南語羅馬字拼音
from 臺灣言語工具.字詞組集句章.解析整理.詞物件網仔 import 詞物件網仔
from 臺灣言語資料庫校對.表格 import 文字校對表格
from 臺灣言語資料庫.欄位資訊 import 改過
from 臺灣言語資料庫.欄位資訊 import 愛查
from 臺灣言語資料庫.欄位資訊 import 外來詞
from 臺灣言語資料庫.欄位資訊 import 人工校對
from 臺灣言語資料庫.腔口資訊 import 國語
from django.db.models import F
from 臺灣言語資料庫.欄位資訊 import 文字組合符號

__資料分類 = 資料分類()
__分析器 = 拆文分析器()
__篩仔 = 字物件篩仔()
__網仔 = 詞物件網仔()
__譀鏡 = 物件譀鏡()

def 揣出一字全羅(request):
# 	編修.objects.create().save()
# 	文字a=文字(年代=22)
# 	文字a.save()
# 	print(文字a.流水號)
# 	關係.objects.create(甲流水號=文字a.流水號,
# 					乙流水號=文字a.流水號,)
	全部資料 = 編修.objects.filter(文字__型體=F('文字__音標'))\
		.filter(文字__型體__regex='.*[0-9]')\
		.exclude(文字__型體__regex='.*[0-9].*[0-9]').order_by('流水號')
	有改資料=[]
	for 一字編修 in 全部資料[:]:
		參考語句 = __資料分類.揣出有這文字的語句(閩南語, 一字編修.流水號)
# 		print(參考語句.count())
		if 參考語句.count()<=1:
			continue
		一字編修.狀況 = 愛改
		一字編修.校對 = None
		一字編修.save()
		有改資料.append(一字編修)
		原本流水號組合 = 文字組合符號 + str(一字編修.流水號) + 文字組合符號
		for 參考一句 in 參考語句[1:]:
			複製 = 文字.objects.get(流水號=一字編修.流水號)
			複製.pk = None
			複製.save()
			新編修資料 = 複製.編修
			新編修資料.狀況 = 愛改
			新編修資料.save()
			複製流水號組合 = 文字組合符號 + str(新編修資料.流水號) + 文字組合符號
# 			print(參考一句.組合)
			參考一句.組合=參考一句.組合.replace(原本流水號組合,複製流水號組合)
			參考一句.save()
			print(原本流水號組合,複製流水號組合,)
# 		break
	版 = loader.get_template('臺灣言語資料庫校對/最近改的資料.html')
	文 = RequestContext(request, {
		'全部資料': 有改資料[:100],
	})
	return HttpResponse(版.render(文))
