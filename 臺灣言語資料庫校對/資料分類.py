from django.db.models import Q
from 臺灣言語資料庫.models import 編修
from 臺灣言語工具.資料庫.欄位資訊 import 閩南語

class 資料分類:
	def 揣出檢查字音的資料(腔, 來源):
		if len(來源) == 0:
			return []
		公家= 編修.objects.filter(版本='正常').\
			filter(文字__組合__startswith=閩南語).filter(文字__組合='')
		要求 = Q(文字__來源=來源[0])
		for 源 in 來源[1:]:
			要求 = 要求 | Q(文字__來源=源)	
		標準資料 = 公家.filter(要求)
		愛檢查的資料 = 公家.filter(~要求)
		return (標準資料, 愛檢查的資料)
	def 揣出愛改的資料():
		return 編修.objects.get(狀況='愛改')
