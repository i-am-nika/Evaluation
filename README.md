# Evaluation (micro- and macro-averaged)

Token-to-token and not token-to-token micro- and macro-averaged Evaluation (Precision, Recall, F1-Measure, Accuracy (only for token-to-token)) for auto Annotation of a text.
------------------------------------------------------------------------------------------------
1. evaluate.py - evaluation
2. extract_pos_ner_from_conllv2.py - extraction
------------------------------------------------------------------------------------------------
evaluate.py

1. The programm evaluate.py shows micro- and macro-averaged Evaluation metrics for token-to-token (e.g. POS - Tags) and not token-to-token (e.g. NER) annotations, both micro- and macro-averaged.

The program takes a file for evaluation as a command-line argument. 
This file for evaluation must constist of three columns with tokens, auto- and gold- Annotations, separated with tabs. The sentences must be separated with an empty line. You can create the file yourself or use the programm extract_pos_ner_from_conllv2.py, which extracts POS and NER Annotations from files with auto- and golden annotations in conll V2 format (see extract_pos_ner_from_conllv2.py).

Example of an input file:

Token-to-token:

What  WP  WP
kind  NN  NN
of  IN  IN
memory  NN IN
? . .


Not token-to-token:

WW	(ORG)	(WORK_OF_ART*
II	(PRODUCT*	*
Landmarks	*)	*
on	*	*
the	(LOC*	*
Great	*	*
Earth	*)	*
of	*	*
China	(GPE)	*
:	*	*
Eternal	(ORG*	*
Memories	*)	*
of	*	*
Taihang	(ORG*	*
Mountain	*)	*)

Output: Precision, Recall, F1-measure, Accuracy (everything micro- and macro-averaged), a list of counts for every class for macro-everaged evaluation.  
------------------------------------------------------------------------------------------------
extract_pos_ner_from_conllv2.py

2. The pragramm extract_pos_ner_from_conllv2.py extracts tokens with POS and NER Annotations from files with auto- and golden annotations in conll V2 format. It writes the result in two txt files (with POS and NER). Every file consists of lines, every line consists of three values: token, auto label, gold label. There is en empty line between sentences.

The programm gets two command-line arguments: input path, output path.

You can use the output files as input for evaluate.py programm.
------------------------------------------------------------------------------------------------

