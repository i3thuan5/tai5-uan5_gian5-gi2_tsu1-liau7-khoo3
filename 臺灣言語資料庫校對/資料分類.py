from django.db.models import Q
from 臺灣言語資料庫.模型 import 編修
from 臺灣言語資料庫.腔口資訊 import 閩南語
from 臺灣言語資料庫.欄位資訊 import 愛改
from 臺灣言語資料庫.欄位資訊 import 猶未檢查
from 臺灣言語資料庫.欄位資訊 import 標準
from 臺灣言語資料庫.模型 import 文字
from 臺灣言語資料庫.欄位資訊 import 語句
from 臺灣言語資料庫.欄位資訊 import 文字組合符號
from 臺灣言語資料庫.腔口資訊 import 國語

class 資料分類:
	def 揣出指定來源準備做檔準(self, 腔, 來源):
		if len(來源) == 0:
			return []
		公家 = 編修.objects.filter(狀況 = 猶未檢查, 結果__isnull = True).\
			filter(文字__腔口__startswith = 腔)
		要求 = Q(文字__來源 = 來源[0])
		for 源 in 來源[1:]:
			要求 = 要求 | Q(文字__來源 = 源)
		標準資料 = 公家.filter(要求)
		return 標準資料
	def 揣出檢查字音的資料(self, 腔):
		標準資料 = 編修.objects.filter(狀況 = 標準, 結果__isnull = True)
		愛檢查的資料 = 編修.objects.filter(狀況 = 猶未檢查, 結果__isnull = True).\
			filter(文字__腔口__startswith = 腔).filter(文字__組合 = '')
		return (標準資料, 愛檢查的資料)
	def 揣出愛改的資料(self):
		return 編修.objects.filter(種類 = '文字', 狀況 = 愛改)
	def 揣出有這文字的語句(self, 流水號):
		return 文字.objects.filter(種類 = 語句, 組合__contains = 文字組合符號 + str(流水號) + 文字組合符號)
	def 揣國語猶未檢查(self):
		return 編修.objects.filter(狀況 = 猶未檢查, 結果__isnull = True).\
				filter(文字__腔口__startswith = 國語)
