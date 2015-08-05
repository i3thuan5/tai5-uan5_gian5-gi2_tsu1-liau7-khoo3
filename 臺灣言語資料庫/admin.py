# -*- coding: utf-8 -*-
from django.apps.registry import apps
from django.contrib import admin


for model in apps.get_app_config('臺灣言語資料庫').get_models():
    admin.site.register(model)
