#!/usr/bin/env python
import json
import codecs
import sys
import re
from operator import itemgetter
import argparse
import random
import datetime

dataNow = datetime.datetime.now()

# optional args
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="input file")
parser.add_argument("-i2", "--sec_input", help="secondary input file")
parser.add_argument("-pheno", "--access_pheno", action="store_true", default=False, help="run acess pheno process")
parser.add_argument("-u", "--update_db", action="store_true", default=False, help="update old database")
parser.add_argument("-c", "--check_annovar", action="store_true", default=False, help="check annovar gene")
args = parser.parse_args()

if args.input:
    inputFile = args.input

if args.sec_input:
    secInputFile = args.sec_input

# entries = []
# annoGene = []
# with open(inputFile,'r') as f:
#     f.readline()
#     for line in f:
#         line = line.strip().split('\t')
#         gene = line[5]
#         if gene not in entries:
#             entries.append(gene)
#         try:
#             anno = line[7]
#             if anno not in annoGene:
#                 annoGene.append(anno)
#         except:
#             pass
# print ('omim:', len(entries))
# print ('omim-anno:', len(annoGene))


# idtGene = []
# with open('IDT-panel-symbol.txt','r') as f:
#     for line in f:
#         gene = line.strip()
#         if gene not in idtGene:
#             idtGene.append(gene)
# print ('IDT-panel:', len(idtGene))

# noIDT = []
# for gene in annoGene:
#     if gene not in idtGene:
#         noIDT.append(gene)
# print ('not in IDT-panel:', len(noIDT))

# noIDT2 = []
# for gene in noIDT:
#     if gene not in idtGene:
#         noIDT2.append(gene)
# print ('not in IDT-panel2:', len(noIDT2))
# geneStr = '\n'.join(noIDT2)

# load_entries = json.load(open('./omimpy/omim_details_sorted.json'))
# loaded = []
# for item in load_entries:
#     if item['omim_num'] not in loaded:
#         loaded.append(item['omim_num'])

def build_dict(seq, key):
    return dict((d[key], dict(d, index=index)) for (index, d) in enumerate(seq))

def sort_key(item):
    return item['omim_num']

# for item in latest_hgnc:
#     if 'omim_id' in item.keys() and len(item['omim_id']) > 1:
#         print (item['omim_id'])
def access_pheno(entries):
    relation_list = []
    rel_title = "location\tphenotype\tpheno_mim\tinherit\tmapping_key\tgene_related\tgene_mim\tannovar_gene"
    relation_list.append(rel_title)
    for entry in entries:
        if 'relations' in entry.keys():
            for relation in entry['relations']:
                if 'gene_related' in relation.keys() and relation['mapping_key'] == '3':
                    res_val=['None' if v is None else v for v in relation.values()]
                    rel_str = "\t".join( res_val )
                    if any(relation['gene_related'] == g['annovar_gene'] for g in annovar_gene):
                        rel_str += "\t" + relation['gene_related']
                    else:
                        geneIdx=next((i for i,d in enumerate(latest_hgnc) if 'omim_id' in d.keys() and relation['gene_mim'] in d['omim_id']), None)
                        if geneIdx:
                            if any(latest_hgnc[geneIdx]['symbol'] == g['annovar_gene'] for g in annovar_gene):
                                rel_str += "\t" + latest_hgnc[geneIdx]['symbol']
                            elif 'alias_symbol' in latest_hgnc[geneIdx].keys() and any(g['annovar_gene'] in latest_hgnc[geneIdx]['alias_symbol'] for g in annovar_gene):
                                tmp_str = ",".join( latest_hgnc[geneIdx]['alias_symbol'] )
                                rel_str += "\t" + tmp_str
                            elif 'prev_symbol' in latest_hgnc[geneIdx].keys() and any(g['annovar_gene'] in latest_hgnc[geneIdx]['prev_symbol'] for g in annovar_gene):
                                tmp_str = ",".join( latest_hgnc[geneIdx]['prev_symbol'] )
                                rel_str += "\t" + tmp_str
                    relation_list.append(rel_str)
    return relation_list

if args.update_db:
    latest_entries = json.load(open(inputFile))
    updated_entries = json.load(open(secInputFile))
    snpMatch = 0
    updated_entries.sort(key=sort_key)
    omimIdx = {}
    for index, value in enumerate(latest_entries):
        omimIdx[value['omim_num']] = index
    print (len(latest_entries))
    print (len(updated_entries))
    for item in updated_entries:
        if item['omim_num'] in omimIdx.keys():
            snpMatch += 1
            latest_entries[omimIdx[item['omim_num']]] = item
        else:
            latest_entries.append(item)
    print (snpMatch)
    match = 0
    for item in updated_entries:
        for index, value in enumerate(latest_entries):
            if value['omim_num'] == item['omim_num']:
                match += 1
                break
    print (match)
    if match == len(updated_entries):
        latest_entries.sort(key=sort_key)
    print (len(latest_entries))
    outFile = 'omim_latest-' + str(dataNow.year) + '0' + str(dataNow.month) + '.json'
    with open(outFile, 'w') as outfile:
        json.dump(latest_entries, outfile)
    print ('updated done!')

if args.access_pheno:
    if not args.update_db:
        latest_entries = json.load(open(inputFile))
    latest_hgnc = json.load(open('./protein-coding_gene.json'))['response']['docs']
    annovar_gene = json.load(open('./annovar_gene.json'))
    print (len(latest_entries))
    print (len(latest_hgnc))
    print (len(annovar_gene))
    results = access_pheno(latest_entries)
    print (len(results))
    res = "\n".join( results )
    output = 'omim_pheno_gene-' + str(dataNow.year) + '0' + str(dataNow.month) + '.txt'
    with open(output, 'w') as f:
        f.write(res)

if args.check_annovar:
    annovarGene = {}
    res = []
    with open(secInputFile) as old:
        firstLine = old.readline().strip()
        for line in old:
            varLine = line.strip()
            var = varLine.split('\t')
            if len(var) >= 8:
                annovarGene[var[5]] = var[7]

    with open(inputFile) as f:
        for line in f:
            varLine = line.strip()
            var = varLine.split('\t')
            if len(var) < 8 and var[5] in annovarGene.keys():
                print (var)
                var.append(annovarGene[var[5]])
                print (var)
            varLine = '\t'.join(var)
            res.append(varLine)
    outResults = '\n'.join(res)
    with open('omim_pheno_gene-fixed.txt', 'w') as text_file:
        text_file.write(outResults)
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
