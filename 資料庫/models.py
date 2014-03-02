from django.db import models

class 編修(models.Model):
	編修種類 = (('文字', '文字'), ('關係', '關係'), ('演化', '演化'))
	流水號 = models.AutoField(primary_key = True)
	種類 = models.CharField(max_length = 10, choices = 編修種類)
	版本 = models.CharField(max_length = 100, null = True)
	結果 = models.ForeignKey('self', related_name = '+',
		null = True)
	起來時間 = models.DateField(auto_now_add = True)
	修改時間 = models.DateField(auto_now = True)
	class Meta():
		db_table = '編修'

class 文字(models.Model):
	文字種類 = (('字詞', '字詞'), ('語句', '語句'), ('章表冊', '章表冊'))
	流水號 = models.ForeignKey('編修', primary_key = True)
	來源 = models.CharField(max_length = 100)
	種類 = models.CharField(max_length = 10, choices = 文字種類)
	腔口 = models.CharField(max_length = 100)
	地區 = models.CharField(max_length = 100)
	年代 = models.IntegerField()
	組合 = models.TextField(null = True)
	型體 = models.TextField()
	音標 = models.TextField(null = True)
	起來時間 = models.DateField(auto_now_add = True)
	修改時間 = models.DateField(auto_now = True)
	class Meta():
		db_table = '文字'

class 關係(models.Model):
	'仝字，用佇無仝言語層', '反義', '近義'
	'文讀層'
	'''會當替換	
	白話層
	袂當替換
	'''
	流水號 = models.ForeignKey('編修', related_name = '關係',
		primary_key = True,)
	甲流水號 = models.ForeignKey('編修', related_name = '關係甲')
	乙流水號 = models.ForeignKey('編修', related_name = '關係乙')
	乙對甲的關係類型 = models.CharField(max_length = 100)
	關係性質 = models.CharField(max_length = 100)
	詞性 = models.CharField(max_length = 100)
	起來時間 = models.DateField(auto_now_add = True)
	修改時間 = models.DateField(auto_now = True)
	class Meta():
		db_table = '關係'

class 演化(models.Model):
	'俗音', '合音'
	流水號 = models.ForeignKey('編修', related_name = '演化',
		primary_key = True)
	甲流水號 = models.ForeignKey('編修', related_name = '演化甲')
	乙流水號 = models.ForeignKey('編修', related_name = '演化乙')
	乙對甲的演化類型 = models.CharField(max_length = 100)
	解釋 = models.CharField(max_length = 100)
	解釋流水號 = models.ForeignKey('編修', related_name = '解釋')
	起來時間 = models.DateField(auto_now_add = True)
	修改時間 = models.DateField(auto_now = True)
	class Meta():
		db_table = '演化'
