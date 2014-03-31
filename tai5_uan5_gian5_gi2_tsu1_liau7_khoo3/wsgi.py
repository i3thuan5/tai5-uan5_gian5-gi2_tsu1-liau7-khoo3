# -*- coding: utf-8 -*-
"""
WSGI config for tai5_uan5_gian5_gi2_tsu1_liau7_khoo3 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tai5_uan5_gian5_gi2_tsu1_liau7_khoo3.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
