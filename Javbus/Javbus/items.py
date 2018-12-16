# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JavbusItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #标题
    title = scrapy.Field()
    #地址
    url = scrapy.Field()
    #番号
    car = scrapy.Field()
    #发行时间
    openTime = scrapy.Field()
    #标签时间
    timeTag = scrapy.Field()
    #封面
    cover = scrapy.Field()
    #长度
    duration = scrapy.Field()
    #导演
    director = scrapy.Field()
    #制作商
    makeCompany = scrapy.Field()
    #发行商
    publishCompany = scrapy.Field()
    #类型
    genre = scrapy.Field()
    #演员
    actor = scrapy.Field()
    #大图
    Image = scrapy.Field()
    #磁力链
    source = scrapy.Field()
    #电影类型
    type = scrapy.Field()

