# Introduction:
	
This package contains a series of resources to help you compile the STIL/JDP proceedings.

# Content:

- latex-proceedings: Folder containing a latex project that allows you to generate the final PDF proceedings file with ease.
- python-scripts: Folder containing python scripts that will help you produce the proceedings and ACL files.
- conference-papers: Folder in which you will save the STIL and JDP pdf files.
- bibtex-files: Folder in which you will save the STIL and JDP bibtext files.
- acl-files: Folder in which you can save the PDF and XML files required for the ACL Anthology.
- auxiliary-files: Folder in which temporary and intermediate files produced by the scripts can be saved.

# Steps-by-step guide:

1. Count number of pages of STIL papers:

```python
python pdf-page-counter.py <paper_folder> <page_lengths_file>
```
	
2. Produce \ppstils for "latex-proceedings/stil.tex":

```python
python bib-to-ppstil.py <bib_nopages> <page_lengths_file> <ppstil_file> <id_order_file>
```
	
3. Organize \ppstils in the "stil" TEX file and update <id_order_file> to the same order as they appear in the TEX file.

4. Repeat steps 1, 2 and 3 for the proceedings "jdp" TEX file (don't forget to change "\ppstil" to "\ppjdp" when you do so).

5. Extract STIL and JDP pdf files for ACL Anthology from proceedings using the following command twice:

```python
python pdf-splitter.py <pdf_proceedings> <page_lengths_file> <id_order_file> <first_paper_page> <short_paper_count> <long_paper_count> <acl_conference_code> <acl_base_paper_id> <acl_out_folder> <page_range_file>
```

6. Generate bib files with page ranges for both STIL and JDP papers using the following command twice:

```python
python bibnopages-to-bibwithpages <bib_nopages> <id_order_file> <page_range_file> ACL-STIL:<current_year> <acl_conference_code> <acl_base_paper_id> <bib_withpages>
```

7. Concatenate the bib files with page ranges for STIL and JDP onto a <combined_bib_withpages> file.

8. Concatenate the id order files for STIL and JDP onto a <combined_order_file> file.

9. Generate the ACL XML file:

```python
python bib-to-aclxml.py <combined_bib_withpages> <combined_order_file> ACL-STIL:<current_year> <acl_conference_code> <acl_base_paper_id> <acl_xml_file>
```

# Important things to check:

- Check that no papers have the same ACL id by the end of the process.
- Check that all ACL papers have been correctly extracted from the proceedings main PDF.
- Check that the page ranges in the bibtex files have been correctly produced.
- Check that brazilian portuguese characters, such as "ã", "á" and "â" are being shown correctly PDF file.
- Check that the order of authors in the \ppstils and \ppjdps is the same as feature in the paper.

# Commands used for STIL 2017:

```python
python pdf-page-counter.py ../conference-papers/stil/ ../auxiliary-files/stil_paper_lengths.txt
python bib-to-ppstil.py ../bibtex-files/bib-stil-nopages.bib ../auxiliary-files/stil_paper_lengths.txt ../auxiliary-files/stil_ppstils_file.txt ../auxiliary-files/stil_paper_order.txt
python pdf-splitter.py ../proceedings.pdf ../auxiliary-files/stil_paper_lengths.txt ../auxiliary-files/stil_paper_order.txt 12 6 14 W17 6600 ../acl-files/ ../auxiliary-files/stil_page_ranges.txt
python bibnopages-to-bibwithpages.py ../bibtex-files/bib-stil-nopages.bib ../auxiliary-files/stil_paper_order.txt ../auxiliary-files/stil_page_ranges.txt ACL-STIL:2017 W17 6600 ../bibtex-files/bib-stil-withpages.bib
python pdf-page-counter.py ../conference-papers/jdp/ ../auxiliary-files/jdp_paper_lengths.txt
python bib-to-ppstil.py ../bibtex-files/bib-jdp-nopages.bib ../auxiliary-files/jdp_paper_lengths.txt ../auxiliary-files/jdp_ppjdps_file.txt ../auxiliary-files/jdp_paper_order.txt
python pdf-splitter.py ../proceedings.pdf ../auxiliary-files/jdp_paper_lengths.txt ../auxiliary-files/jdp_paper_order.txt 185 11 0 W17 6620 ../acl-files/ ../auxiliary-files/jdp_page_ranges.txt
python bibnopages-to-bibwithpages.py ../bibtex-files/bib-jdp-nopages.bib ../auxiliary-files/jdp_paper_order.txt ../auxiliary-files/jdp_page_ranges.txt ACL-STIL:2017 W17 6620 ../bibtex-files/bib-jdp-withpages.bib
python bib-to-aclxml.py ../bibtex-files/bib-all-withpages.bib ../auxiliary-files/all_paper_order.txt ACL-STIL:2017 W17 6600 ../acl-files/W17-6600.xml
```