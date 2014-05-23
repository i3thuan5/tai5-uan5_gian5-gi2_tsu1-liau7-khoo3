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
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.解析整理.字物件篩仔 import 字物件篩仔
from 臺灣言語資料庫.欄位資訊 import 免改
from 臺灣言語資料庫.欄位資訊 import 愛改
from 臺灣言語工具.基本元素.公用變數 import 標點符號
from 臺灣言語資料庫.欄位資訊 import 標準
from 臺灣言語資料庫.欄位資訊 import 免檢查
from django.db.models import Count
import Pyro4
from 臺灣言語工具.解析整理.物件譀鏡 import 物件譀鏡
import sys
import traceback
from 臺灣言語工具.解析整理.轉物件音家私 import 轉物件音家私
from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音 import 臺灣閩南語羅馬字拼音
from 臺灣言語工具.解析整理.詞物件網仔 import 詞物件網仔
from 臺灣言語資料庫校對.表格 import 文字校對表格
from 臺灣言語資料庫.欄位資訊 import 改過
from 臺灣言語資料庫.欄位資訊 import 愛查
from 臺灣言語資料庫.欄位資訊 import 外來詞
from 臺灣言語資料庫.欄位資訊 import 人工校對
from 臺灣言語資料庫.腔口資訊 import 國語
from 臺灣言語資料庫.欄位資訊 import 字典無收著
from 臺灣言語資料庫校對.建議漢字 import 建議漢字
from 臺灣言語資料庫校對.檢查校對資料 import 校對資料整理
from 臺灣言語資料庫.欄位資訊 import 電腦校對
from 臺灣言語資料庫.欄位資訊 import 會使提來用

__資料分類 = 資料分類()
__分析器 = 拆文分析器()
__篩仔 = 字物件篩仔()
__網仔 = 詞物件網仔()
__譀鏡 = 物件譀鏡()
__建議漢字 = 建議漢字()
__校對資料整理 = 校對資料整理()
Pyro4.config.SERIALIZER = 'pickle'
__閩南語標音 = Pyro4.Proxy("PYRONAME:閩南語標音")
class 主動校對:
	def __init__(self,):
		self.會使用 = Q(狀況 = 會使提來用[0])
		for 會使 in 會使提來用[1:]:
			self.會使用 = self.會使用 | Q(狀況 = 會使)
	def 鬥校對仝音的資料(self, 編修資料):
		音標 = 編修資料.文字.音標
		標準資料 = 編修.objects.values_list('文字__型體', '文字__音標').distinct()\
			.filter(self.會使用, 校對__isnull = True).filter(文字__音標 = 音標)
		無正確的 = 編修.objects.filter(校對__isnull = False).filter(文字__音標 = 音標)
		狀況 = None
		print ('無正確的', 無正確的.count())
		上尾校對流水號 = set()
		for 無著 in 無正確的:
			上尾校對 = 無著.揣上尾校對()
			if 上尾校對.狀況 in 會使提來用:
				上尾校對流水號.add(上尾校對.流水號)
				狀況 = 上尾校對.狀況
		參考資料 = set(標準資料)
		print(上尾校對流水號)
		if len(上尾校對流水號) > 0:
			上尾校對資料 = 編修.objects.values_list('文字__型體', '文字__音標').distinct()\
				.filter(流水號__in = 上尾校對流水號)
			參考資料 = 參考資料 | set(上尾校對資料)
			print(上尾校對資料.query)
			print(上尾校對資料.count())
		# [('言論',), ('言論',), ('言論',), ('言論',), ('言論',)]
		print(參考資料)
		if len(參考資料) != 1:
			print('{}有遮濟可能：{}'.format(音標, set(參考資料)))
			return None, None, None, None
		標準漢字, 標準音標 = 參考資料.pop()
		愛改的資料 = 編修.objects.filter(狀況 = 愛改)\
			.filter(文字__音標 = 音標)
		print('有幾筆會當改', 愛改的資料.count())
# 		print('愛改的資料, 標準漢字, 音標',愛改的資料, 標準漢字, 音標)
		return 愛改的資料, 標準漢字, 標準音標, 狀況

