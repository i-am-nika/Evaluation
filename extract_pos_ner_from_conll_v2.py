#!/bin/env python3
#usage:
#$ ./extract_pos_ner_from_conll_v2.py
# 
#__author__ = "Tetyana Chernenko"
#__copyright__ = "Copyright (c) 2017 Tetyana Chernenko"
#__credits__ = ["Tetyana Chernenko"]
#__license__ = "Public Domain"
#__version__ = "1.0.0"
#__maintrainer__ = "Tetyana Chernenko"
#__email__ = "tatjana.chernenko@gmail.com"
#__status__ = "Development"

import os
import sys

"""
The programm extracts tokents with POS and tokens with NER from cctv_0001.v2 auto_conll and  cctv_0001.v2_gold_conll files
and writes the result in two files cctv 0001.v2.pos.txt and cctv 0001.v2.ner.txt. Every file consists of lines, every line consists of
three values: token, auto label, gold label. There is en empty line between sentences.

The programm gets two command-line arguments: input path, output path.
"""

# 1. Read files
def extract_files_in_path(input_path_with_corpus_files, file_name_start = "cctv_0001"):
    corpus_files = [file_name for file_name in os.listdir(input_path_with_corpus_files) if file_name.startswith(file_name_start)]    
    for file_name in corpus_files:
        if file_name.endswith("auto_conll"):
            automatic_annotation = file_name
            
        if file_name.endswith("gold_conll"):
            gold_annotation = file_name
            
    return automatic_annotation, gold_annotation
    
    
# 2. Extract words and POS-tags(from automatic corpus and from gold corpus), write in files:    
def extract_words_and_pos(filename1, filename2, outfilename):
    output = open(outfilename, "w")
    sentence = ""
    pos = ""
    pos_gold = ""

    with open(filename1) as d1:
        data1 = d1.readlines()
    with open(filename2) as d2:
        data2 = d2.readlines()
  
    for line_idx in range(len(data1)):
        if data1[line_idx] == "\n" and data2[line_idx] == "\n":
            if sentence != "" and pos != "" and pos_gold != "":
                for i in range(len(sentence.split(' '))):
                    for x in range(len(pos.split(' '))):
                        for y in range(len(pos_gold.split(' '))):
                            if x == i == y:
                                try:
                                    output.write(sentence.split(' ')[i] + "\t")
                                    output.write(pos.split(' ')[x] + "\t")
                                    output.write(pos_gold.split(' ')[y] + "\n")
                                except:
                                    exit
                
            sentence = ""
            pos = ""
            pos_gold = ""
            continue
        attributes = data1[line_idx].split()
        attributes_gold = data2[line_idx].split()
        if not data1[line_idx].startswith("#") and not data2[line_idx].startswith("#"):
            sentence += attributes[3] + " "
            pos += attributes[4] + " "
            pos_gold += attributes_gold[4] + " "
                    
                        
    if sentence != "" and pos != "" and pos_gold != "":
        for i in range(len(sentence.split(' '))):
            for x in range(len(pos.split(' '))):
                for y in range(len(pos_gold.split(' '))):
                    if x == i == y:
                        try:
                            output.write(sentence.split(' ')[i] + "\t")
                            output.write(pos.split(' ')[x] + "\t")
                            output.write(pos_gold.split(' ')[y] + "\n")
                        except:
                            exit
        
    output.close()    
    
# 3. Extract NER
def extract_words_and_ner(filename1, filename2, outfilename):
    output = open(outfilename, "w")
    sentence = ""
    ner = ""
    ner_gold = ""

    with open(filename1) as d1:
        data1 = d1.readlines()
    with open(filename2) as d2:
        data2 = d2.readlines()

    for line_idx in range(len(data1)):
        if data1[line_idx] == "\n" and data2[line_idx] == "\n":
            if sentence != "" and ner != "" and ner_gold != "":
                for i in range(len(sentence.split(' '))):
                    for x in range(len(ner.split(' '))):
                        for y in range(len(ner_gold.split(' '))):
                            if x == i == y:
                                try:
                                    output.write(sentence.split(' ')[i] + "\t")
                                    output.write(ner.split(' ')[x] + "\t")
                                    output.write(ner_gold.split(' ')[y] + "\n")
                                except:
                                    exit
                
            sentence = ""
            ner = ""
            ner_gold = ""
            continue
        attributes = data1[line_idx].split()
        attributes_gold = data2[line_idx].split()
        if not data1[line_idx].startswith("#") and not data2[line_idx].startswith("#"):
            sentence += attributes[3] + " "
            ner += attributes[10] + " "
            ner_gold += attributes_gold[10] + " "
                    
                        
    if sentence != "" and ner != "" and ner_gold != "":
        for i in range(len(sentence.split(' '))):
            for x in range(len(ner.split(' '))):
                for y in range(len(ner_gold.split(' '))):
                    if x == i == y:
                        try:
                            output.write(sentence.split(' ')[i] + "\t")
                            output.write(ner.split(' ')[x] + "\t")
                            output.write(ner_gold.split(' ')[y] + "\n")
                        except:
                            exit
    output.close() 

if __name__ == "__main__":
    arg_list = sys.argv
    output_path_for_extracted_files = arg_list[2]
    input_path_with_corpus_files = arg_list[1]
    print("INPUT PATH (with corpus files):\n\t{}".format(input_path_with_corpus_files))
    print("OUTPUT PATH (for extracted annotations):\n\t{}\n".format(os.path.abspath(output_path_for_extracted_files)))
    os.makedirs(output_path_for_extracted_files, exist_ok=True)   
    automatic_annotation, gold_annotation = extract_files_in_path(input_path_with_corpus_files)
    print("COLLECTION OF 2 FILES READ\n")
    extract_words_and_pos(input_path_with_corpus_files+automatic_annotation, input_path_with_corpus_files+gold_annotation, output_path_for_extracted_files+"cctv_0001.v2.pos.txt")
    print("WORDS and POS EXTRACTED")
    extract_words_and_ner(input_path_with_corpus_files+automatic_annotation, input_path_with_corpus_files+gold_annotation, output_path_for_extracted_files+"cctv_0001.v2.ner.txt")
    print("WORDS and NER EXTRACTED")
    

    
