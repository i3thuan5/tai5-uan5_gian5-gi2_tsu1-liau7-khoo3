# -*- coding: utf-8 -*-
'''
tar無法度下傷長的檔案名，所以愛用zip
python3 setup.py sdist --format=zip upload
'''
from distutils.core import setup
import os
from 版本 import 版本

def 讀(檔名):
	return open(os.path.join(os.path.dirname(__file__), 檔名), encoding='utf-8').read()

setup(
	# 臺灣言語資料庫 tai5_uan5_gian5_gi2_tsu1_liau7_khoo3
	name='tai5_uan5_gian5_gi2_tsu1_liau7_khoo3',
	packages=['臺灣言語資料庫'],
	version=版本,
	description='臺灣語言資訊系統（Toolkit for Languages in Taiwan）',
	long_description=讀('README.md'),
	author='薛丞宏',
	author_email='ihcaoe@gmail.com',
	url='http://意傳.台灣/',
	download_url='https://github.com/sih4sing5hong5/tai5_uan5_gian5_gi2_tsu1_liau7_khoo3',  # I'll explain this in a second
	keywords=[
		'語料庫', '語言合成', '機器翻譯',
		'Taiwan', 'Natural Language', 'Corpus',
		'Text to Speech', 'TTS',
		'Machine Translateion',
		],
	classifiers=[
		'Development Status :: 4 - Beta',
		'Operating System :: OS Independent',
		'Framework :: Django',
		'Programming Language :: Python :: 3.3',
		'Programming Language :: Python :: 3.4',
		'Natural Language :: Chinese (Traditional)',
		'Topic :: Scientific/Engineering',
		'Topic :: Scientific/Engineering :: Information Analysis',
		'Topic :: Text Processing',
		'Topic :: Text Processing :: Linguistic',
		],
	install_requires=[
		'django>=1.7.0',
		],
)
