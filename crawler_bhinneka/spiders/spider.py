from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.log import *
from crawler_bhinneka.settings import *
from crawler_bhinneka.items import *
import pprint
from MySQLdb import escape_string
import urlparse

'''
Local VARIABLE
'''
cursor = CONN.cursor()
pp = pprint.PrettyPrinter(indent=4)


def complete_url(string):
    """Return complete url"""
    return "http://www.bhinneka.com" + string


def get_base_url(url):
    """
    >>> urlparse.urlparse('http://tmcblog.com')
    >>> ParseResult(scheme='http', netloc='tmcblog.com',
        path='', params='', query='', fragment='')
    """
    if url != "":
        u = urlparse.urlparse(url)
        return "%s://%s" % (u.scheme, u.netloc)
    else:
        return ""


def encode(str):
    return str.encode('utf8', 'ignore')


def insert_table(datas):
    """
    Just MySQL Insert function
    """
    sql = "INSERT INTO %s (name, link, categories, price) \
values('%s', '%s', '%s', '%s')" % (SQL_TABLE,
    escape_string(datas['item_name']),
    escape_string(datas['item_link']),
    escape_string(datas['item_category']),
    escape_string(datas['item_price'])
    )
    # print sql
    if cursor.execute(sql):
        return True
    else:
        print "Something wrong"


def insert_redis(command, key1, key2):
    """
    Just Redis Insert function
    """
    if command == 'sadd':
        if r.sadd(key1, key2):
            return True
    if command == 'set':
        if r.set(key1, key2):
            return True


class BhinnekaSpider(CrawlSpider):
    """
    1. Goto http://www.bhinneka.com/categories.aspx
    2. Find some interesting link
    (http://www.bhinneka.com/aspx/products/pro_display_products.aspx?\
    CategoryID=0115)
    3. Save Our data
    """

    name = 'bhinneka_spider'
    start_urls = [
        'http://www.bhinneka.com/categories.aspx'
    ]

    def parse(self, response):
        """
        Parse List Category page, example :
        http://www.bhinneka.com/categories.aspx
        """
        hxs = HtmlXPathSelector(response)
        # HXS to find url that goes to detail page
        items = hxs.select('//div[@id="ctl00_content_divContent"]\
//li[@class="item"]/a[2]/@href')
        for item in items:
            link = item.extract()
            yield Request(complete_url(link), callback=self.parse_category)

    def parse_category(self, response):
        """
        Parse Categories, example :
        http://www.bhinneka.com/aspx/products/pro_display_products.aspx?CategoryID=0115
        """
        hxs = HtmlXPathSelector(response)
        # HXS to Detail link inside td and a
        items = hxs.select('//div[@class="box"]/table/tr')
        for item in items:
            '''
            Save Our Item
            '''
            bhinneka = CrawlerBhinnekaItem()
            bhinneka['item_link'] = complete_url(item.select('td[1]/a/@href').extract()[0])
            bhinneka['item_name'] = encode(item.select('td[1]/a/text()').extract()[0])
            bhinneka['item_category'] = item.select('td[2]/text()').extract()[0]
            bhinneka['item_price'] = item.select('td[3]/text()').extract()[0]

            '''
            Save Our Item to MySQL
            '''
            insert_table(bhinneka)
