# Scrapy settings for crawler_bhinneka project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
import sys
import MySQLdb
import redis

BOT_NAME = 'crawler_bhinneka'
BOT_VERSION = '1.0'

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

# REDIS SERVER SETTING
REDIS_SERVER = 'localhost'
REDIS_PORT = 6380
REDIS_KEY_FORMAT = 'bhinneka:'

# connect to the MySQL server
try:
    CONN = MySQLdb.connect(host=SQL_HOST,
                         user=SQL_USER,
                         passwd=SQL_PASSWD,
                         db=SQL_DB)
except MySQLdb.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)

try:
    r = redis.Redis(REDIS_SERVER, REDIS_PORT)
except:
    print "Redis Error"
    sys.exit(1)
