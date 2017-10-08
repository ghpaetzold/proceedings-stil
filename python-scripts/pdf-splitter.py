#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyPDF2 import PdfFileReader, PdfFileWriter
import os, sys

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
fproceedings = sys.argv[1]
flengths = sys.argv[2]
forder = sys.argv[3]
first_page = int(sys.argv[4])
short_papers = int(sys.argv[5])
long_papers = int(sys.argv[6])
volumeid = sys.argv[7]
volumever = int(sys.argv[8])
outfolder = sys.argv[9]
outpages = sys.argv[10]

#Open proceedings pdf:
pdf = PdfFileReader(open(fproceedings, 'rb'))

#Read id sizes:
sizes = readLengths(flengths)

#Read id order:
order = [line.strip() for line in open(forder)]

#Open file for page ranges:
o = open(outpages, 'w')

#Extract short paper pdfs:
curr_page = first_page-1
for i in range(0, short_papers):
	#Get paper id and size:
	paperid = order[i]
	papersize = sizes[paperid]
	
	#Mark first page:
	firstpage = curr_page+1
	
	#Create a pdf writer:
	output = PdfFileWriter()
	stream = open(outfolder+'/'+volumeid+'-'+str(volumever+i+1)+'.pdf', 'wb')
	
	#Mount pdf of paper:
	for j in range(0, papersize):
		output.addPage(pdf.getPage(curr_page+j))
	curr_page += papersize
		
	#Mark last page:
	lastpage = curr_page
	
	#Write the paper:
	output.write(stream)
	stream.close()
	
	#Write page range:
	o.write(paperid+'\t'+str(firstpage)+'-'+str(lastpage)+'\n')
	
#Extract long paper pdfs:
curr_page += 1
for k in range(0, long_papers):
	#Get paper id and size:
	i = k+short_papers
	paperid = order[i]
	papersize = sizes[paperid]
	
	#Mark first page:
	firstpage = curr_page+1
	
	#Create a pdf writer:
	output = PdfFileWriter()
	stream = open(outfolder+'/'+volumeid+'-'+str(volumever+i+1)+'.pdf', 'wb')
	
	#Mount pdf of paper:
	for j in range(0, papersize):
		output.addPage(pdf.getPage(curr_page+j))
	curr_page += papersize
		
	#Mark last page:
	lastpage = curr_page
	
	#Write the paper:
	output.write(stream)
	stream.close()
	
	#Write page range:
	o.write(paperid+'\t'+str(firstpage)+'-'+str(lastpage)+'\n')
	
#Close page range file:
o.close()