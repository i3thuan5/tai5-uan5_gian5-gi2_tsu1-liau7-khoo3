from 剖析相關工具.剖析結構化工具 import 剖析結構化工具
from 剖析相關工具.剖析工具 import 剖析工具
from 候選句.交叉二維揣候選句 import 詞相關評價
from 閩南資料.國閩字詞翻譯 import 字音結構化
from 候選句.交叉二維揣候選句 import 交叉二維揣候選句
from 候選句.建立候選句佮對應句關係 import 建立候選句佮對應句關係
from 候選句.建立候選句佮對應句關係 import 提出對照位置
from 候選句.建立候選句佮對應句關係 import 調整對照
from 候選句.建立候選句佮對應句關係 import 候選句佮對應句對照

class 翻譯整合:
	工具=剖析工具()
	結構化工具 = 剖析結構化工具()
	揣候選句工具 = 交叉二維揣候選句()
	def 國閩翻譯(self,待翻句):
		if isinstance(待翻句, list):
			return [self.國閩翻譯(句) for 句 in 待翻句]
		翻譯句結構化結果 = self.結構化工具.結構化剖析結果(待翻句)
		印出 = lambda 型體佮詞性語意:print(型體佮詞性語意[0], end = ' ')
	
		挑出分數懸的=[]
		for 剖析結果字串 in self.揣候選句工具.揣剖析資料:
	# 		print(剖析結果字串)
			結構化結果 = self.結構化工具.結構化剖析結果(剖析結果字串[3])
			分數 = self.揣候選句工具.相似比較(翻譯句結構化結果[1], 結構化結果[1], 詞相關評價)
			挑出分數懸的.append((分數[0],分數,結構化結果,剖析結果字串))
		挑出分數懸的.sort(key=lambda 資料:資料[0],reverse=True)
		翻譯結果=[]
		for i in range(3):
			if i<len(挑出分數懸的):
				剖析結果字串=挑出分數懸的[i][3]
				結構化結果=挑出分數懸的[i][2]
				分數=挑出分數懸的[i][1]
				print(分數)
				print(剖析結果字串)
				print(翻譯句結構化結果)
				print(結構化結果)
				self.結構化工具.處理結構化結果(翻譯句結構化結果, 印出)
				print()
				self.結構化工具.處理結構化結果(結構化結果, 印出)
				print()
				print(分數)
				對應句結構化 = 字音結構化([(剖析結果字串[4], 剖析結果字串[5])])
				print(對應句結構化)
				print(對應句結構化[0])
				print(對應句結構化[0].下跤)
				if 對應句結構化[0].下跤==None:
					continue
				候選句佮對應句 = self.結構化工具.處理結構化結果(結構化結果, 候選句佮對應句對照(對應句結構化[0]))
				print(候選句佮對應句)
				建立關係 = 建立候選句佮對應句關係()
				提出位置工具 = 提出對照位置()
				self.結構化工具.處理結構化結果(候選句佮對應句, 提出位置工具.提出位置)
				關係所在 = 提出位置工具.對照位置
				print(關係所在)
				調整物件 = 調整對照((len(剖析結果字串[4]), 關係所在))
				調整後的對照關係 = self.結構化工具.處理結構化結果(候選句佮對應句, 調整物件.調整)
				print("調整後的對照關係",end=" ")
				print(調整後的對照關係)
				# 替換結果 = 建立關係.相似換新(翻譯句結構化結果[1], 調整後的對照關係[1], 對應句結構化[0], 分數[1], 分數[2])
				對應句結構化 = 字音結構化([(剖析結果字串[4], 剖析結果字串[5])])
				print(對應句結構化[0].下跤)
				替換結果 = 建立關係.相似換新(翻譯句結構化結果[1], 調整後的對照關係[1], 對應句結構化[0], 分數[1], 分數[2])
	#  			分數=揣候選句工具.相似(翻譯句結構化結果[1], 結構化結果[1], 詞相關評價)
	# 			for 對應句 in 揣候選句工具.揣對應資料(剖析結果字串[0]):
	# 				print(對應句[1])
	# 				print(揣候選句工具.相似換新(翻譯句結構化結果, 結構化結果, 對應句[1], 詞相關評價))
				print(替換結果)
				替換陣列 = list(替換結果)
				替換陣列.sort()
				print(替換陣列)
				答案句 = []
				for 位置 in 替換陣列:
					print("替換結果[位置]")
					print(替換結果[位置])
					if 位置[0]<位置[1] or True:
						for 愛插入的詞 in 替換結果[位置]:
							print("愛插入的詞[0]")
							print(愛插入的詞[0])
							print(愛插入的詞[0][0])
							答案句.append(愛插入的詞[0][0])
		# 					for 詞選擇 in 愛插入的詞[0]:
		# 						print(詞選擇)
				for 答案 in 答案句:
					print(答案.型, end = "")
				print()
				for 答案 in 答案句:
					print(答案.音, end = " ")
				print()
				print()
				翻譯結果.append(答案句)
			return 翻譯結果
