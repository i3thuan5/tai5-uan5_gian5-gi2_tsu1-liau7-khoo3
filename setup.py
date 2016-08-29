# -*- coding: utf-8 -*-
from distutils.core import setup
from os import walk
import sys
from 版本 import 版本

_專案說明 = '''
提供收集語料介面的django函式庫

希望能方便語言學習、研究。

感謝您的使用與推廣～～勞力！承蒙
'''

# tar無法度下傷長的檔案名，所以愛用zip
# python setup.py sdist --format=zip upload
try:
    # travis攏先`python setup.py sdist`才閣上傳
    sys.argv.insert(sys.argv.index('sdist') + 1, '--format=zip')
except ValueError:
    # 無upload
    pass


def 揣工具包(頭='.'):
    'setup的find_packages無支援windows中文檔案'
    工具包 = []
    for 目錄, _, 檔案 in walk(頭):
        if '__init__.py' in 檔案:
            工具包.append(目錄.replace('/', '.'))
    return 工具包

setup(
    name='tai5-uan5_gian5-gi2_tsu1-liau7-khoo3',
    packages=揣工具包('臺灣言語資料庫'),
    version=版本,
    description='臺灣語言資料庫系統',
    long_description=_專案說明,
    author='薛丞宏',
    author_email='ihcaoe@gmail.com',
    url='https://xn--v0qr21b.xn--kpry57d/',
    download_url='https://github.com/sih4sing5hong5/tai5_uan5_gian5_gi2_tsu1_liau7_khoo3',
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
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Linguistic',
    ],
    install_requires=[
        'tai5-uan5-gian5-gi2-kang1-ku7>=0.6.0',
        'django>=1.8.0',
        'pyyaml',
        'psycopg2',
        'django-cors-headers',
        'pypi-libavwrapper',
    ],
)
