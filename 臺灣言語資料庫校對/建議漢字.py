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

Pyro4.config.SERIALIZER = 'pickle'

class 建議漢字:
	閩南語唸國語 = '閩南語唸國語'
	參考語句音轉漢字 = '參考語句音轉漢字'
	原本字 = '原本字'
	__資料分類 = 資料分類()
	__分析器 = 拆文分析器()
	__篩仔 = 字物件篩仔()
	__網仔 = 詞物件網仔()
	__譀鏡 = 物件譀鏡()
	__閩南語標音 = Pyro4.Proxy("PYRONAME:閩南語標音")
	def 問建議(self, 編修資料):
		參考語句 = self.__資料分類.揣出有這文字的語句(閩南語, 編修資料.流水號).first()
		參考國語 = self.__資料分類.揣腔口近義(國語, 參考語句.流水號.流水號).first()
		文字資料 = 編修資料.文字.first()
		參考國語文字 = 參考國語.文字.first()
		Pyro4.config.SERIALIZER = 'pickle'
		try:
			建議結果物件 = self.__閩南語標音.語句斷詞標音(參考語句.音標)
			閩南語唸國語 = self.__閩南語標音.語句斷詞標音(參考國語文字.型體)
		except Exception as 錯誤:
			print(錯誤)
			raise 錯誤
		譀鏡 = 物件譀鏡()
		詞物件 = self.__分析器.建立詞物件('')
		建議結果來源 = '無'
		try:
			物件 = self.__分析器.產生對齊組(文字資料.型體, 文字資料.音標)
		except:
			物件 = self.__分析器.產生對齊字(文字資料.型體, 文字資料.音標)
		字陣列 = self.__篩仔.篩出字物件(物件)
		詞物件.內底字 = self.揣建議物件的字陣列(閩南語唸國語[0], 字陣列)
		建議結果來源 = self.閩南語唸國語
		if 詞物件.內底字 == []:
			詞物件.內底字 = self.揣建議物件的字陣列(建議結果物件[0], 字陣列)
			建議結果來源 = self.參考語句音轉漢字
		if 詞物件.內底字 == []:
			print('字陣列內揣無，可能是外來詞')
			建議結果來源 = self.原本字
			詞物件.內底字 = 字陣列
# 		校對表格 = 文字校對表格(
# 			initial={'型體':譀鏡.看型(詞物件).replace('台', '臺')}, instance=文字資料)
		參考語句音轉漢字 = 譀鏡.看型(建議結果物件[0], 物件分詞符號=' ')
		閩南語唸參考國語文字 = 譀鏡.看音(閩南語唸國語[0])
		建議結果 = 譀鏡.看型(詞物件).replace('台', '臺')
		return (文字資料, 參考語句, 參考語句音轉漢字, 參考國語文字, 閩南語唸參考國語文字, 建議結果, 建議結果來源)
# 		文 = RequestContext(request, {
# 			'編修資料': 編修資料,
# 			'參考語句':參考語句,
# 			'建議結果':譀鏡.看型(建議結果物件[0], 物件分詞符號=' '),  # 參考句轉漢字
# 			'參考國語文字':參考國語文字,
# 			'閩南語唸國語':譀鏡.看音(閩南語唸國語[0]),
# 			'校對表格':校對表格,
# 			'動作':[改過, 愛查, 外來詞, 字典無收著],
# 			})
	def 揣建議物件的字陣列(self, 建議物件, 字陣列):
		建議字陣列 = self.__篩仔.篩出字物件(建議物件)
		return self.揣建議字陣列的字陣列(建議字陣列, 字陣列)
	def 揣建議字陣列的字陣列(self, 建議字陣列, 字陣列):
		所在 = self.建議字陣列有包含字陣列(建議字陣列, 字陣列)
		if 所在 == None:
			return []
		return 建議字陣列[所在:所在 + len(字陣列)]
	def 建議字陣列有包含字陣列(self, 建議字陣列, 字陣列):
# 		print(建議字陣列, 字陣列)
		for 參考字物件所在 in range(len(建議字陣列) - len(字陣列) + 1):
			對著 = True
			for 字物件所在 in range(len(字陣列)):
				if 建議字陣列[參考字物件所在 + 字物件所在].音 != 字陣列[字物件所在].音:
					對著 = False
			if 對著:
				return 參考字物件所在
		return None
