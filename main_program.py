##############################################################################
# Problem 
# Description       : This project deals with the problem of finding words that
#                     are semantically similar. I have used distributional 
#                     method to find similar words. 
#                     The motivation behind distributional methods is that 
#                     words found in similar contexts are similar.
#                     
#                     e.g. The words "car" and "truck" are usually followed by
#                     word "driving". So the context word "driving" signifies 
#                     that words followed by it such as "car" and "truck" are
#                     similar. This project uses the statistical techniques 
#                     mentioned at Section 20.7 "Word Similarity:Distributional
#                     methods" of textbook "Speech and Language processing" by
#                     Jurafsky-Martin (referred as JM hereafter).
#                     
#                     Similar words are found by distributional relational 
#                     features from already existing corpus and these 
#                     relational features are used to find similarity scores 
#                     for two words. These similarity scores decides how much
#                     a word is similar to other word.
#                              
#                     The association measure used by this project is t-test
#                     and similarity measure used is Jaccard's similarity 
#                     measure.
#                       
#                     Current file is the main program of this project.
#                     It calls two sub-programs internally:
#                     
#                     1) parse_corpus_sentences.py : This program 
#                        reads all sentences from corpus files and does 
#                        full parsing of those sentences using Stanford
#                        parser. Standford parser is NLP tool used to find 
#                        grammatical relations between two words of a sentence
#                        It generates 53 different relations for the words.
#                        More details about Standford parser can be found here:
#                        http://nlp.stanford.edu/software/lex-parser.shtml
#                        
#                        The output generated by Standford parser is used as 
#                        relational features to decide word similarity by 
#                        another program word_shim.py.
#                         
#                    2)  word_shim.py : This program uses the grammatical 
#                        relations generated by Standford parser and builds
#                        a co-occurrence vector(CV) for those relations and 
#                        words in corpus. CV is then used to calculate t-test 
#                        association measures and Jaccard's similarity scores.
#           
#                    More details about these two programs is mentioned below 
#                    and in respective files of these programs.
#
# Usage             : This program takes following inputs:
#                     1) Absolute path of directory where all 
#                        corpus files are present 
#                     2) Absolute path of base directory of Standford parser
#                     3) Absolute path of a file containing all words for 
#                        which similar words have to found
#                     4) Number of maximum similar words to be 
#                        shown in the output
#
#                     e.g. to run this program for a corpus present at the 
#                     location "/home/corpus/", for the base path of Standford
#                     parser "/home/st_parser", for the target word file
#                     "/home/target" and to generate 20 similar words, use 
#                     following command:   
# 
#	 python main_program.py /home/corpus/ /home/st_parser/ /home/target 20 
#
#                     Please note that sequence of the inputs SHOULD be same as
#                     shown above.
#                    
#                     Also, this program internally calls two programs:
#                     I) parse_corpus_sentences.py : It takes following inputs:
#
#                        A) Absolute path of directory where all 
#                           corpus files are present (Same as input 1 of main 
#                           program) 
#                        B) Path of directory where files split from corpus 
#                           files and output parse files generated by Standford 
#                           parser will be placed (Hardcoded in main program)
#                        C) Absolute path of base directory of Standford parser
#                           (Same as input 2 of main program)
#
#                    II) word_sim.py: This program takes following inputs:
#                       
#                       D) Path of directory where files split from corpus 
#                          files and output parse files generated by Standford 
#                          parser will be placed (Hardcoded in main program)
#                       E) Absolute path of a file containing all words for 
#                          which similar words have to found (Same as input 3 
#                          of main program)
#                       F) Number of maximum similar words to be 
#                          shown in the output (Same as input 4 of the main 
#                          program)
#
#                     * Sample of corpus file data: 
#                     
#                     <DOC id="NYT_ENG_19940701.0001" type="story" >
#                     <HEADLINE>
#                     WITNESS SAYS O.J. SIMPSON BOUGHT KNIFE WEEKS
#                     </HEADLINE>
#                     <DATELINE>
#                     LOS ANGELES  (BC-SIMPSON-KILLINGS-1stLd-3Takes-Writethru)
#                     </DATELINE>
#                     <TEXT>
#                     <P>
#                     With the nation's attention riveted again on a Los
#                     Angeles courtroom, a knife dealer testified that O.J.
#                     bought a 15-inch knife five weeks before the slashing 
#                     ex-wife and her friend.
#                     </P> 
#                     </TEXT>
#                     </DOC>
#
#                    Each corpus file is a collection of several xml file which
#                    have <DOC> as the root tag. One sample content of an xml 
#                    file is shown above. Actual corpus sentences are present 
#                    in the <P> tags.
#                    This corpus is taken from a  directory of text from the 
#                    New York Times.  
#
#                    ----------------------------------------------------------
#
#                    * Sample of target word file:
#                    
#                    hamburger
#                    purple
#                    painter 
#                   
#                    This target file has target words hamburger, purple, 
#                    painter. And similar words will be found for these words.
#                   
#                   -----------------------------------------------------------
#                   
#                   * Sample output file entry:
#                   
#                   Target word: hamburger
#
#                   Target word frequency in corpus: 95
#
#                   Similar words and their similarity scores : 
#
#                   hamburger                           1.0    
#                   metropolitan                        0.0814225873961    
#                   concord                             0.0720935410113    
#                   curators                            0.0535650275523    
#                   holyoke                             0.0513007275853 
#                   
#                   Output  shows similar words to the words placed in 
#                   target words file. Please note that output will always
#                   show the target word as the similar word.
#                      
# Algorithm         : 1) This program first reads the inputs given by user.
#                       
#                     2) It then calls parse_corpus_sentences.py to create
#                        parse files containing grammatical relations for
#                        the sentences in the corpus. Detailed algo for
#                        parsing is present in parse_corpus_sentences.py
#                        file.
#               
#                     3) It then calls word_sim.py, which finds the words
#                        similar to target words. Detail algo of this 
#                        process is present word_sim.py file.
#
#
# Author            : Swapnil Nawale 
#
# Date              : 11/06/2012
#
# Version           : 1.0
#
# Prog. Language    : Programming Language used for this program is Python
#                     (Version 2.7.3).
#                     The basic Python code, used in this program, is
#                     learnt from the book "Think Python - How to Think Like 
#                     a Computer Scientist (by Allen B. Downey)" and from
#                     Google's Python Class , present online at 
#                     http://code.google.com/edu/languages/google-python-class/
#                       
# Text-Editor used  : vim editor on Linux Platform
#
# Notes             : (A) I have used Standford Parser for finding grammatical
#                         relations among words present in the sentences of
#                         corpus data. Standford Parser does full parsing 
#                         of sentences. It is mentioned in JM text that 
#                         full parsing is expensive and it is not used in 
#                         practice. But for some reasons, I missed this fact 
#                         from text and used full parsing. And it proved too
#                         expensive for me too even after using multithreading.
#                         It took huge amount 
#                         processing memory and time for doing full parsing
#                         of all sentences in corpus. And I could not really
#                         do it for all sentences in corpus. So, I did full 
#                         parsing of a vary small subset of corpus data.
#
#                         If we extract the sentences 
#                         present in <P> tags of corpus files and if we write 
#                         all these sentences into a file, then there would be 
#                         totally 98,886,626 lines in such file.
#                         And I have used first 2,559,717 lines out of that
#                         file. It is then just 2% of whole data. I was lucky
#                         enough that  these 2,559,717 lines selected has 
#                         at least few occurrences of target words.
#
#                     (B) With using only 2% of data, I was having just 2% of
#                         recall. But I hoped for a higher precision as 
#                         I have used full parsing. But my hope proved to be
#                         futile, since only few occurrences of target words
#                         were available to me for building co-occurrence 
#                         vector. This hit my results very badly. 
#                         Though, my results of similar words are not 
#                         good enough,I think my program of finding 
#                         similar words works correctly for two reasons:
#
#                         i) The similarity score of target word to itself is 1
#                         as expected.
#
#                         ii) I can see some words of little 
#                         relevance for target word "safely" such as 
#                         "immediately", which at least considers POS of words.
#                      
#                   (C) I realized that using Standford Parser for finding 
#                       relations is not practical while writing this project.
#                       Then I thought of using shallow parser(chunkers) like
#                       in Apache OpenNLP, Illinois Chunker and 
#                       Memory-Based Shallow Parser for Python.
#                       Illinois chunker was Java based, so I thought it will 
#                       cause performance issues and I dropped plan of using 
#                       it. And I tried to install other two parsers but could
#                       not get them working.
#                       Another reason that I was tempted to use Standford 
#                       Parser was the output generated by it is convenient
#                       to use for building CV.
#                       It generates output in <relation>(<word_1>, <word_2>)
#                       format and I thought this is convenient than shallow
#                       parsers' output to process and build CV. 
###############################################################################

#!/usr/bin/python

'''
import statements to include Python's in-built module functionalities in the
program
'''
# sys module is used to access command line argument, exit function etc.
import sys

# os module is used to access file manipulation features
import os

###############################################################################
# Function      : main()
# Description   : Entry point for the project.
# Arguments     : None. Command Line Arguments in Python are retrieved from
#                 sys.argv variable of sys module.
# Returns       : None.
###############################################################################
def main():
    
    '''
    Check if any command line argument is passed to program. If not 
    throw error showing proper sample usage. 
    '''

    if (len(sys.argv) > 1):
        
        '''
        Get the values for following command line arguments:
        
        1) Absolute path of directory where all corpus files are present
        2) Absolute path of base directory of Standford parser
        3) Absolute path of a file containing all words for which similar
           words have to found
        4) Number of maximum similar words to be shown in the output 
        '''

        corpus_path = sys.argv[1]
        parser_base_path = sys.argv[2]
        target_word_file_name = sys.argv[3]
        max_num_of_results =  sys.argv[4]

        '''
        Set the name of directory where all split sentence files and parse
        files will be stored.
        '''
        split_files_path = "split"

        '''
        Run parse_corpus_sentences.py program to parse the sentences present
        in the corpus. Only a small subset of sentences present in the 
        corpus will be parsed. The sentences from the small subset of corpus 
        xml files will be fetched by xml parsing and 
        put into a output file named as "op_file" and this op_file
        will be split again into files containing 100000 lines per split file.
        These split files will be parsed by Standford parser. The split files
        and parsed file will be placed in directory set by variable 
        split_files_path above.
        '''

        os.system("python parse_corpus_sentences.py " + corpus_path + " " \
                    + split_files_path + " " + parser_base_path)

        print "Finished parsing files ...."

        '''
        Run word_sim.py program to find words similar to the target words 
        mentioned in target_word_file_name. This program applies statistical
        method for finding word similarity using t-test association measure 
        and Jaccard's similarity measure. To find word similarity, the relation
        present in the parse files generated by parse_corpus_sentences.py
        program above, will be used. 
        '''

        os.system("python word_sim.py " + split_files_path + " " + "op_file" \
                  + " " + target_word_file_name + " " + max_num_of_results)
    
        print "Finished finding similar words ...."


    else:
        print "Give proper arguments to the program!!"

###############################################################################
# End of main function
###############################################################################

'''
Boilerplate syntax to specify that main() method is the entry point for 
this program.
'''

if __name__ == '__main__':
 
    main()

##############################################################################
# End of main_program.py program
#############################################################################
