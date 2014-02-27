"""
著作權所有 (C) 民國103年 意傳文化科技
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
from 臺灣言語工具.資料庫.資料庫連線 import 資料庫連線
from 臺灣言語工具.字詞組集句章.解析整理工具.物件譀鏡 import 物件譀鏡
from 臺灣言語工具.字詞組集句章.解析整理工具.轉物件音家私 import 轉物件音家私
from 臺灣言語工具.字詞組集句章.音標系統.閩南語.通用拼音音標 import 通用拼音音標
from 臺灣言語工具.字詞組集句章.解析整理工具.字物件篩仔 import 字物件篩仔
from 臺灣言語工具.斷詞標音.改字.阿拉伯數字 import 阿拉伯數字

class 匯入高先生的數位典藏文本:
	資料庫 = True
	def __init__(self):
		分析器 = 拆文分析器()
		篩仔=字物件篩仔()
		數字 = 阿拉伯數字()
		家私 = 轉物件音家私()
		譀鏡 = 物件譀鏡()

		檔案 = open('/dev/shm/台語數位典藏文本.txt')

		插入台語數位典藏文本資料庫 = 資料庫連線.prepare('INSERT INTO "高明達先生資料"."台語數位典藏文本" ' +
			'("漢羅","全羅") VALUES ($1,$2)')

		字音集合=[]
		數字集合 = set()
		for 行 in 檔案:
			if 行.strip()=='':
				continue
			資料 = 行.strip().split('\t')
			if len(資料) == 2:
				try:
					型, 音 = 資料
					句物件 = 分析器.產生對齊句(型, 音)
					字陣列=篩仔.篩出字物件(句物件)
					for 字物件 in 字陣列:
						if 字物件.型==字物件.音 and 數字.是數字無(字物件.型):
							數字集合.add(字物件.型)
					標準句 = 家私.轉做標準音標(通用拼音音標, 句物件)
					字音集合.append((譀鏡.看型(標準句), 譀鏡.看音(標準句)))
				except:
					print(型, 音)
					pass
			else:
				raise RuntimeError('一逝有問題！！' + 行)
		
		print(數字集合)
		print(len(字音集合))
		if self.資料庫:
			for 字, 音解析結果 in 字音集合:
				插入台語數位典藏文本資料庫(字, 音解析結果)

if __name__ == '__main__':
	匯入高先生的數位典藏文本()
