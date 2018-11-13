# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class ThirdCategoryItem(Item):
    collection = table = 'ThirdCategory'

    first_category_id = Field()
    first_category_name = Field()
    first_category_img = Field()
    second_category_id = Field()
    second_category_name = Field()
    second_category_img = Field()
    id = Field()
    third_category_name = Field()


class GoodsItem(Item):
    collection = table = 'Goods'

    first_category_id = Field()
    second_category_id = Field()
    third_category_id = Field()
    id = Field()
    goods_name = Field()
    short_name = Field()
    price = Field()
    normal_price = Field()
    market_price = Field()
    link_url = Field()
    hd_thumb_url = Field()
    hd_url = Field()
    cnt = Field()
    sales_tip = Field()
