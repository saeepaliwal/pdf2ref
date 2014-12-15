pdf2ref
=======

Python script to create bib file from directory of pdf papers.

Run this script to print a bibtex citation from a pdf to a file or a full bibtex bibliography file for a directory of pdfs. There are two inputs, the first is either a file or directory and the second is an output file. The script prints a bibtex file to the output file you specify, and prints the undone files to screen. 

Syntax:

    pdf2ref <FILENAME_OF_PAPER> <OUTPUTFILE>

Example for single paper:

    pdf2ref my_paper.pdf my_output_file.bib

Example for a directory

    pdf2ref ~/myproject/papers ~/myproject/my_output_file.bib


There are a few file exceptions this script can not handle: 
(i) it will not annotate preprints
(ii) it will not annotate images or scanned pdf files
(iii) it will not annotate supplementary information from a paper.

This is a first attempt at solving this problem and therefore will also fail on some standard papers. The current failure rate is 10%.