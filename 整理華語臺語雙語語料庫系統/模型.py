from django.db import models

class 存入來的文章(models.Model):
	文章編號流水號 = models.IntegerField(primary_key=True)
