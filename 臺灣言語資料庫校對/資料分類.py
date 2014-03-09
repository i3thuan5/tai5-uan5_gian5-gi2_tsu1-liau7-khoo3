from django.db.models import Q
from 臺灣言語資料庫.模型 import 編修
from 臺灣言語資料庫.腔口資訊 import 閩南語
from 臺灣言語資料庫.欄位資訊 import 愛改
from 臺灣言語資料庫.欄位資訊 import 猶未檢查

class 資料分類:
	def 揣出檢查字音的資料(self, 腔, 來源):
		if len(來源) == 0:
			return []
		公家 = 編修.objects.filter(狀況 = 猶未檢查,結果__isnull=True).\
			filter(文字__腔口__startswith = 腔).filter(文字__組合 = '')
		要求 = Q(文字__來源 = 來源[0])
		for 源 in 來源[1:]:
			要求 = 要求 | Q(文字__來源 = 源)
		標準資料 = 公家.filter(要求)
		愛檢查的資料 = 公家.filter(~要求)
		return (標準資料, 愛檢查的資料)
	def 揣出愛改的資料(self):
		return 編修.objects.filter(種類 = '文字', 狀況 = 愛改)
