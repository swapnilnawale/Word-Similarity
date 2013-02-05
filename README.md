Word-Similarity
===============

Word Similarity using Distributional methods using Python

 Problem 
 Description       : This project deals with the problem of finding words that
                     are semantically similar. I have used distributional 
                     method to find similar words. 
                     The motivation behind distributional methods is that 
                     words found in similar contexts are similar.
                     
                     e.g. The words "car" and "truck" are usually followed by
                     word "driving". So the context word "driving" signifies 
                     that words followed by it such as "car" and "truck" are
                     similar. This project uses the statistical techniques 
                     mentioned at Section 20.7 "Word Similarity:Distributional
                     methods" of textbook "Speech and Language processing" by
                     Jurafsky-Martin (referred as JM hereafter).
                     
                     Similar words are found by distributional relational 
                     features from already existing corpus and these 
                     relational features are used to find similarity scores 
                     for two words. These similarity scores decides how much
                     a word is similar to other word.
                              
                     The association measure used by this project is t-test
                     and similarity measure used is Jaccard's similarity 
                     measure.
                       
                     Current file is the main program of this project.
                     It calls two sub-programs internally:
                     
                     1) parse_corpus_sentences.py : This program 
                        reads all sentences from corpus files and does 
                        full parsing of those sentences using Stanford
                        parser. Standford parser is NLP tool used to find 
                        grammatical relations between two words of a sentence
                        It generates 53 different relations for the words.
                        More details about Standford parser can be found here:
                        http://nlp.stanford.edu/software/lex-parser.shtml
                        
                        The output generated by Standford parser is used as 
                        relational features to decide word similarity by 
                        another program word_shim.py.
                         
                    2)  word_shim.py : This program uses the grammatical 
                        relations generated by Standford parser and builds
                        a co-occurrence vector(CV) for those relations and 
                        words in corpus. CV is then used to calculate t-test 
                        association measures and Jaccard's similarity scores.
           
                    More details about these two programs is mentioned below 
                    and in respective files of these programs.

 Usage             : This program takes following inputs:
                     1) Absolute path of directory where all 
                        corpus files are present 
                     2) Absolute path of base directory of Standford parser
                     3) Absolute path of a file containing all words for 
                        which similar words have to found
                     4) Number of maximum similar words to be 
                        shown in the output

                     e.g. to run this program for a corpus present at the 
                     location "/home/corpus/", for the base path of Standford
                     parser "/home/st_parser", for the target word file
                     "/home/target" and to generate 20 similar words, use 
                     following command:   
 
   python main_program.py /home/corpus/ /home/st_parser/ /home/target 20 
