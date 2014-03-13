from django.db import models
from django.db.models.query import QuerySet
from 臺灣言語資料庫.欄位資訊 import 編修種類
from 臺灣言語資料庫.欄位資訊 import 狀況種類
from 臺灣言語資料庫.欄位資訊 import 猶未檢查
from 臺灣言語資料庫.欄位資訊 import 文字種類
from 臺灣言語資料庫.欄位資訊 import 關係種類
from 臺灣言語資料庫.欄位資訊 import 演化種類
from 臺灣言語資料庫.欄位資訊 import 改過


class 編修(models.Model):
	流水號 = models.AutoField(primary_key=True)
	種類 = models.CharField(max_length=10, choices=編修種類)
	狀況 = models.CharField(max_length=100, choices=狀況種類, default=猶未檢查)
	結果 = models.ForeignKey('self', related_name='+',
		null=True, default=None)
	收錄時間 = models.DateTimeField(auto_now_add=True)
	修改時間 = models.DateTimeField(auto_now=True)
	def 有對著資料無(self):
		return self.對著幾个資料() == 1
	def 對著幾个資料(self):
		數量 = 0
		for 項, 目 in 編修種類:
			數量 += getattr(self, 項).count()
		return 數量
# 		return self.文字.count() + self.關係.count() + self.演化.count()
	def __str__(self):
		return ' '.join([
			str(self.流水號) , self.種類
			])
	class Meta():
		db_table = '編修'

class 資料控制(QuerySet):
	def filter_one_or_create(self, **參數):
		資 = self.filter(**參數)
		if 資.exists():
			return 資.first()
		return self.create(**參數)

class 資料管理(models.Manager):
	use_for_related_fields = True
	def __init__(self, 控制方式=models.query.QuerySet):
		self.控制方式 = 控制方式
		super(資料管理, self).__init__()
	def get_query_set(self):
		return self.控制方式(self.model)
	def __getattr__(self, name, *args):
		if name.startswith("_"): 
			raise AttributeError
		return getattr(self.get_query_set(), name, *args) 

class 資料(models.Model):
	objects = 資料管理(資料控制)
	def save(self, *args, **kwargs):
		if self.pk == None:
			self.流水號 = 編修.objects.create(種類=self.__class__.__name__)
# 		if self.流水號.有對著資料無() == False:
		super(資料, self).save(*args, **kwargs)
	def 改過閣加結果(self):
		資料物件 = self.__class__.objects.get(流水號=self.pk)
		資料物件.pk = None
		資料物件.save()
		新編修資料 = 資料物件.流水號
		原來編修資料 = self.流水號
		原來編修資料.狀況 = 改過
		原來編修資料.結果 = 新編修資料
		原來編修資料.save()
		return 資料物件
	class Meta:
		abstract = True

class 文字(資料):
	流水號 = models.ForeignKey('編修', related_name='文字',
		primary_key=True)
	來源 = models.CharField(max_length=100)
	種類 = models.CharField(max_length=10, choices=文字種類)
	腔口 = models.CharField(max_length=100)
	地區 = models.CharField(max_length=100)
	年代 = models.IntegerField()
	組合 = models.TextField(blank=True)
	型體 = models.TextField()
	音標 = models.TextField(blank=True)
	調變 = models.TextField(blank=True)
	音變 = models.TextField(blank=True)
	收錄時間 = models.DateTimeField(auto_now_add=True)
	修改時間 = models.DateTimeField(auto_now=True)
# 	def save(self, *args, **kwargs):
# 		if self.pk == None:
# 			self.流水號 = 編修.objects.create(種類 = self.__class__.__name__)
# 		super(文字, self).save(*args, **kwargs)
	def __str__(self):
		return ' '.join([
			str(self.流水號) , self.來源 , self.型體])
	class Meta():
		db_table = '文字'

class 關係(資料):
	'文讀層'
	'''會當替換	
	白話層
	袂當替換
	'''
	流水號 = models.ForeignKey('編修', related_name='關係',
		primary_key=True,)
	甲流水號 = models.ForeignKey('編修', related_name='關係甲')
	乙流水號 = models.ForeignKey('編修', related_name='關係乙')
	乙對甲的關係類型 = models.CharField(max_length=100, choices=關係種類,)
	關係性質 = models.CharField(max_length=100)
	詞性 = models.CharField(max_length=100, blank=True)
	收錄時間 = models.DateTimeField(auto_now_add=True)
	修改時間 = models.DateTimeField(auto_now=True)
	def __str__(self):
		return ' '.join(
			[str(self.流水號) , str(self.甲流水號) , str(self.乙流水號)
			, self.乙對甲的關係類型
			])
	class Meta():
		db_table = '關係'

class 演化(資料):
	流水號 = models.ForeignKey('編修', related_name='演化',
		primary_key=True)
	甲流水號 = models.ForeignKey('編修', related_name='演化甲')
	乙流水號 = models.ForeignKey('編修', related_name='演化乙')
	乙對甲的演化類型 = models.CharField(max_length=100, choices=演化種類,)
	解釋流水號 = models.ForeignKey('編修', related_name='解釋',
		null=True, default=None)
	收錄時間 = models.DateTimeField(auto_now_add=True)
	修改時間 = models.DateTimeField(auto_now=True)
	def __str__(self):
		return ' '.join([
			str(self.流水號) , str(self.甲流水號) , str(self.乙流水號)
			, self.乙對甲的演化類型])
	class Meta():
		db_table = '演化'
