#!/usr/bin/python
# -*- coding: utf-8 -*-
from pybtex.database import *
import codecs, sys
import lib.latex as latex

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

#Gets authors from bib entry:
def getAuthors(entry):
	result = []
	persons = entry.persons['author']
	for person in persons:
		name = ' '.join(person.first_names).strip() + ' '
		if len(person.middle_names)>0:
			name += ' '.join(person.middle_names).strip() + ' '
		name += ' '.join(person.last_names).strip()
		result.append(name.strip())
	return result

#Creates a \ppstil for the latex:
def getPPStil(id, entry, paper_length):
	fields = entry.fields
	title = fields['title']
	authors = ' and '.join(getAuthors(entry)).strip()
	newstring = r'\ppstil{'+str(id)+'}{'+str(paper_length)+'}{'+title+'}{'+authors+'}'
	return newstring

#Get input files
fbib = sys.argv[1]
flengths = sys.argv[2]
fpps = sys.argv[3]
fidorder = sys.argv[4]
	
#Load latex converter:
latex.register()

#Read paper lengths:
lengths = readLengths(flengths)

#Open target files:
o1 = codecs.open(fpps, 'w', encoding='utf8')
o2 = codecs.open(fidorder, 'w', encoding='utf8')

#Read each paper and save \ppstil:
d = parse_file(fbib, bib_format='bibtex')
for i, e in enumerate(sorted(d.entries)):
	ppstil = getPPStil(e, d.entries[e], lengths[e])
	o1.write(ppstil.encode("latex").strip()+'\n')
	o2.write(str(e)+'\n')
	
#Close target files:
o1.close()
o2.close()