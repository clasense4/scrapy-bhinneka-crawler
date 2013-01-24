#Step by step crawling bhinneka.com - part 2

[Bhinneka.com](http://www.bhinneka.com), I know you read my [first post](http://clasense4.wordpress.com/2013/01/22/scrapy-how-to-step-by-step-crawling-bhinneka-com-part-1/), this is the next post how to scrap it. Actually, I really don't know if my method is right or wrong, but it really works, and I got what I need.

##Let's do it

1. You already know how to playing with xpath and scrapy object, but I forgot to mention to You, about xpath documentation [from microsoft](http://msdn.microsoft.com/en-us/library/ms256471.aspx), I think it's really the best.
2. Let's remember a while about last tuts, here's some of the code :
        
        items = hxs.select('//div[@id="ctl00_content_divContent"]//li[@class="item"]/a[2]/@href').extract()
        new_items = [complete_url(item) for item in items]
        print new_items
        [u'http://www.bhinneka.com/aspx/products/pro_display_products.aspx?CategoryID=01VV',
         u'http://www.bhinneka.com/aspx/products/pro_display_products.aspx?CategoryID=01VW',
         u'http://www.bhinneka.com/aspx/products/pro_display_products.aspx?CategoryID=01VK',
         u'http://www.bhinneka.com/aspx/products/pro_display_products.aspx?CategoryID=01VG', 
         ...

3. That's our clue, open [this sample link](http://www.bhinneka.com/aspx/products/pro_display_products.aspx?CategoryID=01A8) then inspect element to know what we want to get. Our target is `item name`, `item category`, `item link` and `item price`. You see, our sample category is `HDD Internal SATA 3.5 inch`.

4. Lets try this code `scrapy shell http://www.bhinneka.com/aspx/products/pro_display_products.aspx?CategoryID=01A8`. I bet you're already know what it's like.

5. Then, if we want to get the item try this code :

        items = hxs.select('//div[@class="box"]/table/tr')

        [<HtmlXPathSelector xpath='//div[@class="box"]/table/tr' data=u'<tr><td align="left"><a class="themenorm'>,
         <HtmlXPathSelector xpath='//div[@class="box"]/table/tr' data=u'<tr><td align="left"><a class="themenorm'>,
         <HtmlXPathSelector xpath='//div[@class="box"]/table/tr' data=u'<tr><td align="left"><a class="themenorm'>,
         <HtmlXPathSelector xpath='//div[@class="box"]/table/tr' data=u'<tr><td align="left"><a class="themenorm'>,
         <HtmlXPathSelector xpath='//div[@class="box"]/table/tr' data=u'<tr><td align="left"><a class="themenorm'>,
        ...

6. Then we loop our item. Remember, that's still not our last object before we do `.extract()` to get what we want. Then loop through the item to get item links with this command :

        for item in items:
            print complete_url(item.select('td[1]/a/@href').extract()[0])

        http://www.bhinneka.com/products/sku00212266/seagate_barracuda_1tb.aspx
        http://www.bhinneka.com/products/sku00911231/seagate_barracuda_250gb.aspx
        http://www.bhinneka.com/products/sku00411183/seagate_barracuda_500gb.aspx
        http://www.bhinneka.com/products/sku01112899/seagate_barracuda_green_2tb.aspx
        http://www.bhinneka.com/products/sku00711814/western_digital_caviar_black_2tb__wd2002faex_.aspx
        ...

7. If You want to get `item name` try this command :

        for item in items:
            print item.select('td[1]/a/text()').extract()[0]

        SEAGATE Barracuda 1TB
        SEAGATE Barracuda 250GB
        SEAGATE Barracuda 500GB
        SEAGATE Barracuda Green 2TB
        WESTERN DIGITAL Caviar Black 2TB [WD2002FAEX]
        WESTERN DIGITAL Caviar Black 500GB [WD5003AZEX]

8. If You want to get `item category` try this command :

        for item in items:
            print item.select('td[2]/text()').extract()[0]

        HDD Internal SATA 3.5 inch
        HDD Internal SATA 3.5 inch
        HDD Internal SATA 3.5 inch
        HDD Internal SATA 3.5 inch
        HDD Internal SATA 3.5 inch

9. If You want to get `item price` try this command :

        for item in items:
            print item.select('td[3]/text()').extract()[0]

        Rp 795,900
        Rp 562,800
        Rp 710,600
        Rp 1,100,400
        Rp 2,106,500


##Conclusion

Now, You're know how to use scrapy more than before, this is just a beginning and the other side tutorial from original [scrapy tutorial](https://scrapy.readthedocs.org/en/latest/intro/tutorial.html). If you can't wait for next part of tutorial, just [fork it](https://github.com/clasense4/scrapy-bhinneka-crawler).
