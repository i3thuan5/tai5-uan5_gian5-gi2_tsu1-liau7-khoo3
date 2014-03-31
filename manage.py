/# -*- coding: utf-8 -*-
#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tai5_uan5_gian5_gi2_tsu1_liau7_khoo3.settings")

	from django.core.management import execute_from_command_line

	execute_from_command_line(sys.argv)
