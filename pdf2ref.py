#!/usr/bin/env python
import urllib2
from PyPDF2 import PdfFileReader
import re
import sys
import glob
import os

def get_citations(dir_or_file, outfile):
    undone_files = []
    all_papers = []
    if os.path.isdir(dir_or_file):
        os.chdir(dir_or_file)
        all_papers = glob.glob("*.pdf")
    elif os.path.isfile(dir_or_file):
        all_papers.append(dir_or_file)
    else:
        print("ERROR: Please input a pdf file or directory.")
        sys.exit()

    if not all_papers:
        print("ERROR: There are no pdf files in the specified directory.")
        sys.exit()

    import pdb; pdb.set_trace()
    with open(outfile,'w+') as bibfile:
        for pdf_file in all_papers:
            doi_re = re.compile("10.(\d)+/([^(\s\>\"\<)])+")
            input = PdfFileReader(file(pdf_file, "rb"))

            text = input.getPage(0).extractText()
             
            m = doi_re.search(text)
            if m is None:
                undone_files.append(pdf_file)
                continue
            basetext = m.group(0)
            doi = re.sub(',', '', basetext)

            try: 
                title = input.getDocumentInfo()['/Title']
                if print_reference(title,bibfile):
                    continue
                elif title.find("doi")<0:
                    idx = doi.find(title.replace(" ",""))
                    doi = doi[0:idx]
            except:
                doi = doi

            # Remove standard words
            standard_words = get_standard_words()
            for word in standard_words:
                if doi.find(word) >= 0:
                    doi = doi[0:doi.find(word)]

            if print_reference(doi,bibfile):
                continue
            elif len(doi) < 50:
                while not print_reference(doi, bibfile):
                    doi = doi[:len(doi)-1]
            else:
                import pdb; pdb.set_trace()
                undone_files.append(pdf_file)
    
    for undone_file in undone_files:
        print ""
    return undone_files

def print_reference(DOI,f):
    if DOI is not None:
        try: 
            file = urllib2.urlopen("http://api.crossref.org/works/" + DOI + "/transform/application/x-bibtex")
            data = file.read()
            if data.find('Peresson')>=0:
                return False
            f.write(data + "\n")
            return True
        except:
            return False

def get_standard_words():
    return ['Contents',
            'January',
            'Februrary', 
            'March',
            'April',
            'May',
            'June',
            'July',
            'August',
            'September',
            'October',
            'November',
            'December',
            'Copyright',
            'Journal',
            'University',
            'Department' ]

if len(sys.argv) < 3: 
    print("ERROR: function requires two inputs: pdf2ref <DIR_OR_PAPER> <OUTPUTFILE>")
    sys.exit()
dir_or_file = sys.argv[1]
outfile = sys.argv[2]

if dir_or_file == '.':
    dir_or_file = os.getcwd()
get_citations(dir_or_file,outfile)

