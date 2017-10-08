#!/usr/bin/python
# -*- coding: utf-8 -*-
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.etree import ElementTree
from xml.dom import minidom
from pybtex.database import *
import codecs, sys

#Gets author from bib entry:
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

#Adds a bib entry to the xml:
def addEntriesToPaper(top, entry, i, basebibkey):
	fields = entry.fields
	title = SubElement(top, 'title')
	title.text = fields['title']
	authors = getAuthors(entry)
	for author in authors:
		a = SubElement(top, 'author')
		a.text = author
	elorder = ['booktitle', 'month', 'year', 'pages', 'address', 'publisher', 'url', 'bibtype', 'bibkey']
	backup = {}
	backup['publisher'] = u'Sociedade Brasileira de Computação'
	backup['bibtype'] = u'InProceedings'
	backup['bibkey'] = basebibkey+':'+"{0:0=2d}".format(i)
	for el in elorder:
		a = SubElement(top, el)
		if el in fields:
			a.text = fields[el]		
		else:
			a.text = backup[el]

#Creates the xml's header:
def getProceedingsHeader(top, volumeid, volumever, basebibkey):
	paper = SubElement(top, 'paper')
	paper.set('id', str(volumever))
	
	title = SubElement(paper, 'title')
	title.text = 'Proceedings of the 11th Brazilian Symposium in Information and Human Language Technology'
	
	editor = SubElement(paper, 'editor')
	editor.text = 'Gustavo Henrique Paetzold'
	
	editor = SubElement(paper, 'editor')
	editor.text = 'Vládia Pinheiro'.decode('utf8')
	
	month = SubElement(paper, 'month')
	month.text = 'October'
	
	year = SubElement(paper, 'year')
	year.text = '2017'
	
	address = SubElement(paper, 'address')
	address.text = 'Uberlândia, Brazil'.decode('utf8')
	
	publisher = SubElement(paper, 'publisher')
	publisher.text = 'Sociedade Brasileira de Computação'.decode('utf8')
	
	url = SubElement(paper, 'url')
	url.text = 'http://www.aclweb.org/anthology/'+volumeid+'-'+str(volumever).decode('utf8')
	
	bibtype = SubElement(paper, 'bibtype')
	bibtype.text = 'book'
	
	bibkey = SubElement(paper, 'bibkey')
	bibkey.text = basebibkey
	return paper

#Makes the xml file pretty:
def prettify(elem):
	rough_string = ElementTree.tostring(elem, 'utf-8')
	reparsed = minidom.parseString(rough_string)
	return reparsed.toprettyxml(indent="  ")

#Get parameters:
fbib = sys.argv[1]
forder = sys.argv[2]
basebibkey = sys.argv[3]
volumeid = sys.argv[4]
volumever = int(sys.argv[5])
outfile = sys.argv[6]

#Get id order:
idorder = [line.strip() for line in open(forder)]

#Create volume node:
vol = Element('volume')
vol.set('id', volumeid+'-'+str(volumever))

#Add proceedings header:
header = getProceedingsHeader(vol, volumeid, volumever, basebibkey)

#Read each paper and add it to the xml:
print fbib
d = parse_file(fbib, bib_format='bibtex')
for i, e in enumerate(idorder):
	paper = SubElement(vol, 'paper')
	paper.set('id', str(volumever+i+1))
	addEntriesToPaper(paper, d.entries[e], i+1, basebibkey)

#Write xml file:
o = codecs.open(outfile, 'w', encoding='utf8')
o.write(prettify(vol))
o.close()