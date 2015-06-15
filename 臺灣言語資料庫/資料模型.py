# -*- coding: utf-8 -*-
from builtins import isinstance
from django.core.files.base import File, ContentFile
from django.db import models
from django.db.models import Count
import json
import os

from libavwrapper.avconv import Input, Output, AVConv
from libavwrapper.codec import AudioCodec, NO_VIDEO
from django.conf import settings


class 屬性表函式:
	def 內容(self):
		return {self.分類:json.loads(self.性質)}
	@classmethod
	def 加屬性(cls, 分類, 性質):
		return cls.objects.get_or_create(分類=分類, 性質=json.dumps(性質))[0]
	@classmethod
	def 揣屬性(cls, 分類, 性質):
		return cls.objects.get(分類=分類, 性質=json.dumps(性質))
	
class 來源屬性表(models.Model, 屬性表函式):
	分類 = models.CharField(max_length=20)  # 出世地
	性質 = models.TextField()  # json字串格式。 臺灣、…
	
class 來源表(models.Model):
	名 = models.CharField(max_length=100)  # 人名、冊名、…
	屬性 = models.ManyToManyField(來源屬性表)  # 出世年、出世地、…
	def 屬性內容(self):
		內容結果 = {}
		for 屬性 in self.屬性.all():
			內容結果[屬性.分類] = json.loads(屬性.性質)
		return 內容結果
	def 編號(self):
		return self.pk
	@classmethod
	def 加來源(cls, 內容):
		名 = 內容['名']
		來源 = cls.objects.create(名=名)
		for 分類, 性質 in 內容.items():
			if 分類 != '名':
				來源.屬性.add(來源屬性表.加屬性(分類, 性質))
		return 來源
	@classmethod
	def 揣來源(cls, 內容):
		名 = 內容['名']
		來源屬性陣列 = []
		for 分類, 性質 in 內容.items():
			if 分類 != '名':
				來源屬性 = 來源屬性表.objects.get(分類=分類, 性質=json.dumps(性質))
				來源屬性陣列.append(來源屬性)
		選擇 = 來源表.objects.filter(名=名).annotate(屬性數量=Count('屬性'))
		for 來源屬性 in 來源屬性陣列:
			選擇 = 選擇.filter(屬性=來源屬性)
		return 選擇.get(屬性數量=len(來源屬性陣列))
	def __str__(self):
		return str(self.編號()) + ' ' + self.名
	
class 版權表(models.Model):
# 	會使公開，袂使公開
	版權 = models.CharField(max_length=20)

class 種類表(models.Model):
# 	字詞 = '字詞'
# 	語句 = '語句'
	種類 = models.CharField(max_length=100)

class 語言腔口表(models.Model):
# 	閩南語、閩南語永靖腔、客話四縣腔、泰雅seediq…
	語言腔口 = models.CharField(max_length=50)

class 著作所在地表(models.Model):
# 	臺灣、員林、…
	著作所在地 = models.CharField(max_length=50)

class 著作年表(models.Model):
# 	1952、19xx、…
	著作年 = models.CharField(max_length=20)

class 資料屬性表(models.Model, 屬性表函式):
	分類 = models.CharField(max_length=20, db_index=True)  # 詞性、語者…
	性質 = models.TextField()  # json字串格式。名詞、…

class 資料表(models.Model):
	class Meta:
		abstract = True
	收錄者 = models.ForeignKey(來源表, related_name='+')
	收錄時間 = models.DateTimeField(auto_now_add=True)
	來源 = models.ForeignKey(來源表, related_name='+')
	版權 = models.ForeignKey(版權表, related_name='+')
	種類 = models.ForeignKey(種類表, related_name='+')
	語言腔口 = models.ForeignKey(語言腔口表, related_name='+')
	著作所在地 = models.ForeignKey(著作所在地表, related_name='+')
	著作年 = models.ForeignKey(著作年表, related_name='+')
	屬性 = models.ManyToManyField(資料屬性表)  # 詞性,分類,…
	def 編號(self):
		return self.pk
	def 屬性內容(self):
		內容結果 = {}
		for 屬性 in self.屬性.all():
			內容結果[屬性.分類] = json.loads(屬性.性質)
		return 內容結果
	def _加基本內容而且儲存(self, 內容):
		if isinstance(內容['收錄者'], int):
			self.收錄者 = 來源表.objects.get(pk=內容['收錄者'])
		else:
			self.收錄者 = 來源表.揣來源(self._內容轉物件(內容['收錄者']))
		if isinstance(內容['來源'], int):
			self.來源 = 來源表.objects.get(pk=內容['來源'])
		else:
			來源物件 = self._內容轉物件(內容['來源'])
			try:
				self.來源 = 來源表.揣來源(來源物件)
			except:
				self.來源 = 來源表.加來源(來源物件)
		if isinstance(內容['版權'], int):
			self.版權 = 版權表.objects.get(pk=內容['版權'])
		elif isinstance(內容['版權'], str):
			self.版權 = 版權表.objects.get(版權=內容['版權'])
		else:
			raise TypeError('版權必須愛是字串抑是整數型態')
		if isinstance(內容['種類'], int):
			self.種類 = 種類表.objects.get(pk=內容['種類'])
		elif isinstance(內容['種類'], str):
			self.種類 = 種類表.objects.get(種類=內容['種類'])
		else:
			raise TypeError('種類必須愛是字串抑是整數型態')
		if isinstance(內容['語言腔口'], int):
			self.語言腔口 = 語言腔口表.objects.get(pk=內容['語言腔口'])
		elif isinstance(內容['語言腔口'], str):
			self.語言腔口 = 語言腔口表.objects.get_or_create(語言腔口=內容['語言腔口'])[0]
		else:
			raise TypeError('語言腔口必須愛是字串抑是整數型態')
		if isinstance(內容['著作所在地'], int):
			self.著作所在地 = 著作所在地表.objects.get(pk=內容['著作所在地'])
		elif isinstance(內容['著作所在地'], str):
			self.著作所在地 = 著作所在地表.objects.get_or_create(著作所在地=內容['著作所在地'])[0]
		else:
			raise TypeError('著作所在地必須愛是字串抑是整數型態')
		if isinstance(內容['著作年'], int):
			self.著作年 = 著作年表.objects.get(pk=內容['著作年'])
		elif isinstance(內容['著作年'], str):
			self.著作年 = 著作年表.objects.get_or_create(著作年=內容['著作年'])[0]
		else:
			raise TypeError('著作年必須愛是字串抑是整數型態')
		self.full_clean()
		if '屬性' in 內容:
			for _, _ in self._內容轉物件(內容['屬性']).items():
				pass
			self.save()
			for 分類, 性質 in self._內容轉物件(內容['屬性']).items():
				self.屬性.add(資料屬性表.objects.get_or_create(分類=分類, 性質=json.dumps(性質))[0])
# 			self.save()
		else:
			self.save()
	def _內容轉物件(self, 內容):
# 		try:
# 			return json.loads(內容)
# 		except:
# 			return 內容
		if isinstance(內容, str):
			return json.loads(內容)
		return 內容
	def _加關係的內容檢查(self, 內容):
		if 內容['種類'] != self.種類.種類:
			raise ValueError('新資料的種類「{}」愛佮原本資料的種類「{}」仝款！！'.format(內容['種類'], self.種類.種類))
		if 內容['語言腔口'] != self.語言腔口.語言腔口:
			raise ValueError('新資料的語言腔口「{}」愛佮原本資料的語言腔口「{}」仝款！！'
							.format(內容['語言腔口'], self.語言腔口.語言腔口))

class 資料類型表(models.Model):
# 	外語、文本、影音、聽拍
	類型 = models.CharField(max_length=20)

class 外語表(資料表):
	外語語言 = models.ForeignKey(語言腔口表, related_name='+')
	外語資料 = models.TextField(blank=False)
	def __str__(self):
		return self.外語資料
	@classmethod
	def 加資料(cls, 輸入內容):
		外語 = cls()
		內容 = 外語._內容轉物件(輸入內容)
		if isinstance(內容['外語語言'], int):
			外語.外語語言 = 語言腔口表.objects.get(pk=內容['外語語言'])
		elif isinstance(內容['外語語言'], str):
			外語.外語語言 = 語言腔口表.objects.get_or_create(語言腔口=內容['外語語言'])[0]
		else:
			raise TypeError('外語語言必須愛是字串抑是整數型態')
		if isinstance(內容['外語資料'], str):
			外語.外語資料 = 內容['外語資料']
		else:
			raise TypeError('外語資料必須愛是字串型態')
		外語._加基本內容而且儲存(內容)
		return 外語
	def 錄母語(self, 輸入影音內容):
		影音內容 = self._內容轉物件(輸入影音內容)
		self._加關係的內容檢查(影音內容)
		影音 = 影音表.加資料(影音內容)
		self.翻譯影音.create(影音=影音)
		return 影音
	def 翻母語(self, 輸入文本內容):
		文本內容 = self._內容轉物件(輸入文本內容)
		self._加關係的內容檢查(文本內容)
		文本 = 文本表.加資料(文本內容)
		self.翻譯文本.create(文本=文本)
		return 文本

class 影音表(資料表):
	原始影音資料 = models.FileField(blank=True)
	網頁影音資料 = models.FileField(blank=True)
	def __str__(self):
		return str(self.原始資料)
	@classmethod
	def 加資料(cls, 輸入內容):
		影音 = cls()
		內容 = 影音._內容轉物件(輸入內容)
		if not hasattr(內容['原始影音資料'], 'read'):
			raise TypeError('影音資料必須是檔案')
		影音._加基本內容而且儲存(內容)
		影音._存原始影音資料(內容['原始影音資料'])
		影音._產生網頁聲音資料()
		return 影音
	def 寫文本(self, 輸入文本內容):
		文本內容 = self._內容轉物件(輸入文本內容)
		self._加關係的內容檢查(文本內容)
		文本 = 文本表.加資料(文本內容)
		self.影音文本.create(文本=文本)
		return 文本
	def 寫聽拍(self, 輸入聽拍內容):
		聽拍內容 = self._內容轉物件(輸入聽拍內容)
		self._加關係的內容檢查(聽拍內容)
		聽拍 = 聽拍表.加資料(聽拍內容)
		self.影音聽拍.create(聽拍=聽拍)
		return 聽拍
	def _存原始影音資料(self, 原始影音資料):
		self.原始影音資料.save(name='原始影音資料{0:07}'.format(self.編號()), content=File(原始影音資料), save=True)
		self.原始影音資料.close()
	def _產生網頁聲音資料(self):
		self.網頁影音資料.save(name='網頁影音資料{0:07}.mp3'.format(self.編號()), content=ContentFile(b''), save=True)
		self.網頁影音資料.close()
		網頁聲音格式 = AudioCodec('libmp3lame')
		網頁聲音格式.channels(1)
		網頁聲音格式.frequence(16000)
		網頁聲音格式.bitrate('128k')
		原始檔案 = Input(os.path.join(settings.MEDIA_ROOT, self.原始影音資料.name))
		網頁檔案 = Output(os.path.join(settings.MEDIA_ROOT, self.網頁影音資料.name))
		網頁檔案.overwrite()
		指令 = AVConv('avconv', 原始檔案, 網頁聲音格式, NO_VIDEO, 網頁檔案)
		程序 = 指令.run()
		結果 = 程序.wait()
		if 結果 != 0:
			self.原始影音資料.delete()
			self.網頁影音資料.delete()
			self.delete()
			raise OSError(
				'avconv指令執行失敗，回傳值：{0}\n指令：{1}\n執行訊息：\n{2}'.format(
					結果, 指令, '\n'.join(程序.readlines()))) 

class 文本表(資料表):
	文本資料 = models.TextField(blank=False)
	def __str__(self):
		return self.文本資料
	@classmethod
	def 加資料(cls, 輸入內容):
		文本 = cls()
		內容 = 文本._內容轉物件(輸入內容)
		if isinstance(內容['文本資料'], str):
			文本.文本資料 = 內容['文本資料']
		else:
			raise TypeError('文本資料必須愛是字串型態')
		文本._加基本內容而且儲存(內容)
		return 文本
	def 校對做(self, 輸入文本內容):
		if self.是校對後的資料():
			raise ValueError('校對的資料袂使閣校對，必須對原來的資料校對')
		文本內容 = self._內容轉物件(輸入文本內容)
		self._加關係的內容檢查(文本內容)
		文本 = 文本表.加資料(文本內容)
		self.文本校對.create(新文本=文本)
		return 文本
	def 是校對後的資料(self):
		return self.校對資料來源.all().count() > 0

class 聽拍規範表(models.Model):
	規範名 = models.CharField(max_length=20, unique=True)
	範例 = models.TextField()
	說明 = models.TextField()

class 聽拍表(資料表):
# 	語者詳細資料記佇屬性內底，逐句話記是佗一个語者
	規範 = models.ForeignKey(聽拍規範表, related_name='全部資料')
	聽拍資料 = models.TextField()  # 存json.dumps的資料
	def __str__(self):
		return self.聽拍資料
	@classmethod
	def 加資料(cls, 輸入內容):
		聽拍 = cls()
		內容 = 聽拍._內容轉物件(輸入內容)
		if isinstance(內容['規範'], int):
			聽拍.規範 = 聽拍規範表.objects.get(pk=內容['規範'])
		elif isinstance(內容['規範'], str):
			聽拍.規範 = 聽拍規範表.objects.get(規範名=內容['規範'])
		else:
			raise TypeError('規範必須愛是字串抑是整數型態')
		聽拍資料內容 = 聽拍._內容轉物件(內容['聽拍資料'])
		for 一句 in 聽拍資料內容:
			if not isinstance(一句, dict):
				raise TypeError('聽拍資料內底應該是字典型態')
			if '內容' not in 一句:
				raise KeyError('逐句聽拍資料攏愛有「內容」欄位')
		聽拍.聽拍資料 = json.dumps(聽拍資料內容)
		聽拍._加基本內容而且儲存(內容)
		return 聽拍
	def 校對做(self, 輸入聽拍內容):
		if self.是校對後的資料():
			raise ValueError('校對的資料袂使閣校對，必須對原來的資料校對')
		聽拍內容 = self._內容轉物件(輸入聽拍內容)
		self._加關係的內容檢查(聽拍內容)
		if 聽拍內容['規範'] != self.規範.規範名:
			raise ValueError('新資料的規範「{}」愛佮原本資料的規範「{}」仝款！！'.format(聽拍內容['規範'], self.規範.規範名))
		聽拍 = 聽拍表.加資料(聽拍內容)
		self.聽拍校對.create(新聽拍=聽拍)
		return 聽拍
	def 是校對後的資料(self):
		return self.校對資料來源.all().count() > 0
