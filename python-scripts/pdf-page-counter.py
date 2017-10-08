#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyPDF2 import PdfFileReader, PdfFileWriter
import os, sys

#Get parameters:
paperfolder = sys.argv[1]
sizesfile = sys.argv[2]

#Get papers in paper folder:
files = os.listdir(paperfolder)

#Open output stream:
o = open(sizesfile, 'w')

#Write paper sizes:
for file in files:
	pdfpath = paperfolder+file
	pdf = PdfFileReader(open(pdfpath, 'rb'))
	o.write(file.split('.')[0]+'\t'+str(pdf.getNumPages())+'\n')

#Close output stream:
o.close()
	