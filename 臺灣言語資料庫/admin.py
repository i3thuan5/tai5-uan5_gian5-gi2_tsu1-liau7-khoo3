from django.contrib import admin
from 臺灣言語資料庫.models import 編修
from 臺灣言語資料庫.models import 文字
from 臺灣言語資料庫.models import 關係
from 臺灣言語資料庫.models import 演化
admin.site.register(編修)
admin.site.register(文字)
admin.site.register(關係)
admin.site.register(演化)