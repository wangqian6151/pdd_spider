# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy import Request

from pdd_spider.items import ThirdCategoryItem, GoodsItem


class PddSpider(scrapy.Spider):
    name = 'pdd'
    allowed_domains = ['yangkeduo.com']

    start_urls = ['https://api.yangkeduo.com/api/fiora/v2/home_operations']

    # base_url = 'https://api.yangkeduo.com/api/fiora/v2/home_operations'

    category_url = 'http://apiv4.yangkeduo.com/operation/{opt_id}/groups?offset=0&size=100&sort_type=DEFAULT&pdduid=0'

    goods_url = 'http://apiv4.yangkeduo.com/operation/{opt_id}/groups?offset={offset}&size=200&sort_type=DEFAULT&pdduid=0'

    goods_detail = 'http://apiv4.yangkeduo.com/api/oakstc/v14/goods/{goods_id}'

    def parse(self, response):
        result = json.loads(response.text)
        if result:
            for r in result:
                first_category_id = r.get('id')
                first_category_name = r.get('opt_name')
                first_category_img = r.get('image_url')
                for c in r.get('children'):
                    second_category_id = c.get('id')
                    second_category_name = c.get('opt_name')
                    second_category_img = c.get('image_url')
                    second_info_dict = {'first_category_id': first_category_id,
                                        'first_category_name': first_category_name,
                                        'first_category_img': first_category_img,
                                        'second_category_id': second_category_id,
                                        'second_category_name': second_category_name,
                                        'second_category_img': second_category_img}

                    yield Request(self.category_url.format(opt_id=second_category_id), callback=self.parse_category,
                                  meta={'second_info_dict': second_info_dict})

    def parse_category(self, response):
        result = json.loads(response.text)
        second_info_dict = response.meta.get('second_info_dict')
        first_category_id = second_info_dict.get('first_category_id')
        first_category_img = second_info_dict.get('first_category_img')
        first_category_name = second_info_dict.get('first_category_name')
        second_category_id = second_info_dict.get('second_category_id')
        second_category_name = second_info_dict.get('second_category_name')
        second_category_img = second_info_dict.get('second_category_img')
        if result.get('error_code'):
            self.logger.debug('parse_category error_code: {}'.format(result.get('error_code')))
            return Request(self.category_url.format(opt_id=second_category_id), callback=self.parse_category,
                           meta={'second_info_dict': second_info_dict})

        for info in result.get('opt_infos'):
            third_category_item = ThirdCategoryItem()
            third_category_item['first_category_id'] = first_category_id
            third_category_item['first_category_name'] = first_category_name
            third_category_item['first_category_img'] = first_category_img
            third_category_item['second_category_id'] = second_category_id
            third_category_item['second_category_name'] = second_category_name
            third_category_item['second_category_img'] = second_category_img
            third_category_id = info.get('id')
            third_category_item['id'] = third_category_id
            third_category_item['third_category_name'] = info.get('opt_name')
            yield third_category_item
            yield Request(self.goods_url.format(opt_id=third_category_id, offset=0), callback=self.parse_goods,
                          meta={'second_info_dict': second_info_dict, 'third_category_id': third_category_id,
                                'offset': 0})

    def parse_goods(self, response):
        result = json.loads(response.text)
        second_info_dict = response.meta.get('second_info_dict')
        first_category_id = second_info_dict.get('first_category_id')
        second_category_id = second_info_dict.get('second_category_id')
        third_category_id = response.meta.get('third_category_id')
        offset = response.meta.get('offset')
        if result.get('error_code'):
            self.logger.debug('parse_goods error_code: {}'.format(result.get('error_code')))
            return Request(self.goods_url.format(opt_id=third_category_id, offset=offset), callback=self.parse_goods,
                           meta={'second_info_dict': second_info_dict, 'third_category_id': third_category_id,
                                 'offset': offset})
        print('before goods_list: {}'.format(result.get('goods_list')))
        self.logger.debug('before goods_list: {}'.format(result.get('goods_list')))
        if 'goods_list' in result and result.get('goods_list'):
            print('after goods_list: {}'.format(result.get('goods_list')))
            self.logger.debug('after goods_list: {}'.format(result.get('goods_list')))
            for goods in result.get('goods_list'):
                goods_item = GoodsItem()
                goods_item['first_category_id'] = first_category_id
                goods_item['second_category_id'] = second_category_id
                goods_item['third_category_id'] = third_category_id
                goods_item['id'] = goods.get('goods_id')
                goods_item['goods_name'] = goods.get('goods_name')
                goods_item['short_name'] = goods.get('short_name')
                goods_item['link_url'] = 'http://yangkeduo.com/' + goods.get('link_url')
                goods_item['hd_thumb_url'] = goods.get('hd_thumb_url')
                goods_item['hd_url'] = goods.get('hd_url')
                goods_item['price'] = goods.get('group').get('price')
                goods_item['normal_price'] = goods.get('normal_price')
                goods_item['market_price'] = goods.get('market_price')
                goods_item['cnt'] = goods.get('cnt')
                goods_item['sales_tip'] = goods.get('sales_tip')
                yield goods_item
            offset = offset + 100
            self.logger.debug('parse_shops offset: {}'.format(offset))
            yield Request(self.goods_url.format(opt_id=third_category_id, offset=offset), callback=self.parse_goods,
                          meta={'second_info_dict': second_info_dict, 'third_category_id': third_category_id,
                                'offset': offset})
