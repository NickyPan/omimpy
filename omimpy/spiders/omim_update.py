#!/usr/bin/env python
#coding=utf-8

import re
import scrapy
import datetime

dataNow = datetime.datetime.now()

class updateSpider(scrapy.Spider):
    name = 'omim-update'
    URL_BASE = 'https://www.omim.org/statistics/updates/'

    def start_requests(self):
        for num in range(1, dataNow.month+1):
            page_url = self.URL_BASE + str(dataNow.year) + '/' + str(num)
            yield scrapy.Request(url=page_url, callback = self.parse)

    def parse(self, response):

        main_div = response.xpath('//*[@id="content"]/div[contains(@class, "hidden-print")]')
        num_list = []

        row_list = main_div.xpath('div')
        for row in row_list:
            numPath = row.xpath('div[1]/a')
            typePath = numPath.xpath('..//span/strong/span/')
            if typePath:
                typeInfo = typePath.xpath('..//text()').extract().strip()
                if typeInfo == '#':
                    numinfo = numPath.xpath('..//@href').extract().strip()
                    updateNum = numinfo.split('/')[2]
                    num_list.append(updateNum)

        return num_list
