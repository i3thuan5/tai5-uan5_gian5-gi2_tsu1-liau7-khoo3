from django.core.management.base import BaseCommand, CommandError
from urllib import request
from 臺灣言語資料庫.匯出入 import 匯出入工具
from os.path import basename


class Command(BaseCommand):
    help = '匯入指定的yaml'

    def add_arguments(self, parser):
        parser.add_argument(
            '網址', nargs='+', type=str,
            help='愛下載的yaml網址'
        )
        parser.add_argument(
            '--莫匯入影音', action='store_true'
        )

    def handle(self, *args, **參數):
        網址陣列 = []
        失敗網址 = []
        for 網址 in 參數['網址']:
            try:
                with request.urlopen(網址):
                    網址陣列.append(網址)
            except:
                失敗網址.append(網址)
        if len(失敗網址) > 0:
            raise CommandError('無法度下載：{}'.format('\n'.join(失敗網址)))
        匯入工具 = 匯出入工具()
        for 網址 in 網址陣列:
            匯入工具.匯入網址(網址, not 參數['莫匯入影音'])
            print('「{}」成功匯入'.format(basename(網址)), file=self.stdout)
