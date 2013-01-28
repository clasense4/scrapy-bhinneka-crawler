#Step by step crawling bhinneka.com - part 4

I know you read my [first post](http://clasense4.wordpress.com/2013/01/22/scrapy-how-to-step-by-step-crawling-bhinneka-com-part-1/), [second post](http://clasense4.wordpress.com/2013/01/24/scrapy-how-to-step-by-step-crawling-bhinneka-com-part-2/), and [third post](http://clasense4.wordpress.com/2013/01/24/scrapy-how-to-step-by-step-crawling-bhinneka-com-part-3/). This time, We will complete Our crawler, We will use scrapy to crawl again the link that we found, and save the data into MySQL.  Actually, I really don't know if my method is right or wrong, but it really works, and I got what I need. Do not hesitate to ask me, just goto [about](http://clasense4.wordpress.com/about/) and ask me, if I can help, I will answer your question.

##Let's do it

1. This is Our last spider code in `scrapy_bhinneka_crawler/spiders.py` :

        from scrapy.selector import HtmlXPathSelector
        from scrapy.contrib.spiders import CrawlSpider
        from scrapy.log import *
        from scrapy_bhinneka_crawler.settings import *
        from scrapy_bhinneka_crawler.items import *


        def complete_url(string):
            """Return complete url"""
            return "http://www.bhinneka.com" + string


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
                    print complete_url(link)

2. Now we want to crawl again the link we found, using scrapy [Request](http://doc.scrapy.org/en/0.16/topics/request-response.html), edit our parse method, and add this line :

        yield Request(complete_url(link), callback=self.parse_category)

   Our parse function will be like this :

        def parse(self, response):
            hxs = HtmlXPathSelector(response)
            # HXS to find url that goes to detail page
            items = hxs.select('//div[@id="ctl00_content_divContent"]//li[@class="item"]/a[2]/@href')
            for item in items:
                link = item.extract()
                yield Request(complete_url(link), callback=self.parse_category)

3. You noticed `callback=self.parse_category` is our callback when we found our link, what to do? This mean, we have to create new function called `parse_category`. Now, try to open some link from what we found. [example](http://www.bhinneka.com/aspx/products/pro_display_products.aspx?CategoryID=01A8). You see, there is `name`, `category` and `price`.

4. Lets try to scrap that single page using this command :

        $> scrapy shell http://www.bhinneka.com/aspx/products/pro_display_products.aspx?CategoryID=01A8

        items = hxs.select('//div[@class="box"]/table/tr')
        for item in items:
            print item.select('td[1]/a/text()').extract()[0]
            print item.select('td[2]/text()').extract()[0]
            print item.select('td[3]/text()').extract()[0]
  
  Here's the output :

        SEAGATE Barracuda 1TB
        HDD Internal SATA 3.5 inch
        Rp 795,900
        SEAGATE Barracuda 250GB
        HDD Internal SATA 3.5 inch
        Rp 562,800
        SEAGATE Barracuda 500GB
        HDD Internal SATA 3.5 inch
        Rp 710,600
        SEAGATE Barracuda Green 2TB
        HDD Internal SATA 3.5 inch
        Rp 1,100,400
        ...

  And now We got what we want, then we will create complete function and save our item.

5. This is our `parse_category` function. But don't forget to add `from scrapy.http import Request` :

        def parse_category(self, response):
            hxs = HtmlXPathSelector(response)
            # HXS to Detail link inside td and a
            items = hxs.select('//div[@class="box"]/table/tr')
            for item in items:
                print item.select('td[1]/a/text()').extract()[0]
                print item.select('td[2]/text()').extract()[0]
                print item.select('td[3]/text()').extract()[0]

6. Let's tes again our spider.

        $> scrapy crawl bhinneka_spider

  Woohoo, this is the result :

        ...
        2013-01-28 11:31:51+0700 [scrapy] DEBUG: Telnet console listening on 0.0.0.0:6023
        2013-01-28 11:31:51+0700 [scrapy] DEBUG: Web service listening on 0.0.0.0:6080
        2013-01-28 11:32:03+0700 [bhinneka_spider] DEBUG: Crawled (200) <GET http://www.bhinneka.com/categories.aspx> (referer: None)
        2013-01-28 11:32:04+0700 [bhinneka_spider] DEBUG: Redirecting (302) to <GET http://www.bhinneka.com/categories.aspx> from <GET http://www.bhinneka.com/aspx/products/pro_display_products.aspx?CategoryID=00N1>
        2013-01-28 11:32:04+0700 [bhinneka_spider] DEBUG: Redirecting (302) to <GET http://www.bhinneka.com/categories.aspx> from <GET http://www.bhinneka.com/aspx/products/pro_display_products.aspx?CategoryID=00K4>
        2013-01-28 11:32:06+0700 [bhinneka_spider] DEBUG: Crawled (200) <GET http://www.bhinneka.com/aspx/products/pro_display_products.aspx?CategoryID=00J5> (referer: http://www.bhinneka.com/categories.aspx)
        B-Grip Belt Grip
        Camera Belt and Waist Pack
        Rp Out of Stock
        KATA KT DL-HF-493
        Camera Belt and Waist Pack
        Rp 600,000
        KATA KT DL-HF-495
        Camera Belt and Waist Pack
        Rp 700,000
        2013-01-28 11:32:06+0700 [bhinneka_spider] DEBUG: Redirecting (302) to <GET http://www.bhinneka.com/categories.aspx> from <GET http://www.bhinneka.com/aspx/products/pro_display_products.aspx?CategoryID=00N0>
        2013-01-28 11:32:07+0700 [bhinneka_spider] DEBUG: Redirecting (302) to <GET http://www.bhinneka.com/categories.aspx> from <GET http://www.bhinneka.com/aspx/products/pro_display_products.aspx?CategoryID=01VV>
        2013-01-28 11:32:08+0700 [bhinneka_spider] DEBUG: Crawled (200) <GET http://www.bhinneka.com/aspx/products/pro_display_products.aspx?CategoryID=00N2> (referer: http://www.bhinneka.com/categories.aspx)
        BHINNEKA MAGAZINE LEGO The Calendar 2013
        General Interest and Science Magazine
        Rp 165,000
        ...

7. Now We are sure our spider is working and, good. Now is save our item to MySQL. Create our database and table refer to our settings in `scrapy_bhinneka_crawler/settings.py`. This is the table :

        CREATE TABLE `bhinneka` (
          `bhinneka_id` int(11) NOT NULL AUTO_INCREMENT,
          `name` tinytext NOT NULL,
          `link` tinytext NOT NULL,
          `categories` tinytext NOT NULL,
          `price` tinytext NOT NULL,
          `time_capt` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
          PRIMARY KEY (`bhinneka_id`)
        ) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='utf8_general_ci'

8. Create a function that save our item. And add this `from MySQLdb import escape_string` to use escape string. Here's the complete function :
        
        cursor = CONN.cursor()  # important MySQLdb Cursor object 

        def insert_table(datas):
            sql = "INSERT INTO %s (name, link, categories, price) \
        values('%s', '%s', '%s', '%s')" % (SQL_TABLE,
            escape_string(datas['item_name']),
            escape_string(datas['item_link']),
            escape_string(datas['item_category']),
            escape_string(datas['item_price'])
            )
            # print sql
            if cursor.execute(sql):
                print "Inserted"
            else:
                print "Something wrong"

9. Change `parse_category` function with this line :

    def parse_category(self, response):
        hxs = HtmlXPathSelector(response)
        items = hxs.select('//div[@class="box"]/table/tr')
        for item in items:
            bhinneka = ScrapyBhinnekaCrawlerItem()
            bhinneka['item_link'] = complete_url(item.select('td[1]/a/@href').extract()[0])
            bhinneka['item_name'] = encode(item.select('td[1]/a/text()').extract()[0])
            bhinneka['item_category'] = item.select('td[2]/text()').extract()[0]
            bhinneka['item_price'] = item.select('td[3]/text()').extract()[0]
            insert_table(bhinneka)

10. Test again Our Spider :

        $> scrapy crawl bhinneka_spider

  Woohoo, this is the result :

        ...
        2013-01-28 11:54:23+0700 [scrapy] DEBUG: Web service listening on 0.0.0.0:6085
        2013-01-28 11:54:28+0700 [bhinneka_spider] DEBUG: Crawled (200) <GET http://www.bhinneka.com/categories.aspx> (referer: None)
        2013-01-28 11:54:28+0700 [bhinneka_spider] DEBUG: Redirecting (302) to <GET http://www.bhinneka.com/categories.aspx> from <GET http://www.bhinneka.com/aspx/products/pro_display_products.aspx?CategoryID=01VV>
        2013-01-28 11:54:29+0700 [bhinneka_spider] DEBUG: Crawled (200) <GET http://www.bhinneka.com/aspx/products/pro_display_products.aspx?CategoryID=00ZP> (referer: http://www.bhinneka.com/categories.aspx)
        Inserted
        Inserted
        Inserted
        Inserted
        Inserted
        Inserted
        Inserted
        Inserted
        ...

11. Check Your Database, and Now You learn how to scraping bhinneka.com

##Conclusion

What next? Play around to [scrapy docs](https://scrapy.readthedocs.org/en/latest/). [Fork my repo](https://github.com/clasense4/scrapy-bhinneka-crawler), and give me some response about this tuts.
