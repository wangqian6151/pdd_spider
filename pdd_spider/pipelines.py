# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import pymysql
import logging


class MongoPipeline(object):
    # collection_name = 'Hotel'

    def __init__(self, mongo_uri, mongo_db):
        self.logger = logging.getLogger(__name__)
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # self.db[item.collection].insert_one(dict(item))
        print('save', dict(item))
        self.logger.debug('save' + str(dict(item)))
        print('self.db[item.collection]: ', self.db[item.collection])
        self.logger.debug('self.db[item.collection]: ' + str(self.db[item.collection]))
        print('mongodb status', self.db[item.collection].find({"id": item['id']}).count())
        self.logger.debug('mongodb status ' + str(self.db[item.collection].find({"id": item['id']}).count()))
        if self.db[item.collection].find({"id": item['id']}).count():  # 如果找到number,则只更新
            self.db[item.collection].update({"id": item['id']}, dict(item), upsert=True)
        else:  # 如果没有找到number,则插入新的数据
            self.db[item.collection].save(dict(item))
        return item


class MysqlPipeline(object):
    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.logger = logging.getLogger(__name__)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            port=crawler.settings.get('MYSQL_PORT'),
        )

    def open_spider(self, spider):
        self.db = pymysql.connect(self.host, self.user, self.password, self.database, charset='utf8',
                                  port=self.port)
        self.cursor = self.db.cursor()

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        # print(item['name'])
        # self.logger.debug(item['name'])
        data = dict(item)
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = 'INSERT INTO {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE'.format(table=item.table,
                                                                                             keys=keys,
                                                                                             values=values)
        update = ','.join([" {key} = %s".format(key=key) for key in data])
        sql += update
        try:
            print('sql :', sql)
            self.logger.debug('sql :' + sql)
            result = self.cursor.execute(sql, tuple(data.values()) * 2)
            print('sql result :', str(result))
            self.logger.debug('sql result :' + str(result))
            if result:
                print('MysqlPipeline Successful')
                self.logger.debug('MysqlPipeline Successful')
                self.db.commit()
                print('Successful   \n' * 3)
        except Exception as e:
            print('MysqlPipeline Failed:', str(e))
            self.logger.debug('MysqlPipeline Failed: ' + str(e))
            self.db.rollback()
            print('Failed   \n' * 3)
        # sql = 'insert into %s (%s) values (%s)' % (item.table, keys, values)
        # self.cursor.execute(sql, tuple(data.values()))
        # self.db.commit()
        return item


class PddSpiderPipeline(object):
    def process_item(self, item, spider):
        return item
