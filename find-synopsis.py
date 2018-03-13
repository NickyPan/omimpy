#!/usr/bin/env python
import json
import codecs
import sys
from operator import itemgetter

latest_entries = json.load(open('./omim_details_latest.json'))
# latest_entries = [{"url": "https://www.omim.org/entry/100100", "omim_num": "100100", "omim_type": "#", "alt_names": ["ABDOMINAL MUSCLES, ABSENCE OF, WITH URINARY TRACT ABNORMALITY AND CRYPTORCHIDISM", "EAGLE-BARRETT SYNDROME;  EGBRS"], "title": "PRUNE BELLY SYNDROME", "title_abbr": "PBS", "text": "A number sign (#) is used with this entry because of evidence that prune belly syndrome (PBS) is caused by homozygous mutation in the CHRM3 gene () on chromosome 1q43. One such family has been reported.", "description": "In its rare complete form, 'prune belly' syndrome comprises megacystis (massively enlarged bladder) with disorganized detrusor muscle, cryptorchidism, and thin abdominal musculature with overlying lax skin (summary by).", "relations": [{"location": "1q43", "phenotype": "?Prune belly syndrome", "pheno_mim": "100100", "inherit": "AR", "mapping_key": "3", "gene_related": "CHRM3", "gene_mim": "118494"}], "clinical": {"Inheritance": ["Autosomal recessive"], "HeadAndNeck": [{"Eyes": ["Impaired pupillary constriction to light"]}, {"Mouth": ["Dry mouth"]}], "Cardiovascular": [{"Heart": ["Congenital heart defect"]}, {"Vascular": ["Patent ductus arteriosus"]}], "Chest": [{"Ribs Sternum Clavicles & Scapulae": ["Flared ribs", "Pectus excavatum", "Pectus carinatum"]}], "Abdomen": [{"External Features": ["Absent abdominal musculature", "Visible intestinal pattern (socalled 'prune belly')", "Thin, lax, protruding abdominal wall"]}, {"Gastrointestinal": ["Imperforate anus"]}], "Genitourinary": [{"Internal Genitalia (Male)": ["Cryptorchidism"]}, {"Kidneys": ["Hydronephrosis"]}, {"Ureters": ["Posterior urethral valves", "Hydroureter"]}, {"Bladder": ["Distended bladder", "Fetal urinary tract obstruction"]}], "Skeletal": [{"Pelvis": ["Congenital hip dislocation"]}, {"Feet": ["Clubfoot"]}], "SkinNailsHair": [{"Skin": ["Wrinkled abdominal skin"]}], "PrenatalManifestations": [{"Amniotic Fluid": ["Oligohydramnios"]}], "MolecularBasis": ["Caused by mutation in the muscarinic cholinergic receptor3 gene (CHRM3,", ")"]}, "created_time": "6/4/1986", "created_author": "Victor A. McKusick", "last_edit": "07/30/2015", "last_edit_author": "carol"}, {"url": "https://www.omim.org/entry/100300", "omim_num": "100300", "omim_type": "#", "alt_names": ["AOS", "ABSENCE DEFECT OF LIMBS, SCALP, AND SKULL", "CONGENITAL SCALP DEFECTS WITH DISTAL LIMB REDUCTION ANOMALIES", "APLASIA CUTIS CONGENITA WITH TERMINAL TRANSVERSE LIMB DEFECTS"], "title": "ADAMS-OLIVER SYNDROME 1", "title_abbr": "AOS1", "text": "A number sign (#) is used with this entry because of evidence that Adams-Oliver syndrome-1 (AOS1) is caused by heterozygous mutation in the ARHGAP31 gene () on chromosome 3q13.", "description": "Adams-Oliver syndrome (AOS) is a rare developmental disorder defined by the combination of aplasia cutis congenita of the scalp vertex and terminal transverse limb defects (e.g., amputations, syndactyly, brachydactyly, or oligodactyly). In addition, vascular anomalies such as cutis marmorata telangiectatica congenita, pulmonary hypertension, portal hypertension, and retinal hypervascularization are recurrently seen. Congenital heart defects have been estimated to be present in 20% of AOS patients; reported malformations include ventricular septal defects, anomalies of the great arteries and their valves, and tetralogy of Fallot (summary by).Other autosomal dominant forms of Adams-Oliver syndrome include AOS3 (), caused by mutation in the RBPJ gene () on chromosome 4p15; AOS5 (), caused by mutation in the NOTCH1 gene () on chromosome 9q34; and AOS6 (), caused by mutation in the DLL4 gene () on chromosome 5q32.Autosomal recessive forms of Adams-Oliver syndrome include AOS2 (), caused by mutation in the DOCK6 gene () on chromosome 19p13, and AOS4 (), caused by mutation in the EOGT gene () on chromosome 3p14.", "relations": [{"location": "3q13.32-q13.33", "phenotype": "Adams-Oliver syndrome 1", "pheno_mim": "100300", "inherit": "AD", "mapping_key": "3", "gene_related": "ARHGAP31", "gene_mim": "610911"}], "clinical": {"Inheritance": ["Autosomal dominant"], "HeadAndNeck": [{"Head": ["Microcephaly", "Aplasia cutis congenita over parietal area"]}, {"Eyes": ["Esotropia", "Microphthalmia"]}, {"Mouth": ["Cleft lip", "Cleft palate"]}], "Cardiovascular": [{"Heart": ["Congenital heart defects (in some patients)", "Ventricular septal defect", "Atrial septal defect", "Pulmonary valve stenosis", "Tetralogy of Fallot"]}, {"Vascular": ["Pulmonary artery stenosis", "Pulmonary hypertension", "Vascular malformations"]}], "Chest": [{"External Features": ["Poland sequence"]}, {"Breasts": ["Accessory nipples"]}], "Genitourinary": [{"Internal Genitalia (Female)": ["Imperforate vaginal hymen"]}], "Skeletal": [{"Skull": ["Skull defect at vertex"]}, {"Limbs": ["Terminal transverse defects, asymmetric (minimal to absence of a limb)"]}, {"Hands": ["Brachydactyly", "Syndactyly"]}, {"Feet": ["Syndactyly", "Malformed toes", "Talipes equinovarus"]}], "SkinNailsHair": [{"Skin": ["Aplasia cutis congenita over posterior parietal area", "Aplasia cutis congenita on trunk or limbs", "Cutis marmorata", "Thin, hyperpigmented skin", "Dilated scalp veins radiating from periphery of scalp defect"]}, {"Nails": ["Hypoplastic nails"]}, {"Hair": ["Singlemultiple roundoval areas of alopecia in parietal area"]}], "Neurologic": [{"Central Nervous System": ["Encephalocele (uncommon)", "Mental retardation (uncommon)", "Developmental delay", "Seizures", "Hypotonia", "Enlarged ventricles", "Periventricular calcifications", "Periventricular leukomalacia (reported in 2 patients)", "Hypoplasia of the corpus callosum", "Cortical dysplasia", "Pachygyria", "Polymicrogyria"]}], "Miscellaneous": ["Variable phenotype", "Phenotype is classically defined as aplasia cutis and transverse limb defects"], "MolecularBasis": ["Caused by mutation in the Rho GTPaseactivating protein 31 gene (ARHGAP31,", ")"]}, "created_time": "6/4/1986", "created_author": "Victor A. McKusick", "last_edit": "11/21/2017", "last_edit_author": "carol"}]
key_str = sys.argv[1]
key_arr = []
key_arr.append("Location\tPhenotype\tPhenotype MIM number\tInheritance\tPhenotype mapping key\tGene/Locus\tGene/Locus MIM number")

def collect_val(dictionary):
    for relation in dictionary:
        relation_str = '\t'.join(str(x) for x in relation.values())
        if relation_str not in key_arr:
            key_arr.append(relation_str)

for item in latest_entries:
    if 'relations' in item and 'clinical' in item:
        if key_str in item['clinical']:
            collect_val(item['relations'])
        else:
            for item_cli in item['clinical'].values():
                for item_key in item_cli:
                    if key_str in item_key:
                        collect_val(item['relations'])
    else:
        pass

file_name = key_str + '_entries.txt'
key_out = '\n'.join([str(x) for x in key_arr])
with open(file_name, 'w') as f:
    print(key_out, file=f)

print ("搜索 " + key_str + " 完成，共 " + str(len(key_arr)-1) + " 条")
