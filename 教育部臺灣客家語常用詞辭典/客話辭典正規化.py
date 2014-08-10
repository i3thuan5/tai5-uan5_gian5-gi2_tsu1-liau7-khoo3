# -*- coding: utf-8 -*-
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
from 臺灣言語工具.解析整理.文章粗胚 import 文章粗胚
class 客話辭典正規化:
	_粗胚 = 文章粗胚()
	def 處理音標頭前字佮加空白(self, 音標):
		音標 = 音標.split('）')[-1]
		音標 = 音標.replace('文', '')
		音標 = 音標.replace('白', '')
		音標 = self._粗胚.數字調英文中央加分字符號(音標)
		return 音標.strip()
	def 調整錯誤的詞條(self, 詞目, 新音):
		if 新音 in self.換音:
# 							print('{0}\n{1}\n{2}\n音標改正：{3}'.
# 								format(編號, 詞目, 新音, 換音[新音]))
			新音 = self.換音[新音]
			新詞目 = 詞目
		elif 詞目 == '時錶仔' and 新音 == 'shi55 biau24':
			新詞目 = '時錶'
		elif 詞目 == '磨刀仔' and 新音 == 'no55 do53':
			新詞目 = '磨刀'
		elif 詞目 == '紙炮仔' and 新音 == 'zhi24 pau11':
			新詞目 = '紙炮'
		elif 詞目 == '毆□死' and 新音 == 'eu55 bun11 gi55 si53':
			新詞目 = '毆分佢死'
		elif 詞目 == '竹馬仔' and 新音 == 'zhug5 ma53':
			新詞目 = '竹馬'
		elif 詞目 == '魚脯仔' and 新音 == 'ng55 pu24':
			新詞目 = '魚脯'
		elif 詞目 == '做粄仔' and 新音 == 'zo11 ban24':
			新詞目 = '做粄'
		elif 詞目 == '嫩葉仔' and 新音 == 'nun33 rhab2':
			新詞目 = '嫩葉'
		elif 詞目 == '茶壺仔' and 新音 == 'ca55 fu55':
			新詞目 = '茶壺'
		elif 詞目 == '嬰兒仔' and 新音 == 'o53 nga11':
			新詞目 = '嬰兒'
		elif 詞目 == '梅仔樹' and 新音 == 'moi55 shu33':
			新詞目 = '梅樹'
		elif 詞目 == '種痘仔' and 新音 == 'zhung11 teu33':
			新詞目 = '種痘'
		elif 詞目 == '送鬼仔' and 新音 == 'sung11 gui24':
			新詞目 = '送鬼'
		elif 詞目 == '頭臥臥仔' and 新音 == 'teu55 ngo11 ngo11':
			新詞目 = '頭臥臥'
		elif 詞目 == '時鐘仔' and 新音 == 'shi55 zhung53':
			新詞目 = '時鐘'
		else:
			新詞目 = 詞目
		新音 = 新音.replace('9', '31')
		return 新詞目, 新音
	換音 = {'han113 fa53 rhid21 tai53 doi33 zhin53 gin33 mo113 rhid21 pied54':
		'han113 fa53 rhid21 tai53 doi33, zhin53 gin33 mo113 rhid21 pied54',
		'mang11 shid5 ng53 ngied5 zied2 zung53 o53 po55 m55 ho53 ngib5 vung53':
		'mang11 shid5 ng53 ngied5 zied2 zung53, o53 po55 m55 ho53 ngib5 vung53',
		'cai55 ga11 cien11 ngid24 hoo31 chid24 mun53 ban31 zhio11 nan53':
		'cai55 ga11 cien11 ngid24 hoo31, chid24 mun53 ban31 zhio11 nan53',
		'teu55 na55 cab2 vo55 chan53 liau55 diau11':
		'teu55 na55 cab2 vo55 chan53 －－ liau55 diau11',
		'uai33 zhoi53 choi33 lab54 ba31，rhid21 ton113 sia113 ki53':
		'uai33 zhoi53 choi33 lab54 ba31 －－ rhid21 ton113 sia113 ki53',
		'gung33 bud21 li113 po113 chin53 bud21 li113 to113':
		'gung33 bud21 li113 po113, chin53 bud21 li113 to113',
		'ho53 ma11 m55 shid5 shid5 fui55 teu55 co53':
		'ho53 ma11 m55 shid5 fui55 teu55 co53',
		'han113 fa53 rhid21 tai53 doi33 zhin53 gin33 mo113 rhid21 pied54':
		'han113 fa53 rhid21 tai53 doi33, zhin53 gin33 mo113 rhid21 pied54',
		}
