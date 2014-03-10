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

__資料分類 = 資料分類()
def 最近改的資料(request):
# 	編修.objects.create().save()
# 	文字a=文字(年代=22)
# 	文字a.save()
# 	print(文字a.流水號)
# 	關係.objects.create(甲流水號=文字a.流水號,
# 					乙流水號=文字a.流水號,)
	全部資料 = 編修.objects.exclude(狀況='正常').order_by('-修改時間')[:100]
	版 = loader.get_template('臺灣言語資料庫校對/最近改的資料.html')
	文 = RequestContext(request, {
		'全部資料': 全部資料,
	})
	return HttpResponse(版.render(文))
def 定教育部辭典做標準(request):
	來源 = ['教育部臺灣閩南語常用詞辭典', '駱嘉鵬老師對應表']
	猶未設的標準資料 = __資料分類.揣出指定來源準備做檔準(閩南語, 來源=來源)
	for 猶未設 in 猶未設的標準資料:
		猶未設.狀況 = 標準
		猶未設.save()
	return HttpResponse("設{}做標準矣".format(來源))
def 國語改免檢查(request):
	國語資料 = __資料分類.揣國語猶未檢查()
	for 國語文字 in 國語資料:
		國語文字.狀況 = 免檢查
		國語文字.save()
	return HttpResponse("國語攏改免檢查矣")
		
def 檢查猶未標的資料(request):
	愛檢查的資料 = __資料分類.揣出檢查字音的資料(閩南語)
	分析器 = 拆文分析器()
	篩仔 = 字物件篩仔()
	網仔 = 詞物件網仔()
	Pyro4.config.SERIALIZER = 'pickle'
	閩南語標音 = Pyro4.Proxy("PYRONAME:閩南語標音")
	家私 = 轉物件音家私()
	音標工具 = 臺灣閩南語羅馬字拼音
	for 愛檢查 in 愛檢查的資料[:]:
		文 = 愛檢查.文字.first()
		try:
			if 文.型體 in 標點符號 and 文.音標 in 標點符號:
				物件 = 分析器.產生對齊字(文.型體, 文.音標)
			else:
				物件 = 分析器.產生對齊組(文.型體, 文.音標)
		except:
			print('有問題', 愛檢查.流水號, 文.型體, 文.音標)
			continue
		try:
			正規物件 = 家私.轉做標準音標(音標工具, 物件)
		except:
			資料攏著 = False
		else:
			資料攏著 = True
			字陣列 = 篩仔.篩出字物件(正規物件)
			for 字物件 in 字陣列:
				詞物件 = 分析器.建立詞物件('')
				詞物件.內底字.append(字物件)
				查著的資料 = 閩南語標音.物件斷詞標音(詞物件)
				查著的句物件 = 查著的資料[0]
				詞陣列 = 網仔.網出詞物件(查著的句物件)
# 				print('查著的資料',查著的資料[0].內底集[0].內底組[0].內底詞[0].屬性)
# 				print('詞陣列',詞陣列[0].屬性)
				if '無佇辭典' in 詞陣列[0].屬性 and 詞陣列[0].屬性['無佇辭典']:
					資料攏著 = False
					break
		if 資料攏著:
			愛檢查.狀況 = 免改
		else:
			愛檢查.狀況 = 愛改
		愛檢查.save()
		print(物件, 資料攏著)
	版 = loader.get_template('臺灣言語資料庫/全部資料.html')
	文 = RequestContext(request, {
		'全部資料': 愛檢查的資料[:10],
	})
	return HttpResponse(版.render(文))
def 改愛改的資料(request):
	愛改資料 = __資料分類.揣出愛改的資料().first()
	參考語句 = __資料分類.揣出有這文字的語句(愛改資料.流水號).first()
	Pyro4.config.SERIALIZER = 'pickle'
	閩南語標音 = Pyro4.Proxy("PYRONAME:閩南語標音")
	try:
		建議結果物件 = 閩南語標音.語句斷詞標音(參考語句.音標)
	except Exception as 錯誤:
		print(錯誤)
 		
# 		錯誤.printStackTrace()
		raise 錯誤
	譀鏡 = 物件譀鏡()
	校對表格 = 文字校對表格(instance=愛改資料.文字.first())
	文 = RequestContext(request, {
		'愛改資料': 愛改資料,
		'參考語句':參考語句,
		'建議結果':譀鏡.看型(建議結果物件[0], 物件分詞符號=' '),
		'校對表格':校對表格,
		'動作':[改過, 愛查, 外來詞],
		})
	版 = loader.get_template('臺灣言語資料庫校對/愛改.html')
	return HttpResponse(版.render(文))
def 檢查改的資料(request, pk):
	資料 = ''
	if request.method == 'POST':
		校對表格 = 文字校對表格(request.POST)
		資料 = str(dict(request.POST))
		print(request.POST, 'request.POST')
		print(request.POST['型體'], 'request.POST')
# 		if 校對表格.is_valid():
# 			文章 = 文章表格.save()
# 			文章.自動斷詞()
# 			return redirect('改國語斷詞', pk=文章.pk)
# 	else:
	return HttpResponse("資料:" + 資料)
def 閩南語狀況(request):
	閩南語資料 = 編修.objects.filter(文字__腔口__startswith=閩南語)\
		.values('狀況').annotate(數量=Count('狀況')).order_by()
	文 = RequestContext(request, {
		'閩南語': 閩南語資料,
		})
	版 = loader.get_template('臺灣言語資料庫校對/閩南語狀況.html')
	return HttpResponse(版.render(文))
	
if __name__ == '__main__':
	參考語句 = 'Obama tua7-sing3 bi2-kok4 thau5-tsit8-ui7 oo1-lang5 tsong2-thong2 '
	閩南語標音 = Pyro4.Proxy("PYRONAME:閩南語標音")
	建議結果物件 = 閩南語標音.語句斷詞標音(參考語句)
