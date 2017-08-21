#!/bin/env python3
#usage:
#$ ./evaluate.py
# 
#__author__ = "Tetyana Chernenko"
#__copyright__ = "Copyright (c) 2017 Tetyana Chernenko"
#__credits__ = ["Tetyana Chernenko"]
#__license__ = "Public Domain"
#__version__ = "1.0.0"
#__maintrainer__ = "Tetyana Chernenko"
#__email__ = "tatjana.chernenko@gmail.com"
#__status__ = "Development"

import sys

"""
The programm evaluates token-to-token (e.g. POS) and not token-to-token (e.g. NER) auto- and gold-annotations.
It needs one command-line argument: a file for evaluation.
Output: precision, recall, f1-measure, accuracy (everything micro- and macro-averaged), a list of counts for every class for macro-everaged evaluation.   
 
"""


def count(filename, auto=int, gold=int): # auto, gold - numbers of the columns of auto und gold labels in input file
    """
    Counts tp, tn, fp, fn for MICRO-averaged evaluation. 
    Is used for evaluation of token-to-token annotations (e.g. POS).
    """
    with open(filename) as textfile:
        text = textfile.readlines()
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    labels = []

    for line in text:
        if line != "":
            autolabel = line.split('\t')[auto].strip()
            goldlabel = line.split('\t')[gold].strip()
                   
            if autolabel !="" and goldlabel !="":
                labels.append(autolabel)
                labels.append(goldlabel)
                labels = list(set(labels))
                
                if autolabel == goldlabel:
                    tp += 1
                    
                else:
                    fn += 1
                    fp += 1
                    
    return(tp, tn, fp, fn, labels)

def counts_for_every_class(filename, auto=int, gold=int): #without TN
    """
    Counts tp, tn, fp, fn for every class for MACRO-averaged evaluation.
    Is used for evaluation of token-to-token annotations (e.g. POS).
    """
    with open(filename) as textfile:
        text = textfile.readlines()

    data = count(filename, auto, gold)
    labels = data[4]

    list_of_counts = []
    for element in labels:
        tp = 0
        tn = 0
        fp = 0
        fn = 0

        counts_for_class = []
        counts_for_class.append(element)

        for line in text:
            if line != "":
                autolabel = line.split('\t')[auto].strip()
                goldlabel = line.split('\t')[gold].strip()   
 
                if autolabel == element and goldlabel == element:       
                    tp += 1
     
                if autolabel == element and goldlabel != element:
                    fn += 1
                    fp += 1

                if autolabel != element and goldlabel == element:
                    fn += 1
                    fp += 1
    
        counts_for_class.append(tp)
        counts_for_class.append(tn)
        counts_for_class.append(fp)
        counts_for_class.append(fn)
        list_of_counts.append(counts_for_class)

    return (list_of_counts)


def new_count(filename, auto=int, gold=int): #without TN, but with fp_spurious, fn_missing
    """
    Counts tp, tn, fp_fn_same, fp_spurious, fn_missing for MICRO-averaged annotation.
    Is used for evaluation of not token-to-token annotations (e.g. NER).
    """
    with open(filename) as textfile:
        text = textfile.readlines()
 
    list_of_borders_auto = []
    list_of_borders_gold = []

    tp = 0
    tn = 0
    fp_fn_same = 0
    fp_spurious = 0
    fn_missing = 0

    my_tp= []
    my_fp_fn_same = []
    my_fp_spurious = []
    my_fn_missing = []

    # FIND BORDERS FOR AUTO:
    for line_idx in range(len(text)):
        a = text[line_idx].split('\t')[auto].strip()
        if a.split() != []:        
            x = list(a)
            if x[0] == "(":
                n = 0
                left_border_auto = line_idx   
                if n<10:
                    while list(text[line_idx+n].split('\t')[auto].strip())[-1] != ")":
                        n+=1
                    right_border_auto = line_idx+n
                tup = (left_border_auto, right_border_auto)
                list_of_borders_auto.append(tup)
    #print("LIST_B_A: ", list_of_borders_auto)

    # FIND BORDERS FOR GOLD:
    for line_idx in range(len(text)):
        a = text[line_idx].split('\t')[gold].strip()
        if a.split() != []:        
            x = list(a)
            if x[0] == "(":
                n = 0
                left_border_gold = line_idx   
                if n<10:
                    while list(text[line_idx+n].split('\t')[gold].strip())[-1] != ")":
                        n+=1
                    right_border_gold = line_idx+n
                tup = (left_border_gold, right_border_gold)
                list_of_borders_gold.append(tup)
    #print("LIST_B_G: ", list_of_borders_gold)

    # Find all labels:
    muster = ["(", ")", "*"]
    all_labels = []
    for el in list_of_borders_auto:
        labels = text[el[0]].split('\t')[auto].strip()
        for k in muster:
            labels = labels.replace(k, "")
        all_labels.append(labels)
        all_labels = list(set(all_labels))
        
    #print("ALL LABELS: ", all_labels)

    # Count tp and fp_fn_same:
    for el in list_of_borders_auto:
        for elem in list_of_borders_gold:
            if el == elem:       
                z = 0
                length = el[1]-el[0]
                for i in range(length+1):
                    while z <= length: 
                        if text[el[0]+z].split("\t")[auto].strip() == text[el[0]+z].split("\t")[gold].strip():
                            z+=1
                            if z-1 == length:
                                tp+=1
                                my_tp.append(el)
                        else:
                            z=length+1
                            fp_fn_same += 1
                            my_fp_fn_same.append(el)

    #print("MY_TP: ", my_tp)
    #print("MY_FP_FN_SAME: ", my_fp_fn_same)
    
    # Count fp_spurious:
    for el in list_of_borders_auto:
        if el not in my_tp and el not in my_fp_fn_same:
            my_fp_spurious.append(el) 
            fp_spurious +=1
    #print("My_fp_sp: ", my_fp_spurious)

    # Count fn_missing:
    for el in list_of_borders_gold:
        if el not in my_tp and el not in my_fp_fn_same:
            my_fn_missing.append(el) 
            fn_missing+=1
    #print("My_fn_missing: ", my_fn_missing)

    return tp, tn, fp_fn_same, fp_spurious, fn_missing, all_labels



def new_counts_for_every_class(filename, auto=int, gold=int):
    """
    Counts tp, tn, fp_fn_same, fp_spurious, fn_missing for MACRO-averaged annotation.
    Is used for evaluation of not token-to-token annotations (e.g. NER).
    """
    with open(filename) as textfile:
        text = textfile.readlines()

    data = new_count(filename, auto, gold)
    labels = data[5]

    list_of_counts = []

    borders_auto = []
    borders_gold = []

    for element in labels:
        tp = 0
        tn = 0
        fp_fn_same = 0
        fp_spurious = 0
        fn_missing = 0
        my_tp = []
        my_fp_fn_same = []
        my_fp_spurious = []
        my_fn_missing = []
        counts_for_class = []
        counts_for_class.append(element)

        list_of_borders_auto_for_el = []
        list_of_borders_gold_for_el = []
        list_of_borders_auto_for_el.append(element) 
        list_of_borders_gold_for_el.append(element)
        
        list_of_b_auto_klein = [] 
        list_of_b_gold_klein = []
       
        # Find borders of NER for auto annotation:
        muster = ["(", ")", "*"]
       
        for line_idx in range(len(text)):
            a = text[line_idx].split('\t')[auto].strip()
            if a.split() != []:
                b = a
                for k in muster:
                    b = b.replace(k,"")
                if b == element:      
                    x = list(a)
                    if x[0] == "(":
                
                        n = 0
                        left_border_auto = line_idx   
                        if n<10:
                            while list(text[line_idx+n].split('\t')[auto].strip())[-1] != ")":
                                n+=1
                            right_border_auto = line_idx+n
                        tup = (left_border_auto, right_border_auto)
                        list_of_b_auto_klein.append(tup)
        list_of_borders_auto_for_el.append(list_of_b_auto_klein)
        borders_auto.append(list_of_borders_auto_for_el)

        # Find borders of NER for gold annotation:
        for line_idx in range(len(text)):
            a = text[line_idx].split('\t')[gold].strip()
            if a.split() != []:     
                b = a
                for k in muster:
                    b = b.replace(k,"")
                if b == element: 
                       
                    x = list(a)
               
                    if x[0] == "(":
                        n = 0
                        left_border_gold = line_idx   
                        if n<10:
                            while list(text[line_idx+n].split('\t')[gold].strip())[-1] != ")":
                                n+=1
                            right_border_gold = line_idx+n
                        tup = (left_border_gold, right_border_gold)
                 
                        list_of_b_gold_klein.append(tup)
                      
        list_of_borders_gold_for_el.append(list_of_b_gold_klein)
        borders_gold.append(list_of_borders_gold_for_el)
   
    # Count tp and fp_fn_same for every class:
        for el in borders_auto:
            for elem in borders_gold:
                for e in el[1]:
                    for p in elem[1]:
                        if e == p:   
                            z = 0
                            length = e[1]-e[0]
                            for i in range(length+1):
                                while z <= length: 
                                    if text[e[0]+z].split("\t")[auto].strip() == text[e[0]+z].split("\t")[gold].strip():
                                        z+=1
                                        if z-1 == length:
                                            tp+=1
                                            my_tp.append(e)
                                    else:
                                        z=length+1
                                        fp_fn_same += 1
                                        my_fp_fn_same.append(e)
    
        # Count fp_spurious:
        for el in borders_auto:
            if el[0] == element:
                for ele in el[1]:
                    if ele not in my_tp and ele not in my_fp_fn_same:
                        my_fp_spurious.append(ele) 
                        fp_spurious +=1

        # Count fn_missing:
        for el in borders_gold:
            if el[0] == element:
                for eleme in el[1]:
                    if el not in my_tp and el not in my_fp_fn_same:
                        my_fn_missing.append(el) 
                        fn_missing+=1
    
        counts_for_class.append(tp)
        counts_for_class.append(tn)
        counts_for_class.append(fp_fn_same)
        counts_for_class.append(fp_spurious)
        counts_for_class.append(fn_missing)
        list_of_counts.append(counts_for_class)

    return (list_of_counts)


# ----------------------------------------------------------------------     

# Micro-averaged evaluation for toket-to-token annotations (e.g. POS):

def precision(filename, auto=int, gold=int):
    data = count(filename, auto, gold)
    tp, tn, fp, fn = data[0], data[1], data[2], data[3]
    pr = tp/(tp+fp)
    return pr

def recall(filename, auto=int, gold=int):
    data = count(filename, auto, gold)
    tp, tn, fp, fn = data[0], data[1], data[2], data[3]
    r = tp/(tp+fn)
    return r

def f1_measure(filename, auto=int, gold=int):
    data = count(filename, auto, gold)
    tp, tn, fp, fn = data[0], data[1], data[2], data[3]
    pres = precision(filename, auto, gold)
    rec = recall(filename, auto, gold)
    f1_m = (2*pres*rec)/(pres+rec)
    return f1_m

def accuracy(filename, auto=int, gold=int):
    data = count(filename, auto, gold)
    tp, tn, fp, fn = data[0], data[1], data[2], data[3]
    acc = (tp+tn)/(tp+tn+fp)  # fp = fn
    return acc 

# Macro-averaged evaluation for token-to-token annotation (e.g. POS):

def precision_macro(filename, auto=int, gold=int):
    data = counts_for_every_class(filename, auto, gold)
    preci = []
    for el in data:
        element, tp, tn, fp, fn= el[0], el[1], el[2], el[3], el[4]
        prec_for_every_class = tp/(tp+fp)
        preci.append(prec_for_every_class)
    number_of_el = len(preci)
    summe = 0
    for el in preci:
        summe += el
        pr_macro = summe/number_of_el
    return pr_macro

def recall_macro(filename, auto=int, gold=int):
    data = counts_for_every_class(filename, auto, gold)
    recall = []
    for el in data:
        element, tp, tn, fp, fn= el[0], el[1], el[2], el[3], el[4]
        rec_for_every_class = tp/(tp+fn)
        recall.append(rec_for_every_class)
    number_of_el = len(recall)
    summe = 0
    for el in recall:
        summe += el
        re_macro = summe/number_of_el
    return re_macro

def f1_measure_macro(filename, auto=int, gold=int):
    data = counts_for_every_class(filename, auto, gold)
    f1 = []
    for el in data:
        element, tp, tn, fp, fn= el[0], el[1], el[2], el[3], el[4]
        pres = precision_macro(filename, auto, gold)
        rec = recall_macro(filename, auto, gold)
        f1_for_every_class = (2*pres*rec)/(pres+rec)
        f1.append(f1_for_every_class)
    number_of_el = len(f1)
    summe = 0
    for el in f1:
        summe += el
        f1_macro = summe/number_of_el
    return f1_macro

def accuracy_macro(filename, auto=int, gold=int):
    data = counts_for_every_class(filename, auto, gold)
    acc = []
    for el in data:
        element, tp, tn, fp, fn= el[0], el[1], el[2], el[3], el[4]
        acc_for_every_class = (tp+tn)/(tp+tn+fp)  # wenn fp = fn
        acc.append(acc_for_every_class)
    number_of_el = len(acc)
    summe = 0
    for el in acc:
        summe += el
        acc_macro = summe/number_of_el
    return acc_macro

# Micro-averaged evaluation for NOT token-to-token-annotations (e.g. NER):

def precision_ner(filename, auto=int, gold=int):
    data = new_count(filename, auto, gold)
    tp, tn, fp_fn_same, fp_spurious, fn_missing = data[0], data[1], data[2], data[3], data[4]
    pr = tp/(tp+fp_fn_same+fp_spurious)
    return pr

def recall_ner(filename, auto=int, gold=int):
    data = new_count(filename, auto, gold)
    tp, tn, fp_fn_same, fp_spurious, fn_missing = data[0], data[1], data[2], data[3], data[4]
    r = tp/(tp+fp_fn_same+fn_missing)
    return r

def f1_measure_ner(filename, auto=int, gold=int):
    data = count(filename, auto, gold)
    ttp, tn, fp_fn_same, fp_spurious, fn_missing = data[0], data[1], data[2], data[3], data[4]
    pres = precision_ner(filename, auto, gold)
    rec = recall_ner(filename, auto, gold)
    f1_m = (2*pres*rec)/(pres+rec)
    return f1_m


# Macro-averaged evaluation for NOT token-to-token-annotations (e.g. NER):

def precision_macro_ner(filename, auto=int, gold=int):
    data = new_counts_for_every_class(filename, auto, gold)
    preci = []
    for el in data:
        element, tp, tn, fp_fn_same, fp_spurious, fn_missing= el[0], el[1], el[2], el[3], el[4], el[5]
        prec_for_every_class = tp/(tp+fp_fn_same+fp_spurious)
        preci.append(prec_for_every_class)
    number_of_el = len(preci)
    summe = 0
    for el in preci:
        summe += el
        pr_macro = summe/number_of_el
    return pr_macro

def recall_macro_ner(filename, auto=int, gold=int):
    data = new_counts_for_every_class(filename, auto, gold)
    recall = []
    for el in data:
        element, tp, tn, fp_fn_same, fp_spurious, fn_missing= el[0], el[1], el[2], el[3], el[4], el[5]
        rec_for_every_class = tp/(tp+fp_fn_same+fn_missing)
        recall.append(rec_for_every_class)
    number_of_el = len(recall)
    summe = 0
    for el in recall:
        summe += el
        re_macro = summe/number_of_el
    return re_macro

def f1_measure_macro_ner(filename, auto=int, gold=int):
    data = new_counts_for_every_class(filename, auto, gold)
    f1 = []
    for el in data:
        element, tp, tn, fp_fn_same, fp_spurious, fn_missing= el[0], el[1], el[2], el[3], el[4], el[5]
        pres = precision_macro_ner(filename, auto, gold)
        rec = recall_macro_ner(filename, auto, gold)
        f1_for_every_class = (2*pres*rec)/(pres+rec)
        f1.append(f1_for_every_class)

    number_of_el = len(f1)
    summe = 0
    for el in f1:
        summe += el
        f1_macro = summe/number_of_el
    return f1_macro


if __name__ == "__main__":
    arg_list = sys.argv
    
    if len(arg_list) > 1:
        textfile_for_evaluation = arg_list[1]
 
    wahl = input(" Drücken Sie \"a\", wenn Sie eine \"token-to-token\" Annotation evaluieren wollen (Z.B.: POS). \n Drücken Sie \"b\", wenn Sie eine \"NOT token-to-token\" Annotation evaluieren wollen (Z.B. NER). Ihre Wahl: ")

    print("\nTextfile for evaluation:\n\t{}\n".format(textfile_for_evaluation))
        
    if wahl == "a":
        print("\nMICRO-AVERAGED:\n")
        pr = precision(textfile_for_evaluation, 1, 2)
        print("PRECISION: {}".format(pr))
    
        r = recall(textfile_for_evaluation, 1, 2)
        print("RACALL: {}".format(r))
    
        f1_m = f1_measure(textfile_for_evaluation, 1, 2)
        print("F1-MEASURE: {}".format(f1_m))
    
        acc = accuracy(textfile_for_evaluation, 1, 2)
        print("ACCURACY: {}\n".format(acc))
        print("\nMACRO-AVERAGED:\n")

        our_counts_for_every_class = counts_for_every_class(textfile_for_evaluation, 1, 2)
        print("COUNTS_FOR_CLASS (label, tp, tn, fp, fn):\n {}\n".format(our_counts_for_every_class))

        preci_macro = precision_macro(textfile_for_evaluation, 1, 2)
        print("PRECISION_MACRO: {}".format(preci_macro))

        re_macro = recall_macro(textfile_for_evaluation, 1, 2)
        print("RECALL_MACRO: {}".format(re_macro))

        f1_macro = f1_measure_macro(textfile_for_evaluation, 1, 2)
        print("F1_MEASURE_MACRO: {}".format(f1_macro))

        acc_macro = accuracy_macro(textfile_for_evaluation, 1, 2)
        print("ACCURACY_MACRO: {}".format(acc_macro))

    if wahl == "b":
        print("\nMICRO-AVERAGED:\n")

        pres = precision_ner(textfile_for_evaluation, 1, 2)
        print("PRECISION: {}".format(pres))
    
        re = recall_ner(textfile_for_evaluation, 1, 2)
        print("RACALL: {}".format(re))
    
        f1_me = f1_measure_ner(textfile_for_evaluation, 1, 2)
        print("F1-MEASURE: {}\n".format(f1_me))
        
        print("\nMACRO-AVERAGED for NER:\n")
        
        new_counts_for_ev = new_counts_for_every_class(textfile_for_evaluation, 1, 2)
        print("NEW COUNTS FOR EVERY CLASS (label, tp, tn, fp_fn_same, fp_spurious, fn_missing):\n {}\n".format(new_counts_for_ev))
        
        pres_macro = precision_macro_ner(textfile_for_evaluation, 1, 2)
        print("PRECISION: {}".format(pres_macro))
    
        re_macro = recall_macro_ner(textfile_for_evaluation, 1, 2)
        print("RACALL: {}".format(re_macro))
    
        f1_me_macro = f1_measure_macro_ner(textfile_for_evaluation, 1, 2)
        print("F1-MEASURE: {}\n".format(f1_me_macro))
