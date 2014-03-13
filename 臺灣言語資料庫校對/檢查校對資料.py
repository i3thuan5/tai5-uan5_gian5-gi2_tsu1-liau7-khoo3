import Pyro4
from 臺灣言語資料庫.模型 import 編修
from 臺灣言語資料庫.模型 import 文字
from 臺灣言語資料庫.模型 import 關係
from 臺灣言語資料庫.模型 import 演化
from 臺灣言語資料庫校對.資料分類 import 資料分類
from 臺灣言語資料庫.腔口資訊 import 閩南語
from 臺灣言語工具.斷詞.型音辭典 import 型音辭典
from 臺灣言語工具.字詞組集句章.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.字詞組集句章.解析整理.字物件篩仔 import 字物件篩仔
from 臺灣言語資料庫.欄位資訊 import 免改
from 臺灣言語資料庫.欄位資訊 import 愛改
from 臺灣言語工具.字詞組集句章.基本元素.公用變數 import 標點符號
from 臺灣言語資料庫.欄位資訊 import 標準
from 臺灣言語資料庫.欄位資訊 import 免檢查
from 臺灣言語工具.字詞組集句章.解析整理.物件譀鏡 import 物件譀鏡
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

Pyro4.config.SERIALIZER = 'pickle'

class 校對資料整理:
	__資料分類 = 資料分類()
	__分析器 = 拆文分析器()
	__篩仔 = 字物件篩仔()
	__網仔 = 詞物件網仔()
	__譀鏡 = 物件譀鏡()
	__建議漢字 = 建議漢字()
	__閩南語標音 = Pyro4.Proxy("PYRONAME:閩南語標音")
	def 加校對資料(self, 編修資料, 動作, 型體, 音標):
		if 動作 not in [改過, 愛查, 外來詞, 字典無收著]:
			return "動作有問題"
		愛處理的物件 = 編修.objects.get(流水號=編修資料.流水號)
		if 愛處理的物件.狀況 != 愛改:
			return "這个詞有人改過矣"
		字典無收著有改 = False
		if 動作 in [字典無收著]:
			愛處理的物件文字 = 愛處理的物件.文字.first()
			if 愛處理的物件文字.型體 != 型體 or 愛處理的物件文字.音標 != 音標:
				字典無收著有改 = True
		if not 字典無收著有改 and 動作 in [愛查, 外來詞, 字典無收著]:
			愛處理的物件.狀況 = 動作
			愛處理的物件.save()
			return None
		攏佇辭典 = True
		try:
			物件 = self.__分析器.產生對齊組(型體, 音標)
		except Exception as 問題:
			print(問題)
			攏佇辭典 = False
		else:
			攏佇辭典 = self.是毋是攏佇辭典內底(物件)
		if 攏佇辭典 or 字典無收著有改:
			原來文字資料 = 愛處理的物件.文字.first()
			文字資料 = 原來文字資料.改過閣加結果()
			文字資料.來源 = 人工校對
			文字資料.型體 = self.__譀鏡.看型(物件)
			文字資料.音標 = self.__譀鏡.看音(物件)
			文字資料.save()
			新編修資料 = 文字資料.流水號
			if 動作 in [字典無收著]:
				新編修資料.狀況 = 動作
			else:
				新編修資料.狀況 = 人工校對
			新編修資料.save()
			return None
		else:
			return "「{}」「{}」無佇辭典".format(型體, 音標)

	def 是毋是攏佇辭典內底(self, 正規物件):
		查著的資料 = self.__閩南語標音.物件斷詞標音(正規物件)
		查著的句物件 = 查著的資料[0]
		詞陣列 = self.__網仔.網出詞物件(查著的句物件)
		for 詞物件 in 詞陣列:
			if '無佇辭典' in 詞物件.屬性 and 詞物件.屬性['無佇辭典']:
				print(詞物件, '無佇辭典')
				return False
		return True
