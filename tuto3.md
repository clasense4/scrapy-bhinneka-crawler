#Step by step crawling bhinneka.com - part 3

I know you read my [first post](http://clasense4.wordpress.com/2013/01/22/scrapy-how-to-step-by-step-crawling-bhinneka-com-part-1/) and [second post](http://clasense4.wordpress.com/2013/01/24/scrapy-how-to-step-by-step-crawling-bhinneka-com-part-2/), that's still not complete, and now I will complete this tuts, this is not the last post in this session about scrapy. Actually, I really don't know if my method is right or wrong, but it really works, and I got what I need. Do not hesitate to ask me, just goto [about](http://clasense4.wordpress.com/about/) and ask me, if I can help, I will answer your question.

##Let's do it
1. Open your terminal and create new scrapy project (my scrapy version is 0.14.3) :

        $> scrapy startproject scrapy_bhinneka_crawler

2. Edit your `scrapy_bhinneka_crawler/settings.py`, add this line :

        import sys
        import MySQLdb

        # SCRAPY SETTING
        SPIDER_MODULES = ['crawler_bhinneka.spiders']
        NEWSPIDER_MODULE = 'crawler_bhinneka.spiders'
        USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

        # SQL DATABASE SETTING
        SQL_DB = 'scrapy'
        SQL_TABLE = 'bhinneka'
        SQL_HOST = 'localhost'
        SQL_USER = 'root'
        SQL_PASSWD = '54321'

        # connect to the MySQL server
        try:
            CONN = MySQLdb.connect(host=SQL_HOST,
                                 user=SQL_USER,
                                 passwd=SQL_PASSWD,
                                 db=SQL_DB)
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit(1)

3. Now we decide what we want to save. Edit your `scrapy_bhinneka_crawler/items.py`, add this line :

        from scrapy.item import Item, Field

        class ScrapyBhinnekaCrawlerItem(Item):
            # define the fields for your item here like:
            # name = Field()
            item_link = Field()
            item_name = Field()
            item_category = Field()
            item_price = Field()

4. Now create a spider file in `scrapy_bhinneka_crawler/spiders/spider.py`, and wrap up what we already learn :

        from scrapy.selector import HtmlXPathSelector
        from scrapy.contrib.spiders import CrawlSpider
        from scrapy.log import *
        from scrapy_bhinneka_crawler.settings import *
        from scrapy_bhinneka_crawler.items import *


        class BhinnekaSpider(CrawlSpider):

            name = 'bhinneka_spider'
            start_urls = [
                'http://www.bhinneka.com/categories.aspx'
            ]

            def parse(self, response):
                hxs = HtmlXPathSelector(response)
                # HXS to find url that goes to detail page
                items = hxs.select('//div[@id="ctl00_content_divContent"]//li[@class="item"]/a[2]/@href')
                for item in items:
                    link = item.extract()
                    print link

5. Go back to terminal and test our spider with command :

        $> scrapy list
        bhinneka_spider
   
   If there's no problem the output must be like that.

6. Now let's test our spider with this command :

        $> scrapy crawl bhinneka_spider
        ...
        2013-01-25 17:00:20+0700 [scrapy] DEBUG: Telnet console listening on 0.0.0.0:6023
        2013-01-25 17:00:20+0700 [scrapy] DEBUG: Web service listening on 0.0.0.0:6080
        2013-01-25 17:00:24+0700 [bhinneka_spider] DEBUG: Crawled (200) <GET http://www.bhinneka.com/categories.aspx> (referer: None)
        /aspx/products/pro_display_products.aspx?CategoryID=01VV
        /aspx/products/pro_display_products.aspx?CategoryID=01VW
        /aspx/products/pro_display_products.aspx?CategoryID=01VK
        /aspx/products/pro_display_products.aspx?CategoryID=01VG
        /aspx/products/pro_display_products.aspx?CategoryID=01VJ
        ...

   I have minimalize the output only 5 will appear, the actual result is so many.
   And now We know Our spider is working.

7. It's look not good, let's add some function to complete the url.

        def complete_url(string):
            """Return complete url"""
            return "http://www.bhinneka.com" + string

   And add the function into this line :

        def parse(self, response):
            hxs = HtmlXPathSelector(response)
            # HXS to find url that goes to detail page
            items = hxs.select('//div[@id="ctl00_content_divContent"]//li[@class="item"]/a[2]/@href')
            for item in items:
                link = item.extract()
                print complete_url(link)   

8. And try Our spider again :

        $> scrapy crawl bhinneka_spider
        ...
        2013-01-25 17:15:14+0700 [scrapy] DEBUG: Telnet console listening on 0.0.0.0:6023
        2013-01-25 17:15:14+0700 [scrapy] DEBUG: Web service listening on 0.0.0.0:6080
        2013-01-25 17:15:32+0700 [bhinneka_spider] DEBUG: Crawled (200) <GET http://www.bhinneka.com/categories.aspx> (referer: None)
        http://www.bhinneka.com/aspx/products/pro_display_products.aspx?CategoryID=01VV
        http://www.bhinneka.com/aspx/products/pro_display_products.aspx?CategoryID=01VW
        http://www.bhinneka.com/aspx/products/pro_display_products.aspx?CategoryID=01VK
        http://www.bhinneka.com/aspx/products/pro_display_products.aspx?CategoryID=01VG
        http://www.bhinneka.com/aspx/products/pro_display_products.aspx?CategoryID=01VJ
        ...
   
   Looks better isn't it?

##Conclusion

This is not the end of tuts, next? We will use scrapy to crawl again the link, and save into MySQL. Don't forget to play around in [scrapy docs](https://scrapy.readthedocs.org/en/latest/). If you can't wait for next part of tutorial, just [fork it](https://github.com/clasense4/scrapy-bhinneka-crawler) .
