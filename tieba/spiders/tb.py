# -*- coding: utf-8 -*-
import scrapy
from tieba.items import TiebaItem
import copy


class TbSpider(scrapy.Spider):
    name = 'tb'
    allowed_domains = ['tieba.baidu.com']
    start_urls = ['https://tieba.baidu.com/f?kw=fate&pn=0&']
    i=1
    def parse(self,response):
        self.i = 1
        item=TiebaItem()
        list = response.xpath('//*[@id="thread_list"]/li')
        for i in list:
            item["tittle"] = i.xpath('.//a[@rel="noreferrer"]/@title').extract_first()
            item["url"] = i.xpath('.//a[@rel="noreferrer"]/@href').extract_first()
            item["content"] = i.xpath('.//div[contains(@class,"threadlist_abs threadlist_abs_onlyline ")]/text()').extract_first()

            if item["url"] is not 'javascript:;':

                item["url"] = "https://tieba.baidu.com" + (i.xpath('.//a[@rel="noreferrer"]/@href').extract_first())

                yield scrapy.Request(
                    item["url"],
                    callback=self.parse_detail,
                    meta={"item":copy.deepcopy(item)}
                )
                print(item["url"])
        next_url = "https:"+response.xpath("//a[contains(@class,'next pagination-item')]/@href").extract_first()
        print(type(next_url))
        print(next_url)
        if next_url is not None:
            yield scrapy.Request(
                next_url,callback=self.parse
            )

    def parse_detail(self, response):
        print("detail")
        print(response.url)
        item = response.meta["item"]

        dict1={}
        floors = response.xpath("//div[contains(@class,'l_post l_post_bright j_l_post clearfix')]")
        for floor in floors:

            index=str(self.i)
            dict1[index] = {}
            dict1[index]["name"]= floor.xpath('.//a[contains(@class,"p_author_name j_user_card")]/text()').extract_first()

            dict1[index]["user_img"]= floor.xpath('.//a[contains(@class,"p_author_face ")]/img/@src').extract_first()
            dict1[index]["floor_comment"]={}
            dict1[index]["floor_comment"]["img"] = floor.xpath('.//div[contains(@class,"d_post_content j_d_post_content" )]/img/@src').extract()
            dict1[index]["floor_comment"]["content"] = floor.xpath('.//div[contains(@class,"d_post_content j_d_post_content ")]/text()').extract_first()
            self.i = self.i+1
        item["floor"]=(dict1)

        next_url = response.xpath("//a[text()='下一页']/@href").extract_first()

        if next_url is not None:
            next_url = "https://tieba.baidu.com"+response.xpath("//a[text()='下一页']/@href").extract_first()
            print(999999999999999999)
            print(next_url)
            print(999999999999999999)
            yield scrapy.Request(
                next_url,
                meta={"item":copy.deepcopy(item)},
                callback=self.parse_detail
            )

        # print(item)
        yield item
