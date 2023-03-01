import requests
import time
from bs4 import BeautifulSoup
from Configs import style
from BaseParser import GazetaRuBaseParser
from pprint import pprint


class CategoryParser(GazetaRuBaseParser):
    def __init__(self):
        super(CategoryParser, self).__init__()
        self.DATA = {}

    def Category(self, Html):
        Soup = BeautifulSoup(Html, 'html.parser')
        Section = Soup.find('div', class_='w_col4')
        Sections = Section.find_all('a', class_='b_ear')
        for Article in Sections:
            try:
                ArticleTitle = Article.find('div', class_='b_ear-title').get_text(strip=True)
                self.DATA[ArticleTitle] = []
                ArticleLink = self.Host + Article.get('href')
                ArticleHtml = self.GetHtml(ArticleLink)
                self.ArticlePageParser(ArticleHtml, ArticleLink, ArticleTitle)
            except:
                print('Не сработало')



    def ArticlePageParser(self, PageHtml, Link, ArticleTitle):
        ArticleSoup = BeautifulSoup(PageHtml, 'html.parser')
        ArticleData = ArticleSoup.find('article', class_='b_article')
        Title = ArticleData.find('h1', class_='headline').get_text(strip=True)
        try:
            Image = ArticleData.find('img', class_='item-image-front').get('src')
        except:
            Image = 'Нету изображения'
        if ArticleData.find('h2', class_='subheader'):
            Subhead = ArticleData.find('h2', class_='subheader').get_text(strip=True)
        else:
            Subhead = 'Нету описания'

        if ArticleData.find('span', class_='intro'):
            Intro = ArticleData.find('span', class_='intro').get_text(strip=True)
        else:
            try:
                Intro = ArticleData.find('div', class_='b_article-text').get_text(strip=True)
            except:
                Intro = 'Нету текста'
        self.DATA[ArticleTitle].append({
            'Image': Image,
            'Link': Link,
            'Definition': Subhead,
            'Text': Intro
        })



def StartParsing():
    Category = CategoryParser()
    CategoryInput = input('Введите категорию: ')
    CategoryLink = 'https://www.gazeta.ru/' + CategoryInput
    print(style.GREEN + 'Парсер начал работу')
    start = time.time()
    Html = Category.GetHtml(CategoryLink)
    Category.Category(Html)
    Category.SaveDataToJson(CategoryInput, Category.DATA)
    finish = time.time()
    print(style.GREEN + f'Парсер закончил работу за {round(finish - start, 2)} секунд')


StartParsing()
