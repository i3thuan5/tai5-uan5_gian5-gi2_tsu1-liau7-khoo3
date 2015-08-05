#!/bin/bash
rm __init__.py ; python manage.py migrate ; python manage.py test ; touch __init__.py
