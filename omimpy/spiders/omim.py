#!/usr/bin/env python
#coding=utf-8

import re
import scrapy

class omimSpider(scrapy.Spider):
    name = 'omim'
    # start_urls = ['http://www.omim.org/entry/601186']
    # start_urls = ['http://127.0.0.1:8000/omim_2.html']
    start_urls = ['http://127.0.0.1:8000/omim_1.html']

#     def __init__(self, filename=None):
#         URL_BASE = 'https://www.omim.org/entry/'
#         if filename:
#             with open(filename, 'r') as f:
#                 omim_ids = [re.findall(r'\((\d+)\)', line )  for line in f if line.startswith('chr') ]
#                 self.start_urls = [ '{0}{1}'.format(URL_BASE, int(omim[0]) ) for omim in omim_ids if omim]
#                 print self.start_urls
# #                 self.start_urls = ['https://www.omim.org/entry/131244']
    def parse(self, response):
        clinical_synopsis = ['Inheritance', 'Growth', 'HeadAndNeck', 'Cardiovascular', 'Respiratory', 'Chest', 'Abdomen',
                            'Genitourinary', 'Skeletal', 'SkinNailsHair', 'MuscleSoftTissue', 'Neurologic', 'MetabolicFeatures',
                            'EndocrineFeatures', 'Hematology', 'Immunology', 'PrenatalManifestations', 'Neoplasia',
                            'LaboratoryAbnormalities', 'Miscellaneous', 'MolecularBasis']
        # omim_db = { "disease":[], "gene": [] }
        # omim_disease = {}
        main_div = response.xpath('//*[@id="content"]/div[contains(@class, "hidden-print")]/div[2]/div[3]')
        gene_pheno = {}
        gene_pheno['url'] = response.url
        gene_pheno['omim_num'] = main_div.xpath('div[1]/div[1]/div[2]/span/span/span[contains(@class, "mim-highlighted")]/text()').extract_first().strip()
        gene_pheno['omim_type'] = main_div.xpath('div[1]/div[1]/div[2]/span/span/span/strong/text()').extract_first().strip()

        if gene_pheno['omim_type'] == "#":
            omim_title = main_div.xpath('div[1]/div[2]/h3/span/text()').extract_first().strip()
            omim_title = omim_title.split(";")
            gene_pheno['title'] = omim_title[0].strip()
            gene_pheno['title_abbr'] = omim_title[1].strip()
        # extract from Description
        # if 'Description' in main_div.text:
        #     gene_pheno['description'] = ','.join(response.xpath('//div[@id="descriptionFold"]/span/p/text()').extract().strip() )

        if main_div.xpath('.//table[contains(@class, "small")]'):
            gene_pheno['relations'] = []
            tr = main_div.xpath('.//table[contains(@class, "small")]/tbody/tr')

            for tb_record in tr:
                    phenotype = {}
                    phenotype['location'] = tb_record.xpath('td')[0].xpath('span/a/text()').extract_first().strip()
                    phenotype['phenotype'] = tb_record.xpath('td')[1].xpath('span/text()').extract_first().strip()
                    phenotype['pheno_mim'] = tb_record.xpath('td')[2].xpath('span/a/span[contains(@class, "mim-highlighted")]/text()').extract_first().strip()
                    phenotype['inherit'] = tb_record.xpath('td')[3].xpath('span/abbr/text()').extract_first().strip()
                    phenotype['mapping_key'] = tb_record.xpath('td')[4].xpath('span/abbr/text()').extract_first().strip()
                    if len(tb_record.xpath('td')) > 5:
                        phenotype['gene_related'] = tb_record.xpath('td')[5].xpath('span/text()').extract_first().strip()
                    if len(tb_record.xpath('td')) > 6:
                        phenotype['gene_mim'] = tb_record.xpath('td')[6].xpath('span/a/text()').extract_first().strip()
                    gene_pheno['relations'].append(phenotype)

        print (main_div.xpath('.//div[contains(@class, "btn-group")]/a/text()').extract_first().strip())

        if main_div.xpath('.//div[contains(@class, "btn-group")]/a/text()').extract_first().strip() == 'Clinical Synopsis' :
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
                            synopsis_name = tmp_system_num[0].xpath('span/em/text()').extract_first().strip()
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
                            synopsis_name = item.xpath('div[1]/span/em/text()').extract_first().strip()
                            synopsis[synopsis_name] = []
                            synopsis_path = item.xpath('div[2]/span/text()').extract()
                            for item in synopsis_path:
                                if item != ' ':
                                    item_cut = item.replace("\r\n","").replace("-","")
                                    item_cut = item_cut.strip()
                                    synopsis[synopsis_name].append(item_cut)
                            gene_pheno['clinical'][ system ].append(synopsis)

        return gene_pheno
