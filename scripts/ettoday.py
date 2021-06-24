from datetime import datetime
from Script.Http import Http
from bs4 import Tag

http: Http

HOT_NEWS_URL = 'https://www.ettoday.net/news/realtime-hot.htm'
BREAK_TEXT  = [
    '其他人也看了這些新聞',
    '更多新聞',
    '更多國際熱門新聞',
    '更多熱門新聞',
    '你可能也想看',
    '你可能有興趣',
    '更多精彩內容' ]

def listing():
    ret = []

    res = http.Get(HOT_NEWS_URL)
    if res.Status != 200:
        return ret

    document = res.ToSoup()
    for elem in document.select('div.hot-newslist div.block_content .piece.clearfix h3 a'):
        elem: Tag
        url: str

        title     = elem.string
        url       = elem['href']
        ids       = url.split('/')
        news_time = ids[-2]
        news_id   = ids[-1].split('.')[0]

        if not url or not url.startswith('http'):
            return ''

        try:
            ret.append({
                'key' : news_id,
                'data': {
                    'time'  : datetime.strptime(news_time, '%Y%m%d'),
                    'title' : title,
                    'url'   : url }})
        except:
            pass
    return ret

def fetch(data):
    element: Tag

    res = http.Get(data['url'])
    if res.Status != 200:
        return None

    contents = []
    document = res.ToSoup()
    newstype = document.select('div.part_menu_5.clearfix strong')[0].string
    for element in document.select('div.story p'):
        if not element.string:
            continue
        elif True in list(map(lambda text: element.string.find(text) != -1, BREAK_TEXT)):
            break
        contents.append(element.string)

    return {
        'title'      : '東森新聞 - {}'.format(newstype),
        'description': data['title'],
        'content'    : '\n\n'.join(contents),
        'update_time': data['time'] }