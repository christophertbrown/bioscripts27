#!/usr/bin/env python2.7

"""
script for getting more info from blast output
given a blast .tsv file, query fasta file, and
database .tch or .fasta file
"""

import os
import sys
from tokyocabinet import hash

import ctbBio27.id2tax
from ctbBio27.check import check as check
from ctbBio27.fasta import iterate_fasta as parse_fasta

taxtch = True # use to get tax descriptions using tch files

def get_tax(hit, description):
    if 'Tax=' in description:
        tax = description.split('Tax=')[1].rsplit(' ', 1)[0]
    elif len(hit.split('|')) == 5:
        tax = hit.split('|')[1]
    else:
        tax = 'n/a'
    return tax

def headerid2desc(fasta, subset = False):
    db = {}
    for seq in parse_fasta(fasta):
        header = seq[0].split('>')[1]
        id, desc = header.split()[0], '%s len:%s' % (header, len(seq[1]))
        db[id] = desc
        if subset == False:
            db[id] = desc
        elif id in subset:
            db[id] = desc
    return db

def close_dict(database, dict):
    if database.rsplit('.', 1)[1] == 'tch':
        dict.close()

def get_subset(blast):
    subset = []
    for line in open(blast):
        id = line.strip().split('\t')[1]
        if id not in subset:
            subset.append(id)
    return set(subset)

def get_db(database, blast):
    if database.rsplit('.', 1)[1] == 'tch':
        id2desc = hash.Hash()
        id2desc.open(database)
        return id2desc
    else:
        return headerid2desc(database, get_subset(blast))

def get_info(blast, query, database):
    hit2description = get_db(database, blast)
    query2description = headerid2desc(query)
    if taxtch is True:
        taxtchs = id2tax.get_tchs()
    for line in open(blast):
        line = line.strip().split('\t')
        query, hit = line[0].split()[0], line[1]
        try:
            description = hit2description[hit]
        except KeyError:
            description = 'n/a'
        try:
            line.append(query2description[query])
        except KeyError:
            line.append('n/a')
        tax = get_tax(hit, description)
        if taxtch is True:
            query = id2tax.id2name(tax, taxtchs)
            tax = [tax, id2tax.find_hierarchy(query, taxtchs)]
        line.extend(tax)
        line.append(description)
        yield line
    if taxtch is True:
        [taxtchs[tch].close() for tch in taxtchs]
    close_dict(database, hit2description)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print('usage: blast2desc.py <blast.tsv> <query.fasta> <database.tch/fasta>')
        exit()
    blast, query, database = sys.argv[1], sys.argv[2], sys.argv[3]
    for hit in get_info(blast, query, database):
        print('\t'.join(hit))
