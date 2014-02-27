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
from 臺灣言語工具.字詞組集句章.解析整理工具.拆文分析器 import 拆文分析器
from 臺灣言語工具.字詞組集句章.解析整理工具.轉物件音家私 import 轉物件音家私
from 臺灣言語工具.資料佮語料匯入整合.華語台語雙語語料庫系統.何澤政教會羅馬字音標 import 何澤政教會羅馬字音標
from 臺灣言語工具.資料庫.欄位資訊 import 文字組合符號
from 臺灣言語工具.資料庫.整合.整合入言語 import 加文字佮版本
from 臺灣言語工具.資料庫.欄位資訊 import 版本正常
from 臺灣言語工具.資料庫.欄位資訊 import 臺員
from 臺灣言語工具.資料庫.欄位資訊 import 國語臺員腔
from 臺灣言語工具.資料庫.欄位資訊 import 字詞
from 臺灣言語工具.資料庫.整合.整合入言語 import 加關係
from 臺灣言語工具.資料庫.欄位資訊 import 義近
from 臺灣言語工具.資料庫.整合.整合入言語 import 加文字佮組合佮版本
from 臺灣言語工具.資料庫.欄位資訊 import 語句
from 臺灣言語工具.資料庫.欄位資訊 import 閩南語
from 臺灣言語工具.資料庫.欄位資訊 import 章表冊
from 臺灣言語工具.資料佮語料匯入整合.華語台語雙語語料庫系統.對語料庫網站掠資料落來 import 對語料庫網站掠資料落來
from 臺灣言語工具.字詞組集句章.解析整理工具.文章粗胚工具 import 文章粗胚工具
from 臺灣言語工具.字詞組集句章.解析整理工具.物件譀鏡 import 物件譀鏡
from 臺灣言語工具.字詞組集句章.基本元素.公用變數 import 分字符號
from 臺灣言語工具.字詞組集句章.基本元素.公用變數 import 分詞符號
from 臺灣言語工具.資料庫.欄位資訊 import 會當替換

class 整合平行語料:
	華語台語雙語語料庫系統='華語台語雙語語料庫系統'
	def __init__(self):
		掠資料落來 = 對語料庫網站掠資料落來()
				
		self.粗胚工具 = 文章粗胚工具()
		self.分析器 = 拆文分析器()
		self.轉音家私 = 轉物件音家私()
		self.譀鏡 = 物件譀鏡()
		for 翻譯 in 掠資料落來.掠資料():
			文號 = 翻譯['文號']
			日期 = 翻譯['日期']
			國語 = 翻譯['國語']
			教羅 = 翻譯['閩南語']
			民國 = int(日期.split('-')[0]) - 1911
			教羅減號了 = self.粗胚工具.建立物件語句前處理減號(何澤政教會羅馬字音標, 教羅)
			教羅章物件 = self.分析器.建立章物件(教羅減號了)
			臺羅章物件 = self.轉音家私.轉做標準音標(何澤政教會羅馬字音標, 教羅章物件)
			音標 = self.譀鏡.看型(臺羅章物件, 物件分字符號=分字符號, 物件分詞符號=分詞符號)
			
# 			print(國語.split('\n')[3])
# 			print(教羅.split('\n')[3])
# 			print(音標.split('\n')[3])
			文章國語 = 國語.split('\n')
			文章音標 = 音標.split('\n')
			if len(文章國語) != len(文章音標):
				print('國語佮音標對無齊：{0}'.format(文號))
				continue
			
			國語文章流水號組合 = '#' + 文字組合符號
			閩南語文章流水號組合 = '#' + 文字組合符號
			配對臺語字陣列 = []
			配對臺語音陣列 = []
			for 一逝國語, 一逝音標 in zip(文章國語, 文章音標):
				語料, 流水號 = self.處理逝(民國, 一逝國語, 一逝音標.strip())
				配對臺語字陣列.append(語料[1].strip())
				配對臺語音陣列.append(語料[2].strip())
				國語句流水號組合, 閩南語句流水號組合 = 流水號
				國語文章流水號組合 += 國語句流水號組合 + 文字組合符號
				閩南語文章流水號組合 += 閩南語句流水號組合 + 文字組合符號
			國語文章流水號組合 += '#'
			閩南語文章流水號組合 += '#'
			配對臺語字文章 = '\n'.join(配對臺語字陣列)
			配對臺語音文章 = '\n'.join(配對臺語音陣列)
			國語流水號 = self.加文字佮組合佮版本(self.華語台語雙語語料庫系統, 章表冊, 國語臺員腔, 臺員, 民國,
				國語, '', 國語文章流水號組合, 版本正常)
			閩南語流水號 = self.加文字佮組合佮版本(self.華語台語雙語語料庫系統, 章表冊, 閩南語, 臺員, 民國,
				配對臺語字文章, 配對臺語音文章, 閩南語文章流水號組合, 版本正常)
			self.加關係(國語流水號, 閩南語流水號, 義近, 會當替換)
			self.加關係(閩南語流水號, 國語流水號, 義近, 會當替換)
			
	def 處理逝(self, 民國, 一逝國語, 一逝音標):
		國語句流水號組合 = '#' + 文字組合符號
		閩南語句流水號組合 = '#' + 文字組合符號
		國語詞 = 一逝國語.split()
		音標詞 = 一逝音標.split()
		if len(國語詞) != len(音標詞):
			臺語字詞 = 音標詞
		else:
			臺語字詞 = 國語詞
		配對臺語字陣列 = []
		for 國語詞, 臺語字, 臺語音 in zip(國語詞, 臺語字詞, 音標詞):
# 			國語集物件 = self.分析器.建立集物件(國語詞)
			try:
				self.分析器.產生對齊集(臺語字, 臺語音)
				配對臺語字 = 臺語字
			except:
				配對臺語字 = 臺語音
			國語流水號 = self.加文字佮版本(self.華語台語雙語語料庫系統, 字詞, 國語臺員腔, 臺員, 民國,
					國語詞, '', 版本正常)
			閩南語流水號 = self.加文字佮版本(self.華語台語雙語語料庫系統, 字詞, 閩南語, 臺員, 民國,
				配對臺語字, 臺語音, 版本正常)
# 					閩南語流水號 = 揣文字上大流水號()
			國語關係流水號 = self.加關係(國語流水號, 閩南語流水號, 義近, 會當替換)
			閩南語關係流水號 = self.加關係(閩南語流水號, 國語流水號, 義近, 會當替換)
			國語句流水號組合 += str(國語關係流水號) + 文字組合符號
			閩南語句流水號組合 += str(閩南語關係流水號) + 文字組合符號
			配對臺語字陣列.append(配對臺語字)
		
		# 整合句
		國語句流水號組合 += '#'
		閩南語句流水號組合 += '#'
		一逝配對臺語字 = 分詞符號.join(配對臺語字陣列)
		國語流水號 = self.加文字佮組合佮版本(self.華語台語雙語語料庫系統, 語句, 國語臺員腔, 臺員, 民國,
			一逝國語, '', 國語句流水號組合, 版本正常)
		閩南語流水號 = self.加文字佮組合佮版本(self.華語台語雙語語料庫系統, 語句, 閩南語, 臺員, 民國,
			一逝配對臺語字, 一逝音標, 閩南語句流水號組合, 版本正常)
		國語句關係流水號 = self.加關係(國語流水號, 閩南語流水號, 義近, 會當替換)
		閩南語句關係流水號 = self.加關係(閩南語流水號, 國語流水號, 義近, 會當替換)
		return ((一逝國語, 一逝配對臺語字, 一逝音標),
			(str(國語句關係流水號), str(閩南語句關係流水號)),)
	def 加文字佮版本(self, *arg):
# 		print(arg)
		return 加文字佮版本(*arg)
	def 加文字佮組合佮版本(self, *arg):
# 		print(arg)
		return 加文字佮組合佮版本(*arg)
	def 加關係(self, *arg):
# 		print(arg)
		return 加關係(*arg)
if __name__ == '__main__':
	整合平行語料()
