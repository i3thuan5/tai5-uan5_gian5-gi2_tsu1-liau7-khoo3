from django.db import models
from 臺灣言語資料庫.模型 import 編修

class 教育部臺灣閩南語常用詞辭典來源(models.Model):
	流水號 = models.ForeignKey(編修, related_name='教育部臺灣閩南語常用詞辭典來源',
		primary_key=True)
	主編號 = models.IntegerField()
	class Meta():
		db_table = '教育部臺灣閩南語常用詞辭典來源'
