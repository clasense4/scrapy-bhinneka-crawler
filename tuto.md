#Step by step crawling bhinneka.com

I want to show you how to scrap one of the biggest online store in indonesia, [Bhinneka.com](http://www.bhinneka.com). I'm often check to compare price, day by day. Especially, computer peripheral. My Goal from this crawler is to create item comparing site, You can track item price history day by day.

##Let's do it

1. Make sure you have scrapy installed in your machine (I use ubuntu 10.04). [Installation](http://doc.scrapy.org/en/0.16/intro/install.html)
2. First, open up [Bhinneka.com](http://www.bhinneka.com) in your browser, (I use google chrome), and find [Shop by Categories](http://www.bhinneka.com/categories.aspx).
3. Then right click in magnify icon, click "inspect element". And now you know what element in it. It show Us next link that we want to scrap. If we hover to the icon, the link will appear, maybe something like [this](http://www.bhinneka.com/aspx/products/pro_display_products.aspx?CategoryID=01A8).
4. Then save the link, and try to use scrapy via console with this command to get all the links. `scrapy shell http://www.bhinneka.com/aspx/products/pro_display_products.aspx?CategoryID=01A8`.

        fajri@fajri-laptop:~$ scrapy shell http://www.bhinneka.com/aspx/products/pro_display_products.aspx?CategoryID=01A8
        2013-01-22 12:30:12+0700 [scrapy] INFO: Scrapy 0.14.3 started (bot: scrapybot)
        2013-01-22 12:30:12+0700 [scrapy] DEBUG: Enabled extensions: TelnetConsole, CloseSpider, WebService, CoreStats, MemoryUsage, SpiderState
        2013-01-22 12:30:12+0700 [scrapy] DEBUG: Enabled downloader middlewares: HttpAuthMiddleware, DownloadTimeoutMiddleware, UserAgentMiddleware, RetryMiddleware, DefaultHeadersMiddleware, RedirectMiddleware, CookiesMiddleware, HttpCompressionMiddleware, ChunkedTransferMiddleware, DownloaderStats
        2013-01-22 12:30:12+0700 [scrapy] DEBUG: Enabled spider middlewares: HttpErrorMiddleware, OffsiteMiddleware, RefererMiddleware, UrlLengthMiddleware, DepthMiddleware
        2013-01-22 12:30:12+0700 [scrapy] DEBUG: Enabled item pipelines: 
        2013-01-22 12:30:12+0700 [scrapy] DEBUG: Telnet console listening on 0.0.0.0:6024
        2013-01-22 12:30:12+0700 [scrapy] DEBUG: Web service listening on 0.0.0.0:6081
        2013-01-22 12:30:12+0700 [default] INFO: Spider opened
        2013-01-22 12:30:13+0700 [default] DEBUG: Crawled (200) <GET http://www.bhinneka.com/aspx/products/pro_display_products.aspx?CategoryID=01A7> (referer: None)
        [s] Available Scrapy objects:
        [s]   hxs                <HtmlXPathSelector xpath=None data=u'<html id="ctl00_html" itemscope="itemsco'>
        [s]   item           {}
        [s]   request        <GET http://www.bhinneka.com/aspx/products/pro_display_products.aspx?CategoryID=01A8>
        [s]   response   <200 http://www.bhinneka.com/aspx/products/pro_display_products.aspx?CategoryID=01A8>
        [s]   settings   <CrawlerSettings module=None>
        [s]   spider         <BaseSpider 'default' at 0xa7e33ec>
        [s] Useful shortcuts:
        [s]   shelp()                   Shell help (print this help)
        [s]   fetch(req_or_url) Fetch request (or URL) and update local objects
        [s]   view(response)        View response in a browser

5. Then use this command to get all links inside the page `hxs.select('//div[@id="ctl00_content_divContent"]//li[@class="item"]/a[2]/@href').extract()`. The output is something like this.

        [u'/aspx/products/pro_display_products.aspx?CategoryID=01VV',
         u'/aspx/products/pro_display_products.aspx?CategoryID=01VW',
         u'/aspx/products/pro_display_products.aspx?CategoryID=01VK',
         u'/aspx/products/pro_display_products.aspx?CategoryID=01VG',
         ...

6. We use those links to get our details. But those links seems not right, so put this function in your ipython console :

        def complete_url(string):
            """Return complete url"""
            return "http://www.bhinneka.com" + string

7. And test again our script

        items = hxs.select('//div[@id="ctl00_content_divContent"]//li[@class="item"]/a[2]/@href').extract()
        new_items = [complete_url(item) for item in items]
        print new_items
        [u'http://www.bhinneka.com/aspx/products/pro_display_products.aspx?CategoryID=01VV',
         u'http://www.bhinneka.com/aspx/products/pro_display_products.aspx?CategoryID=01VW',
         u'http://www.bhinneka.com/aspx/products/pro_display_products.aspx?CategoryID=01VK',
         u'http://www.bhinneka.com/aspx/products/pro_display_products.aspx?CategoryID=01VG', 
         ...

