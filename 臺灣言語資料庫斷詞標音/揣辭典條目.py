"""
著作權所有 (C) 民國102年 意傳文化科技
開發者：薛丞宏
網址：http://意傳.台灣
語料來源：請看各資料庫內說明

本程式乃自由軟體，您必須遵照SocialCalc設計的通用公共授權（Common Public Attribution License, CPAL)來修改和重新發佈這一程式，詳情請參閱條文。授權大略如下，若有歧異，以授權原文為主：
	１．得使用、修改、複製並發佈此程式碼，且必須以通用公共授權發行；
	２．任何以程式碼衍生的執行檔或網路服務，必須公開該程式碼；
	３．將此程式的原始碼當函式庫引用入商業軟體，且不需公開非關此函式庫的任何程式碼

此開放原始碼、共享軟體或說明文件之使用或散佈不負擔保責任，並拒絕負擔因使用上述軟體或說明文件所致任何及一切賠償責任或損害。

臺灣言語工具緣起於本土文化推廣與傳承，非常歡迎各界用於商業軟體，但希望在使用之餘，能夠提供建議、錯誤回報或修補，回饋給這塊土地。

感謝您的使用與推廣～～勞力！承蒙！
"""
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
from 臺灣言語資料庫.欄位資訊 import 無仝言語層
from 臺灣言語資料庫.模型 import 關係
from 臺灣言語資料庫.欄位資訊 import 字詞
from 臺灣言語資料庫.欄位資訊 import 會使提來用

class 揣辭典條目():
	def __init__(self):
		self.要求 = Q(狀況=會使提來用)
		for 用 in 會使提來用[1:]:
			self.要求 = self.要求 | Q(狀況=用)
	def 揣言語層的字詞(self, 腔口, 語言層):
		乙流水號 = '乙流水號'
		資料 = 關係.objects.values(乙流水號).distinct()\
			.filter(乙對甲的關係類型=無仝言語層, 關係性質=語言層)\
			.order_by(乙流水號)
		流水號集 = set()
		for 關 in 資料:
			流水號集.add(關[乙流水號])
		return 流水號集
	def 揣腔口資料(self, 腔口):
# 	文字.objects.values_list('型體', '音標')\
		return 編修.objects.filter(self.要求).filter(結果__isnull=True)\
			.filter(文字__腔口__contains=腔口)
	def 揣腔口字詞資料(self, 腔口):
# 		return 文字.objects.values_list('型體', '音標')\
		return 編修.objects.filter(self.要求).filter(結果__isnull=True)\
			.filter(腔口__contains=腔口, 種類=字詞)
