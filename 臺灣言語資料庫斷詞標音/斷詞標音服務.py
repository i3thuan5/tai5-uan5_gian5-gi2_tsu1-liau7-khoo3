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
import Pyro4
from 臺灣言語資料庫斷詞標音.閩南語標音整合 import 閩南語標音整合
'''
from 臺灣言語資料庫斷詞標音.斷詞標音服務 import 斷詞標音服務
斷詞標音服務()
'''
__資料分類 = 資料分類()
def 斷詞標音服務():
	Pyro4.config.SERIALIZERS_ACCEPTED.add('pickle')
	閩南語標音 = 閩南語標音整合(閩南語,型音辭典)
	Pyro4.Daemon.serveSimple(
	{
		閩南語標音: "內部自動標音"
	}, ns = True)
# 	標準資料, 愛檢查的資料 = __資料分類.揣出檢查字音的資料(閩南語)
# 	分析器 = 拆文分析器()
# 	篩仔 = 字物件篩仔()
# 	辭典 = 型音辭典(4)
# 	for 標準 in 標準資料[:]:
# 		文 = 標準.文字.first()
# 		組物件 = 分析器.產生對齊組(文.型體, 文.音標)
# 		for 詞物件 in 組物件.內底詞:
# 			辭典.加詞(詞物件)
# 		字陣列 = 篩仔.篩出字物件(組物件)
# 		for 字物件 in 字陣列:
# 			詞物件 = 分析器.建立詞物件('')
# 			詞物件.內底字.append(字物件)
# 			辭典.加詞(詞物件)