#!/usr/bin/env python
import json
import codecs
import sys
from operator import itemgetter

# entries = []
# with open('omim_cn.txt','r') as f:
#     for line in f:
#         entries.append(line.split('\t')[0])

# load_entries = json.load(open('./omimpy/omim_details_sorted.json'))
# loaded = []
# for item in load_entries:
#     if item['omim_num'] not in loaded:
#         loaded.append(item['omim_num'])

# # loaded.sort()
# print (len(load_entries))
# print (loaded[-1])
# latest_entries = json.load(open('./omimpy/omim_latest_entries.json'))
# print (latest_entries[-1])

# need_to_scrapy = []
# for entry in latest_entries:
#     if entry not in loaded:
#         if entry not in need_to_scrapy:
#             need_to_scrapy.append(entry)

# print (len(need_to_scrapy))
# print (need_to_scrapy)

# with open('./omimpy/need_to_scrapy.json', 'w') as outfile:
#     json.dump(need_to_scrapy, outfile)

# toBeLoad = []
# for item in entries:
#     if item not in loaded:
#         toBeLoad.append(item)

# print (len(entries))
# print (len(load_entries))
# print (len(toBeLoad))

# latest_entries = []
# with codecs.open('latest_omim.txt','r',encoding='utf8') as f:
#     for line in f:
#         latest_entries.append(line.split(':')[1].split(' # ')[1].split('. ')[0])
# print (len(latest_entries))

# with open('latest_to_scrapy.json', 'w') as outfile:
#     json.dump(latest_entries, outfile)

# latest_entries = []
# latest_list = json.load(open('./omimpy/omim_list.json'))
# for list in latest_list:
#     for entry in list['list']:
#         if entry not in latest_entries:
#             latest_entries.append(entry)
# print (len(latest_entries))
# with open('./omimpy/omim_latest_entries.json', 'w') as outfile:
#     json.dump(latest_entries, outfile)

# part1 = json.load(open('./omimpy/omim_part1_3674.json'))
# part2 = json.load(open('./omimpy/omim_part2_590.json'))
# part3 = json.load(open('./omimpy/omim_part3.json'))
# part4 = json.load(open('./omimpy/omim_part4.json'))
# part5 = json.load(open('./omimpy/omim_part5_5_20180304.json'))
# omim_latest = json.load(open('./omimpy/omim_details_latest.json'))
# omim_latest = omim_latest + part5
# print (len(omim_latest))
# with open('./omimpy/omim_details_latest.json', 'w') as outfile:
#     json.dump(omim_latest, outfile)

# # find key value
# latest_entries = json.load(open('./omim_details_latest.json'))
# key_str = sys.argv[1]
# key_arr = []
# key_arr.append("Location\tPhenotype\tPhenotype MIM number\tInheritance\tPhenotype mapping key\tGene/Locus\tGene/Locus MIM number")

# def collect_val(dictionary):
#     for relation in dictionary:
#         relation_str = '\t'.join(str(x) for x in relation.values())
#         if relation_str not in key_arr:
#             key_arr.append(relation_str)

# for item in latest_entries:
#     for item_str in item.values():
#         if key_str in item_str and 'relations' in item:
#             collect_val(item['relations'])
#             pass
#         elif 'clinical' in item:
#             for cli_item in item['clinical'].values():
#                 for cli_val in cli_item:
#                     if isinstance(cli_val, dict):
#                         for cli_val in cli_val.values():
#                             if key_str in cli_val and 'relations' in item:
#                                 collect_val(item['relations'])
#                                 pass
#                     elif isinstance(cli_val, list):
#                         if key_str in cli_val and 'relations' in item:
#                             collect_val(item['relations'])
#                             pass
# print(len(key_arr))
# key_out = '\n'.join([str(x) for x in key_arr])
# with open('key_entries.txt', 'w') as f:
#     print(key_out, file=f)

# print ("搜索" + key_str + "完成")
