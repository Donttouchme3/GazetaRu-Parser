import requests
from Configs import *
import json


class GazetaRuBaseParser:
    def __init__(self):
        self.Url = URL
        self.Host = HOST

    def GetHtml(self, Html):
        try:
            Html = requests.get(Html)
            return Html.text
        except requests.HTTPError:
            print('Сайт не работает')

    @staticmethod
    def SaveDataToJson(path, data):
        with open(f'{path}.json', mode='w', encoding='UTF-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
