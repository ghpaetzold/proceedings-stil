#!/usr/bin/python
# -*- coding: utf-8 -*-
import codecs, sys
from pybtex.database import *

#Reads the paper's ranges from file:
def readRanges(franges):
	map = {}
	f = open(franges)
	for line in f:
		data = line.strip().split('\t')
		id = data[0]
		range = data[1]
		map[id] = range
		print id, range
	f.close()
	return map

#Reads the paper's lengths from file:
def readLengths(flengths):
	map = {}
	f = open(flengths)
	for line in f:
		data = line.strip().split('\t')
		id = data[0]
		length = int(data[1])
		map[id] = length
	f.close()
	return map

#Get parameters:
fbibnopages = sys.argv[1]
fidorder = sys.argv[2]
fpageranges = sys.argv[3]
basebibkey = sys.argv[4]
volumeid = sys.argv[5]
volumever = int(sys.argv[6])
fbibwithpages = sys.argv[7]

#Read id order:
order = [line.strip() for line in open(fidorder)]

#Read page ranges:
ranges = readRanges(fpageranges)

#Open output file stream:
o = codecs.open(fbibwithpages, 'w', encoding='utf8')

#Read each paper and fix it:
d = parse_file(fbibnopages, bib_format='bibtex')
for i, id in enumerate(order):
	#Add address:
	d.entries[id].fields['address'] = 'Uberlândia, Brazil'.decode('utf8')
	
	#Add pages:
	d.entries[id].fields['pages'] = ranges[id]
	
	#Add organization:
	d.entries[id].fields['organization'] = 'Sociedade Brasileira de Computação'.decode('utf8')
	
	#Add editors:
	d.entries[id].fields['editor'] = 'Gustavo Henrique Paetzold and Vládia Pinheiro'.decode('utf8')
	
	#Add correct ACL url:
	d.entries[id].fields['url'] = 'http://www.aclweb.org/anthology/'+volumeid+'-'+str(volumever+i+1)

#Write bib file with pages and other important information:	
o.write(d.to_string('bibtex')+'\n')
	
#Close output file:
o.close()