#!/usr/bin/env python
#coding=utf-8

import re
import scrapy
import json
import datetime
# from omimpy.items import OmimItem, updatedItem

dataNow = datetime.datetime.now()
curYear = dataNow.year
curMonth = dataNow.month

class omimSpider(scrapy.Spider):
    name = 'omim'
    # URL_BASE = 'http://127.0.0.1:8000/'
    MAIN_URL = 'https://www.omim.org/entry/'
    UPDATE_URL = 'https://www.omim.org/statistics/updates/'
    # entries = json.load(open('need_to_scrapy.json'))
    f = open ('updated.log')
    lastLine = f.readlines()[-1].strip()
    f.close()
    lastUpdatedYear = int(lastLine.split('\t')[1])
    lastUpdatedMonth = int(lastLine.split('\t')[2])

    if (lastUpdatedYear == curYear and lastUpdatedMonth >= curMonth) or lastUpdatedYear > curYear:
        scrapy.exceptions.CloseSpider(reason='updated list is the latest!')

    num_list = []

    def start_requests(self):
        for num in range(self.lastUpdatedMonth, curMonth+1):
            updated_url = self.UPDATE_URL + str(curYear) + '/' + str(num)
            yield scrapy.Request(url=updated_url, callback = self.parse_updated)

        # for page in self.entries:
        #     main_url = self.MAIN_URL + page
        #     yield scrapy.Request(url=main_url, callback = self.parse_item)

    def parse_updated(self, response):

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
                    main_url = self.MAIN_URL + updateNum
                    yield scrapy.Request(url=main_url, callback = self.parse_item)
                    # yield Request(main_url, callback=self.parse_item,
                    #         meta={'item': item, 'agent_urls' agent_urls})

        # return num_list

    def parse_item(self, response):
        clinical_synopsis = ['Inheritance', 'Growth', 'HeadAndNeck', 'Cardiovascular', 'Respiratory', 'Chest', 'Abdomen',
                            'Genitourinary', 'Skeletal', 'SkinNailsHair', 'MuscleSoftTissue', 'Neurologic', 'MetabolicFeatures',
                            'EndocrineFeatures', 'Hematology', 'Immunology', 'PrenatalManifestations', 'Neoplasia',
                            'LaboratoryAbnormalities', 'Miscellaneous', 'MolecularBasis']
        # omim_db = { "disease":[], "gene": [] }
        # omim_disease = {}
        # gene_pheno = OmimItem()
        gene_pheno = {}
        main_div = response.xpath('//*[@id="content"]/div[contains(@class, "hidden-print")]/div[2]/div[3]')
        gene_pheno['url'] = response.url

        # extract from omim id
        gene_pheno['omim_num'] = gene_pheno['url'].partition("entry/")[-1]
        # if gene_pheno['omim_num']:
        #     gene_pheno['omim_num'] = gene_pheno['omim_num'].strip()
        # else:
        #     gene_pheno['omim_num'] = main_div.xpath('div[1]/div[1]/div[2]/span/span/text()').extract_first().strip()
        gene_pheno['omim_type'] = main_div.xpath('div[1]/div[1]/div[2]/span/span/span/strong/text()').extract_first().strip()

        if gene_pheno['omim_type'] == "#":
            # extract from Alternative titles and symbols
            alt_names = main_div.xpath('.//*[@id="alternativeTitles"]/following-sibling::div[2]/h4/span/text()').extract()
            gene_pheno['alt_names'] = []
            for alt in alt_names:
                gene_pheno['alt_names'].append(alt.strip())

            # extract from Description
            omim_title = main_div.xpath('div[1]/div[2]/h3/span/text()').extract_first()
            if omim_title:
                omim_title = omim_title.strip()
                omim_title = omim_title.split(";")
                gene_pheno['title'] = omim_title[0].strip()
                if len(omim_title) > 1:
                    gene_pheno['title_abbr'] = omim_title[1].strip()

            # extract from text
            if main_div.xpath('.//*[@id="textFold"]'):
                text_info = main_div.xpath('.//*[@id="textFold"]/span/p/text()').extract()
                gene_pheno['text'] = ''
                for text in text_info:
                    gene_pheno['text'] += text.strip()

            # extract from Description
            if main_div.xpath('.//div[@id="descriptionFold"]'):
                description = main_div.xpath('.//div[@id="descriptionFold"]/span/p/text()').extract()
                gene_pheno['description'] = ''
                for des in description:
                    gene_pheno['description'] += des.strip()

            # extract from phenotype-gene relationships
            if main_div.xpath('.//table[contains(@class, "small")]'):
                gene_pheno['relations'] = []
                tr = main_div.xpath('.//table[contains(@class, "small")]/tbody/tr')
                for tb_record in tr:
                        phenotype = {}
                        # if len(main_div.xpath('.//table[contains(@class, "small")]').xpath('.//td[@rowspan]')) > 0:
                        #     phenotype['location'] = main_div.xpath('.//table[contains(@class, "small")]').xpath('.//td[@rowspan]').xpath('span/a/text()').extract_first().strip()
                        #     print (1, phenotype['location'])
                        # else:
                        phenotype['location'] = tb_record.xpath('td')[0].xpath('span/a/text()').extract_first().strip()
                        print (2, phenotype['location'])
                        # if len(tb_record.xpath('.//td[@rowspan]')) > 0:
                        #     index = 1
                        # else:
                        #     index = 0
                        phenotype['phenotype'] = tb_record.xpath('td')[1].xpath('span/text()').extract_first().strip()
                        phenotype['pheno_mim'] = tb_record.xpath('td')[2].xpath('span/a/span[contains(@class, "mim-highlighted")]/text()').extract_first()
                        if phenotype['pheno_mim']:
                            phenotype['pheno_mim'] = phenotype['pheno_mim'].strip()
                        else:
                            phenotype['pheno_mim'] = tb_record.xpath('td')[2].xpath('span/a/text()').extract_first().strip()
                        phenotype['inherit'] = tb_record.xpath('td')[3].xpath('span/abbr/text()').extract_first()
                        if phenotype['inherit']:
                            phenotype['inherit'] = phenotype['inherit'].strip()
                        phenotype['mapping_key'] = tb_record.xpath('td')[4].xpath('span/abbr/text()').extract_first().strip()
                        if len(tb_record.xpath('td')) > 5:
                            phenotype['gene_related'] = tb_record.xpath('td')[5].xpath('span/text()').extract_first().strip()
                        if len(tb_record.xpath('td')) > 6:
                            phenotype['gene_mim'] = tb_record.xpath('td')[6].xpath('span/a/text()').extract_first().strip()
                        gene_pheno['relations'].append(phenotype)

            # extract from clinical synopsis
            if main_div.xpath('.//*[@id="clinicalSynopsisFold"]'):
                gene_pheno['clinical'] = {}
                for system in clinical_synopsis:
                    tmp_path = '//*[@id="cs' + system + '"]'
                    if main_div.xpath(tmp_path):
                        gene_pheno['clinical'][ system ] = []
                        tmp_div_num = response.xpath(tmp_path + '/div[2]/div')
                        if len(tmp_div_num) == 1:
                            tmp_system_num = response.xpath(tmp_path + '/div[2]/div/div')
                            if len(tmp_system_num) > 1:
                                synopsis = {}
                                synopsis_name = tmp_system_num[0].xpath('span/em/text()').extract_first()
                                if synopsis_name:
                                    synopsis_name = synopsis_name.strip()
                                else:
                                    synopsis_name = "null"
                                synopsis[synopsis_name] = []
                                synopsis_path = tmp_system_num[1].xpath('span/text()').extract()
                                for item in synopsis_path:
                                    if item != ' ':
                                        item_cut = item.replace("\r\n","").replace("-","")
                                        item_cut = item_cut.strip()
                                        synopsis[synopsis_name].append(item_cut)
                                gene_pheno['clinical'][ system ].append(synopsis)
                            else:
                                tmp_system_path = tmp_path + '/div[2]/div/span/text()'
                                synopsis_path = response.xpath(tmp_system_path).extract()
                                for item in synopsis_path:
                                    if item != ' ':
                                        item_cut = item.replace("\r\n","").replace("-","")
                                        item_cut = item_cut.strip()
                                        gene_pheno['clinical'][ system ].append(item_cut)
                        elif len(tmp_div_num) > 1:
                            for item in tmp_div_num:
                                synopsis = {}
                                synopsis_name = item.xpath('div[1]/span/em/text()').extract_first()
                                if synopsis_name:
                                    synopsis_name = synopsis_name.strip()
                                else:
                                    synopsis_name = "null"
                                synopsis[synopsis_name] = []
                                synopsis_path = item.xpath('div[2]/span/text()').extract()
                                for item in synopsis_path:
                                    if item != ' ':
                                        item_cut = item.replace("\r\n","").replace("-","")
                                        item_cut = item_cut.strip()
                                        synopsis[synopsis_name].append(item_cut)
                                gene_pheno['clinical'][ system ].append(synopsis)

            # extract from created time
            created_time = main_div.xpath('.//span[text()[contains(.,"Creation Date")]]/../following-sibling::div/span/text()').extract_first().strip()
            gene_pheno['created_time'] = created_time.split(":")[1].strip()
            gene_pheno['created_author'] = created_time.split(":")[0].strip()

            # extract from edit history
            if main_div.xpath('.//a[text()[contains(.," Edit History")]]'):
                edit_time = main_div.xpath('.//a[text()[contains(.," Edit History")]]/../../following-sibling::div/span/text()').extract_first().strip()
                gene_pheno['last_edit'] = edit_time.split(":")[1].strip()
                gene_pheno['last_edit_author'] = edit_time.split(":")[0].strip()

            # extract from phenotypic Series
            # if main_div.xpath('.//*[@id="phenotypicSeriesFold"]'):

            return gene_pheno

f = open("updated.log", "a")
logText = "updated\t" + str(curYear) + '\t' + str(curMonth)
f.write(logText)
f.close()
