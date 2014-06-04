# -*- coding: utf-8 -*-
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
		參考國語 = self.__資料分類.揣腔口近義(國語, 參考語句.編修.流水號).first()
		文字資料 = 編修資料.文字
		參考國語文字 = 參考國語.文字
		Pyro4.config.SERIALIZER = 'pickle'
		try:
			self.改定毋著的音標(參考語句)
			print('參考語句.音標', 參考語句.音標)
			建議結果物件 = self.__閩南語標音.語句斷詞標音(參考語句.音標)
			閩南語唸國語 = self.__閩南語標音.語句斷詞標音(參考國語文字.型體)
		except Exception as 錯誤:
			print(錯誤)
			raise 錯誤
		譀鏡 = 物件譀鏡()
		詞物件 = self.__分析器.建立詞物件('')
		建議結果來源 = '無'
		self.改定毋著的音標(文字資料)
		try:
			物件 = self.__分析器.產生對齊組(文字資料.型體, 文字資料.音標)
		except:
			物件 = self.__分析器.產生對齊字(文字資料.型體, 文字資料.音標)
		字陣列 = self.__篩仔.篩出字物件(物件)
		詞物件.內底字 = self.揣建議物件的字陣列(閩南語唸國語, 字陣列)
		建議結果來源 = self.閩南語唸國語
		if 詞物件.內底字 == []:
			詞物件.內底字 = self.揣建議物件的字陣列(建議結果物件, 字陣列)
			print(建議結果物件, 字陣列)
			建議結果來源 = self.參考語句音轉漢字
		if 詞物件.內底字 == []:
			print('字陣列內揣無，可能是外來詞')
			建議結果來源 = self.原本字
			詞物件.內底字 = 字陣列
# 		校對表格 = 文字校對表格(
# 			initial={'型體':譀鏡.看型(詞物件).replace('台', '臺')}, instance=文字資料)
		參考語句音轉漢字 = 譀鏡.看型(建議結果物件, 物件分詞符號 = ' ')
		閩南語唸參考國語文字 = 譀鏡.看音(閩南語唸國語)
		建議結果 = 譀鏡.看型(詞物件) .replace('台灣', '臺灣')
		應該音標 = 譀鏡.看音(詞物件)
		return (文字資料, 參考語句, 參考語句音轉漢字, 參考國語文字, 閩南語唸參考國語文字, 建議結果, 應該音標, 建議結果來源)
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
				if 建議字陣列[參考字物件所在 + 字物件所在].音 == 字陣列[字物件所在].音:
					pass
				elif 建議字陣列[參考字物件所在 + 字物件所在].音 \
					== 字陣列[字物件所在].音.replace('o', 'oo'):
					字陣列[字物件所在].音 = 字陣列[字物件所在].音.replace('o', 'oo')
					print(字陣列[字物件所在].音,'字陣列[字物件所在].音')
				else:
					對著 = False
			if 對著:
				return 參考字物件所在
		return None
	def 改定毋著的音標(self, 文字資料):
		if 文字資料.音標.startswith('m1'):
			文字資料.音標 = 'm7' + 文字資料.音標[2:]
		文字資料.音標 = 文字資料.音標.replace('-m1', '-m7')  # 毋
		文字資料.音標 = 文字資料.音標.replace('jiat4', 'jiat8')  # 熱
		文字資料.音標 = 文字資料.音標.replace('juah4', 'juah8')  # 熱
		文字資料.音標 = 文字資料.音標.replace('lat4', 'lat8')  # 力
		文字資料.音標 = 文字資料.音標.replace('kah8', 'kah4')  # 甲
		文字資料.音標 = 文字資料.音標.replace('uah4', 'uah8')  # 活
		文字資料.音標 = 文字資料.音標.replace('jit4', 'jit8')  # 日
		文字資料.音標 = 文字資料.音標.replace('mue2', 'mui2')  # 每
		文字資料.音標 = 文字資料.音標.replace('gak4', 'gak8')  # 樂
		文字資料.音標 = 文字資料.音標.replace('liok4', 'liok8')  # 六陸
		文字資料.音標 = 文字資料.音標.replace('kuh4', 'koh4')  # 毋「過」
		文字資料.音標 = 文字資料.音標.replace('bit4', 'bit8')  # 密
		文字資料.音標 = 文字資料.音標.replace('geh4', 'geh8')  # 月
		文字資料.音標 = 文字資料.音標.replace('gueh4', 'gueh8')  # 月
		文字資料.音標 = 文字資料.音標.replace('liat4', 'liat8')  # 烈
		文字資料.音標 = 文字資料.音標.replace('boo3', 'bo5')  # 無
		文字資料.音標 = 文字資料.音標.replace('mai5', 'bai5')  # 埋
		文字資料.音標 = 文字資料.音標.replace('tshut8', 'tshut4')  # 出
		文字資料.音標 = 文字資料.音標.replace('ngo7', 'ngoo2')  # 五
		文字資料.音標 = 文字資料.音標.replace('͘', '')
		文字資料.音標 = 文字資料.音標.replace('giann5', 'ngia5')  # 迎
		文字資料.音標 = 文字資料.音標.replace('ken', 'king1')  # 間
		文字資料.音標 = 文字資料.音標.replace('nng1', 'nng7')  # 兩
		文字資料.音標 = 文字資料.音標.replace('jim7-ui5', 'jin7-ui5')  # 認為
		文字資料.音標 = 文字資料.音標.replace('goo5', 'goo7')  # 五
		文字資料.音標 = 文字資料.音標.replace('go7', 'goo7')  # 五
		文字資料.音標 = 文字資料.音標.replace('tsap4', 'tsap8')  # 十
		文字資料.音標 = 文字資料.音標.replace('jip8-pun2', 'jit8-pun2')  # 日本
		文字資料.音標 = 文字資料.音標.replace('king2-jian5', 'king3-jian5')  # 竟然
		文字資料.音標 = 文字資料.音標.replace('tsit8-tso2', 'tsit8-tso7')  # 一座
		文字資料.音標 = 文字資料.音標.replace('beh4-ho7', 'beh4-hoo7')  # 欲予
		文字資料.音標 = 文字資料.音標.replace('hu3-tsoo7', 'hu2-tsoo7')  # 輔助
		文字資料.音標 = 文字資料.音標.replace('ham3-ko2', 'ham3-koo2')  # 譀古
		文字資料.音標 = 文字資料.音標.replace('bueh4-ho7', 'bueh4-hoo7')  # 欲予
		文字資料.音標 = 文字資料.音標.replace('beh4-ho7', 'beh4-hoo7')  # 欲予
		文字資料.音標 = 文字資料.音標.replace('e5-po1', 'e5-poo1')  # 下晡
		文字資料.音標 = 文字資料.音標.replace('pan7-an2', 'pan7-an3')  # 辦案
		文字資料.音標 = 文字資料.音標.replace('hio2-jim7', 'honn2-jin7')  # 否認
		文字資料.音標 = 文字資料.音標.replace('hoo2-jim7', 'honn2-jin7')  # 否認
		文字資料.音標 = 文字資料.音標.replace('kan1-na7', 'kan1-na1')  # 干焦
		文字資料.音標 = 文字資料.音標.replace('tit4-beh4', 'tih4-beh4')  # 咧欲
		文字資料.音標 = 文字資料.音標.replace('it4-to2', 'it4-too7')  # 一度
		文字資料.音標 = 文字資料.音標.replace('tang5-tshiu2', 'tang7-tshiu2')  # 動手
		文字資料.音標 = 文字資料.音標.replace('he1-hok8', 'khue1-hok8')  # 恢復
		文字資料.音標 = 文字資料.音標.replace('an1-tsuann2', 'an2-tsuann2')  # 按怎
		文字資料.音標 = 文字資料.音標.replace('an3-tsuann2', 'an2-tsuann2')  # 按怎
		文字資料.音標 = 文字資料.音標.replace('tsap8-kho3', 'tsap8-khoo1')  # 箍
		文字資料.音標 = 文字資料.音標.replace('pah4-kho3', 'pah4-khoo1')  # 箍
		文字資料.音標 = 文字資料.音標.replace('tshing1-kho3', 'tshing1-khoo1')  # 箍
		文字資料.音標 = 文字資料.音標.replace('ban7-kho3', 'ban7-khoo1')  # 箍
		文字資料.音標 = 文字資料.音標.replace('kui2-kho3', 'kui2-khoo1')  # 箍
		文字資料.音標 = 文字資料.音標.replace('tsap8-khoo3', 'tsap8-khoo1')  # 箍
		文字資料.音標 = 文字資料.音標.replace('pah4-khoo3', 'pah4-khoo1')  # 箍
		文字資料.音標 = 文字資料.音標.replace('tshing1-khoo3', 'tshing1-khoo1')  # 箍
		文字資料.音標 = 文字資料.音標.replace('ban7-khoo3', 'ban7-khoo1')  # 箍
		文字資料.音標 = 文字資料.音標.replace('kui2-khoo3', 'kui2-khoo1')  # 箍
		文字資料.音標 = 文字資料.音標.replace('go5-tsap8', 'goo7-tsap8')  # 五
		文字資料.音標 = 文字資料.音標.replace('go5-pah4', 'goo7-pah4')  # 五
		文字資料.音標 = 文字資料.音標.replace('go5-tshing1-', 'goo7-tshing1')  # 五
		文字資料.音標 = 文字資料.音標.replace('go5-ban7', 'goo7-ban7')  # 五
		文字資料.音標 = 文字資料.音標.replace('iu5-guan5', 'iu1-guan5')  # 猶原
		文字資料.音標 = 文字資料.音標.replace('iau3-si7', 'iah4-si7')  # 猶是
		文字資料.音標 = 文字資料.音標.replace('phok8-huat4', 'pok8-huat4')  # 爆發
		文字資料.音標 = 文字資料.音標.replace('kan1-kho2', 'kan1-khoo2')  # 艱苦
		文字資料.音標 = 文字資料.音標.replace('si2-the2', 'si1-the2')  # 屍體
		文字資料.音標 = 文字資料.音標.replace('tshin1-tshiu7', 'tshin1-tshiunn7')  # 親像
		文字資料.音標 = 文字資料.音標.replace('huan3-be2', 'huan3-be7')  # 販賣
		文字資料.音標 = 文字資料.音標.replace('in2-tsong5', 'un2-tsong5')  # 隱藏
		文字資料.音標 = 文字資料.音標.replace('san2-giap4', 'san2-giap8')  # 產業
		文字資料.音標 = 文字資料.音標.replace('som1-lim5', 'sim1-lim5')  # 森林
		文字資料.音標 = 文字資料.音標.replace('hak4-sing1', 'hak8-sing1')  # 學生
		文字資料.音標 = 文字資料.音標.replace('an3-ni1', 'an2-ni1')  # 按呢
		文字資料.音標 = 文字資料.音標.replace('pak4-to2', 'pak4-too2')  # 腹肚

		文字資料.音標 = 文字資料.音標.replace('go5', 'goo7')  # 五 暫時用
		