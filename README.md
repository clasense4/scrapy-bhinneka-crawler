# Scrapy Bhinneka Crawler

This Crawler is for crawl an online shop [Bhinneka](http://www.bhinneka.com).
It will save the item name, link, categories and price in MySQL.

## How to Use :
1. Clone this repository

        git clone https://github.com/clasense4/scrapy-bhinneka-crawler.git

2. Edit `bhinneka_crawler/settings.py` change your `scrapy`, `redis` and `MySQL` setting
3. Insert this SQL query :
        
        CREATE TABLE `bhinneka` (
          `bhinneka_id` int(11) NOT NULL AUTO_INCREMENT,
          `name` tinytext NOT NULL,
          `link` tinytext NOT NULL,
          `categories` tinytext NOT NULL,
          `price` tinytext NOT NULL,
          PRIMARY KEY (`bhinneka_id`)
        ) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='latin1_swedish_ci'

4. Start your crawler with this command

        $> scrapy crawl bhinneka_spider

9. At 19 January 2013, this script give me `14567 Items`.

## Notice
The script is still sucks, just for fun, not follow scrapy standards, use at your own risks.

mail me at clasense4[at]gmail[dot]com

[@clasense4](http://twitter.com/clasense4)
