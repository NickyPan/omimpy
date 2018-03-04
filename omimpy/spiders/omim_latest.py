#!/usr/bin/env python
#coding=utf-8

import re
import scrapy

class omimSpider(scrapy.Spider):
    name = 'omim_latest'
    URL_BASE = 'https://omim.org/search/?index=entry&search=prefix%3A%23&sort=number+asc&limit=200&start='

    def start_requests(self):
        for num in range(1,27):
            page_url = self.URL_BASE + str(num)
            yield scrapy.Request(url=page_url, callback = self.parse)

    def parse(self, response):

        main_div = response.xpath('//*[@id="content"]/div[contains(@class, "hidden-print")]')
        num_list = {}
        num_list['list'] = []
        result_list = main_div.xpath('div')
        for result in result_list:
            if len(result.xpath('div[2]/a[1]/span/span')) > 0:
                omim_num = result.xpath('div[2]/a[1]/span/span/text()').extract()
                omim_num = omim_num[1].strip()
                omim_num = omim_num.split('.')[0]
                num_list['list'].append(omim_num)

        return num_list
