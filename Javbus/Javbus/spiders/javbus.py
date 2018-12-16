# -*- coding: utf-8 -*-
import scrapy
from ..items import JavbusItem
from scrapy.spider import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
import re
import math
import random

class JavbusSpider(scrapy.Spider):
    name = 'javbus'
    allowed_domains = ['javbus.pw',"javbus.org","javbus.com"]

    def start_requests(self):
        urls = ["https://www.javbus.org/actresses"]
        for url in urls:
            #因为很多作品在有码和无码里没有，因此需要根据女星的作品来爬取所有的番号
            if "actresses" not in url:
                yield Request(url=url,callback=self.parse_works)

            else:
                yield Request(url=url,callback=self.parse)

    def parse(self, response):
        """"""

        actress = response.xpath("//div[@id='waterfall']/div")
        for i in range(len(actress)):
            url = actress[i].xpath("a/@href").extract_first()
            name = actress[i].xpath("a/div[2]/span/text()").extract_first()
            print(name)
            yield Request(url=url,callback=self.parse_works)
        if "/uncensored" in response.url:
            baseUrl = response.url.replace("/uncensored","").split("/page")[0]
        else:

            baseUrl = response.url.split("/page")[0]
        next_url = response.xpath("//ul[@class='pagination pagination-lg']/li[last()]/a/@href").extract_first()

        if next_url:
            next_page = baseUrl + next_url
            print(next_page)
            yield Request(url=next_page,callback=self.parse)
    def parse_works(self, response):
        elements = response.xpath("//div[@id='waterfall']/div")

        for i in range(len(elements)):

            #详情页链接
            item = JavbusItem()
            if ".org" in response.url:
                type = "欧美"
            elif "uncensored" in response.url:

                type = "无码"
            else:
                type = "有码"
            url = elements[i].xpath("a/@href").extract_first()
            if url:
                #封面
                cover = elements[i].xpath("a/div[1]/img/@src").extract_first()
                #标题
                title = elements[i].xpath("a/div[2]/span/text()").extract_first()
                #番号
                car = elements[i].xpath("a/div[2]/span/date[1]/text()").extract_first()
                #时间
                openTime = elements[i].xpath("a/div[2]/span/date[2]/text()").extract_first()
                #日期标签
                timeTag = elements[i].xpath("a/div[2]/span/div/button/text()").extract_first()
                item["url"] = url

                item["cover"] = cover
                item["car"] = car
                item["title"] = title
                item["openTime"]= openTime
                item["timeTag"] = timeTag
                item["url"] = url
                item["type"] = type
                #下一级抓取详细信息
                yield Request(url=url,meta={"item":item},callback=self.parse_detail)
        if "/uncensored" in response.url:
            baseUrl = response.url.replace("/uncensored","").split("/page")[0]
        else:

            baseUrl = response.url.split("/page")[0]
        next_url = response.xpath("//ul[@class='pagination pagination-lg']/li[last()]/a/@href").extract_first()

        if next_url:
            next_page = baseUrl + next_url
            yield Request(url=next_page,callback=self.parse_works)


    def parse_detail(self,response):
        """

        :param response: 详细信息的url
        :return: 下一级
        """
        item = response.meta.get("item")
        #时长
        pattern1 = re.compile("長度:</span>(.*?)</p>")
        matcher1 = pattern1.search(response.text)
        if matcher1:
            item["duration"] = matcher1.group(1)
        #导演
        pattern2 = re.compile("導演:</span> <a .*>(.*?)</a>")
        matcher2 = pattern2.search(response.text)
        if matcher2:
            item["director"] = matcher2.group(1)
        #制作商
        pattern3 = re.compile("製作商:</span> <a .*>(.*?)</a>")
        matcher3 = pattern3.search(response.text)
        if matcher3:
            item["makeCompany"] = matcher3.group(1)
        #发行商
        pattern4 = re.compile("發行商:</span> <a .*>(.*?)</a>")
        matcher4 = pattern4.search(response.text)
        if matcher4:
            item["publishCompany"] = matcher4.group(1)
        #类型
        pattern5 = re.compile('href="https://www.javbus.*/genre/.*">(.*?)</a>')
        matcher5 = re.findall(pattern5,response.text)
        if matcher5:
            item["genre"] = list(set(matcher5))[1:]
        #演员
        pattern6 = re.compile('<a href="https://www.javbus.*/star/.*">(.*?)</a>')
        matcher6 = re.findall(pattern6,response.text)
        if matcher6:
            item["actor"] = list(set(matcher6))[1:]
        Image = response.xpath("//div[@class='col-md-9 screencap']/a/@href").extract_first()
        item["Image"] = Image
        pattern7 = re.compile("var gid = (\d+)",re.S)
        matcher7 = pattern7.search(response.text)
        pattern8 = re.compile("img = '(.*?)'",re.S)
        matcher8 = pattern8.search(response.text)
        if matcher7:
            gid = matcher7.group(1)
            img = matcher8.group(1)
            magnetUrl = "https://www.javbus.pw/ajax/uncledatoolsbyajax.php?gid={}&lang=zh&img={}&uc=0&floor={}".format(gid,img,math.floor(random.random()*1000+1))
            yield Request(url=magnetUrl,callback=self.parseMagnet,meta={"item":item})

    def parseMagnet(self,response):
        """

        :param response: 磁力的url
        :return: item
        """
        item = response.meta.get("item")

        elements = response.xpath("//tr")
        info = []
        if len(elements)>=1:
            for i in range(len(elements)):
                sourceInfo = {}
                #磁力链接
                mangetUrl = elements[i].xpath("td[1]/a/@href").extract_first()
                #番号
                fanhao = elements[i].xpath("td[1]/a/text()").extract_first().strip() if elements[i].xpath("td[1]/a/text()").extract_first() else ""
                sourceInfo["fanao"] = fanhao
                sourceInfo["magnetUrl"] = mangetUrl
                #视频大小
                size = elements[i].xpath("td[2]/a/text()").extract_first().strip() if  elements[i].xpath("td[2]/a/text()").extract_first() else ""
                sourceInfo["size"] = size
                #时间
                openTime = elements[i].xpath("td[3]/a/text()").extract_first().strip() if elements[i].xpath("td[3]/a/text()").extract_first() else ""
                sourceInfo["openTime"] = openTime
                info.append(sourceInfo)
        item["source"] = info
        yield item






