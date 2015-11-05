from django.core.management.base import BaseCommand, CommandError
from os.path import basename
from urllib import request, parse
from 臺灣言語資料庫.匯出入 import 匯出入工具


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
                安全網址 = parse.quote(網址).replace('%3A//', '://')
                with request.urlopen(安全網址):
                    網址陣列.append((安全網址, 網址))
            except Exception as e:
                print(e)
                失敗網址.append(網址)
        if len(失敗網址) > 0:
            raise CommandError('無法度下載：{}'.format('\n'.join(失敗網址)))
        匯入工具 = 匯出入工具()
        self.stdout.write(匯入工具.顯示資料狀態())
        for 安全網址, 原本網址 in 網址陣列:
            try:
                匯入工具.匯入網址(安全網址, not 參數['莫匯入影音'])
                self.stdout.write('「{}」匯入成功'.format(basename(原本網址)))
            except Exception as 錯誤:
                self.stdout.write('{}：{}'.format(type(錯誤).__name__, 錯誤))
                self.stdout.write('「{}」匯入失敗'.format(basename(原本網址)))
            finally:
                self.stdout.write(匯入工具.顯示資料狀態())
