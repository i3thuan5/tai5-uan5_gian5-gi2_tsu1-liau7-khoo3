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
from 臺灣言語資料庫.欄位資訊 import 字典無收著
from 臺灣言語資料庫校對.建議漢字 import 建議漢字
from 臺灣言語資料庫校對.檢查校對資料 import 校對資料整理
from 臺灣言語資料庫.欄位資訊 import 電腦校對
from 臺灣言語資料庫.欄位資訊 import 電腦算的結果
from django.views.generic.base import View
from 臺灣言語資料庫.欄位資訊 import 字詞

__資料分類 = 資料分類()
__分析器 = 拆文分析器()
__篩仔 = 字物件篩仔()
__網仔 = 詞物件網仔()
__譀鏡 = 物件譀鏡()
__建議漢字 = 建議漢字()
__校對資料整理 = 校對資料整理()
Pyro4.config.SERIALIZER = 'pickle'
__閩南語標音 = Pyro4.Proxy("PYRONAME:閩南語標音")


def 改愛改的資料(request):
	愛改資料 = __資料分類.揣出愛改的資料().first()
	if 愛改資料 != None:
		(愛改文字資料, 參考語句, 參考語句音轉漢字, \
			參考國語文字, 閩南語唸參考國語文字, 建議結果, 應該音標, 建議結果來源) = __建議漢字.問建議(愛改資料)
		校對表格 = 文字校對表格(
			initial = {'型體':建議結果, '音標':應該音標}, instance = 愛改文字資料)
		文 = RequestContext(request, {
			'愛改資料': 愛改資料,
			'參考語句':參考語句,
			'參考語句音轉漢字':參考語句音轉漢字,
			'參考國語文字':參考國語文字,
			'閩南語唸國語':閩南語唸參考國語文字,
			'校對表格':校對表格,
			'動作':[人工校對, 愛查, 外來詞, 字典無收著],
			})
	else:
		文 = RequestContext(request, {})
	版 = loader.get_template('臺灣言語資料庫校對/改愛改的資料.html')
	return HttpResponse(版.render(文))

def 檢查改的資料(request, pk):
	if request.method == 'POST':
		插入結果 = __校對資料整理.加校對資料(編修.objects.get(流水號 = pk),
			request.POST['動作'], 人工校對, request.POST['型體'], request.POST['音標'])
		if 插入結果 != None:
			return HttpResponse(插入結果)
	return redirect('改愛改的資料')

class 有問題愛改(View):
	無確定 = [人工校對, 免改, 電腦校對, 電腦算的結果, 愛查,
		外來詞, 愛改, 字典無收著]
	資料 = 編修.objects.filter(文字__種類 = 字詞)
	def get(self, request, *args, **kwargs):
		request.POST = {}
		request.POST['動作'] = '這愛改'
		request.POST['音標'] = ''
		a = []
		for b in a:
			request.POST['型體'] = b
			print(request.POST)
			self.改(request, *args, **kwargs)
		版 = loader.get_template('臺灣言語資料庫校對/有問題愛改.html')
		文 = RequestContext(request, {
		})
		return HttpResponse(版.render(文))
	def post(self, request, *args, **kwargs):
		self.改(request, *args, **kwargs)
		return self.get(request, *args, **kwargs)
	def 改(self, request, *args, **kwargs):
		if request.POST['動作'] == '這愛改':
			if request.POST['型體'].strip() != '' and request.POST['音標'].strip() != '':
				甲 = self.資料.filter(文字__型體__contains = request.POST['型體'],
					文字__音標__contains = request.POST['音標'])
			elif request.POST['型體'].strip() != '':
				甲 = self.資料.filter(文字__型體__contains = request.POST['型體'])
			elif request.POST['音標'].strip() != '':
				甲 = self.資料.filter(文字__音標__contains = request.POST['音標'])
			else:
				甲 = []
			for 資料 in 甲:
				if 資料.狀況 in self.無確定:
					資料.狀況 = 愛改
					資料.save()
				print(資料.狀況, 資料)
		elif request.POST['動作'] == '這愛改做':
			if request.POST['型體'].strip() != '' and request.POST['音標'].strip() != '':
				甲 = self.資料.filter(
					文字__型體__contains = request.POST['型體'],
					文字__音標__contains = request.POST['音標'])
			else:
				甲 = []
			if request.POST['改做型體'].strip() != '' and \
				request.POST['改做音標'].strip() != '':
				for 資料 in 甲:
					if 資料.狀況 in self.無確定:
						資料.狀況 = 愛改
						資料.save()
						文字資料 = 資料.文字
						__校對資料整理 = 校對資料整理()
						結果 = __校對資料整理.加校對資料(資料,
									電腦算的結果, 電腦算的結果,
									文字資料.型體.replace(
										request.POST['型體'].strip(),
										request.POST['改做型體'].strip()),
									文字資料.音標.replace(
										request.POST['音標'].strip(),
										request.POST['改做音標'].strip())

									)
						print(文字資料.型體, 文字資料.音標, '結果', 結果)
					print(資料.狀況, 資料)
		return
