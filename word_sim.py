##############################################################################
# Algorithm         :	This program finds the words similar to target words
#						by using t-test association measure and Jaccard's
#						similarity measure.
#                       
#                       Steps followed in this program:
#       
#		                1) This program first read the target words from
#                          a file passed as input to it.
#                       
#                       2) Next it calculates the freq and max likelihood prob
#                          of each word present in the file containing 
#                          sentences from corpus. This file is also passed
#                          an input to it.
#               
#                       3) Next it reads all parse files and segregates all
#                          grammatical relations from it. These relations
#                          act as relational feature for out distributional
#                          method
#
#                       4) Using these relations features, it calculates the
#                          max likelihood prob for features and max likelihood
#                          estimate for joint prob of a feature and a word 
#                          together.
#                   
#                       5) Using various prob calculated in step 2 and 4, 
#                          it calculates t-test association measures for
#                          each word and feature.
#
#                       6) Using association measures calculated in step 5, 
#                          words similar to each target word is found by
#                          by using similarity measure score by Jaccard's
#                          formula.
#
#                       7) Then it displays top N words similar to each target 
#                          word. Here the number N is also passed input to the
#                          program.
###############################################################################

#!/usr/bin/python

'''
import statements to include Python's in-built module functionalities in the
program
'''
# sys module is used to access command line argument, exit function etc.
import sys

# re module is used to access regular expression related facilities
import re

# os module is used to access file manipulation features
import os

# python csv module is used for pretty printing of confusion matrix
import csv

# math module for logarithmic functionalities
import math

# collections module is used for creating ordered hash tables / dicts 
import collections

# time module for time related functionality
import time


'''
Set the value of debug flag. debug flag is used to decide whether to print
debug information in the output or not. This flag will be a global variable.
'''
debug = False

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
        if debug:
            print "At least one parameter passed to program !"
        
        '''
        Get the values of command line arguments for :
        1) Path of directory where all parse files are present  
        
        2) File containing all sentences present in the corpus
        (which is referred as sentence file hereafter in this program)

        3) File containing list of target words for which we want to 
        find similar words
        
        4) Maximum number of similar words that needs to be displayed 
        in output
        '''        
        parse_directory =  sys.argv[1]
        sent_file = sys.argv[2]
        target_words_file = sys.argv[3]
        num_of_sim_words = int(sys.argv[4])

        '''
        Read the target list word file and store them into a list
        '''
        target_file_handle = open(target_words_file, 'r')
        target_words_list =  target_file_handle.readlines()
        target_file_handle.close()

        
        '''
        Get the names of all parse files present in the
        parse directory. For this, built-in function, listdir is used.
        It gives the directory listing for any directory on disk.
        The usage of listdir function was learnt from the link:
        http://docs.python.org/2/library/os.html

        These parse files were created earlier by Standford parser
        by running parse_corpus_sentences.py file.
        '''
        parse_files_list =  os.listdir(parse_directory)

        
        '''
        Start getting max likelihood Probabilities for each word.
        '''

        '''
        Get the frequencies of all words present in the corpus. 
        These frequencies  will be obtained from sentence file (passed as
        command line argument).
        The frequencies of all words will be stored in 
        dict object "word_frq_dict",
        which will have each word as the key and its freq as the value
        for that key. 

        E.g. if a word "Cleopatra" occurs 900 times in sentence file
        and word "Ceaser" occurs 89 times in sentence file
        dict object will look this:

        [('Cleopatra':900), ('Ceaser'):89]
        '''
        # create word_frq_dict
        word_frq_dict = {}

        '''
        To retrieve the frequencies of all words from the sentence file, 
        built-in counter object will be used. The example usage of counter
        object to get word frequencies is borrowed from the link:
        http://docs.python.org/2/library/collections.html
        '''  
        words = re.findall('\w+', open(sent_file).read().lower())
    
        word_freq_counter = collections.Counter(words)
        
        '''
        Iterate over the word_freq_counter object and feed in those
        values to word_frq_dict. Also calculate total number of tokens
        in the sentence file.
        '''
        total_tokens = 0

        for word_freq in word_freq_counter.most_common():
             
            word_frq_dict[word_freq[0]] = word_freq[1]
            total_tokens = total_tokens + word_freq[1]

        if debug:
            print total_tokens
            print word_frq_dict
        
        '''
        Next, calculate Max likelihood Probabilities for each word in sentence
        file. This probability will be equal to freq of word / total tokens in 
        sentence file. Since the number of total token is too high,the prob.
        will be calculated in log space.

        The max likelihood prob will be stored in a dict object called as p_w.
        This dict object corresponds to P(w) given in section 20.7.2 of JM text
        '''
        # create p_w dict object
        p_w = {}

        # iterate over the word_frq_dict to get max likelihood prob for words 

        for word, freq in word_frq_dict.iteritems():
            p_w[word] = math.log10(freq) - math.log10(total_tokens) 
            
        
        if debug:
            print p_w

        '''
        Start building co-occurrence vector using all parse files.

        These parse files were created earlier by Standford parser
        by running parse_corpus_sentences.py program.

        '''
        
        ''' 
        Get the names of all parse files present in the
        parse directory (passed as command line argument). 
        For this, built-in function listdir is used.
        It gives the directory listing for any directory on disk.
        The usage of listdir function was learnt from the link:
        http://docs.python.org/2/library/os.html

        '''
        parse_files_list =  os.listdir(parse_directory)

        '''
        Iterate over the parse files list created above and read 
        each parse file. A list containing grammatical relations for
        all words in parse files will be created from all parse files.
        This list will be used further in program to create co-occurrence
        vector.

        A typical grammatical relation in any parse file looks like this:
        
        <grammatical_relation>(<word_1_in_relation> - 
                               <index_of_word_1_in_sentence>, 
                               <word_2_in relation> - 
                               <index_of_word_2_in_sentence>)
        
        E.g. if the original sentence in the corpus file is :
        
        "The Bush family did its best to shield the service and reception from
        public view."
        
        Then the parse file showing grammatical relation will have following 
        contents:

        det(family-3, The-1)
        nn(family-3, Bush-2)
        nsubj(did-4, family-3)
        root(ROOT-0, did-4)
        poss(best-6, its-5)
        dobj(did-4, best-6)
        aux(shield-8, to-7)
        xcomp(did-4, shield-8)
        det(service-10, the-9)
        dobj(shield-8, service-10)
        dobj(shield-8, reception-12)
        conj_and(service-10, reception-12)
        amod(view-15, public-14)
        prep_from(shield-8, view-15)
 
        
        This program will segregate all grammatical relations from
        all parse files and create a list "grammar_relations_list", 
        which has tuples corresponding to each grammatical relation as the 
        elements of the list. The first element in tuple will be grammatical
        relation like det, nn. Second element will be word_1 in relation and
        Third element will be word_2 in relation. All words will be converted
        into lower case before adding them into "grammar_relations_list".

        (Note: Python tuples are the specific data structures which is used to 
        store sequence data types. Usage of tuples was learnt from this link:
        http://docs.python.org/2/tutorial/datastructures.html)

        E.g.  
        
        For above mentioned grammatical relations, our grammar_relations_list
        will have following contents:

        [
            ('det', 'family', 'the'),
            ('nn', 'family', 'bush'),
            ('nsubj', 'did', 'family'),
            ('nsubj', 'did', 'family'),
            ('poss', 'best', 'its'),
            ('dobj', 'did', 'best'),
            ('aux', 'shield', 'to'),
            ('xcomp', 'did', 'shield'),
            ('det', 'service', 'the'),
            ('dobj', 'shield', 'service'),
            ('dobj', 'shield', 'reception'),
            ('conj_and', 'service', 'reception'),
            ('amod', 'view', 'public'),
            ('prep_from', 'shield', 'view')
        ]
    
        '''

        '''
        Create and initialize grammar_relations_list
        '''
        grammar_relations_list = []
        
        '''
        Iterate over the parse files list to build grammar_relations_list
        '''
        for parse_file_name in parse_files_list:
            
            if debug:
                 print parse_file_name
       
            '''
            Check if current file being processed is a parse file.
            This check is required to make sure that we only process
            parse files as other types of files can be there in parse
            directory.
            '''

            if ".parse" in parse_file_name:
                
                # open and read parse file
                parse_file_handle = open(parse_directory  + "/" + \
                                         parse_file_name, 'r')

                # get all lines from parse file into a list                
                parse_file_lines = parse_file_handle.readlines()
    
                # close the parse file
                parse_file_handle.close()

                '''
                Iterate over the parse_file_lines to get grammatical relations
                '''
                
                for parse_file_line in parse_file_lines:

                    if "(" in parse_file_line:
                            
                        if debug:
                            print parse_file_line
                        
                        
                        '''
                        Split the parse_file_line to get grammatical relation
                        , word_1 and word_2  
                        '''
                        
                        relations_list =  parse_file_line.split('(')
                        
                        grammar_relation =  relations_list[0]
                        words_list =  relations_list[1]
                        
                        if debug:
                            print grammar_relation
                            print words_list
            
                        words_list = words_list.split(',')
                        word_1 = words_list[0].split('-')[0]
                        word_2 = words_list[1].split('-')[0].strip() 
                        
                        if debug:
                            print word_1, word_2
                        
                        '''
                        Form the tuple storing relation, word_1 and word_2
                        and add it into the grammar_relations_list. 
                        Exclude all root relations which are not of any interest
                        to us. Root relation shows the relation of root to
                        head word in the parse tree for a sentence
                        '''
                        if grammar_relation == "root":
                            continue

                        relation_tuple =  (grammar_relation, \
                                           word_1.lower(), word_2.lower())

                        grammar_relations_list.append(relation_tuple)
                        
        if debug:
            print len(grammar_relations_list)

        '''
        Get the freq of each relation present in grammar_relations_list.
        The freq of relations will be stored into a dict object called 
        rel_freq which has a tuple of (relation,word_1,word_2) as keys and
        freq of this tuple into grammar_relations_list as the values.This
        dict object will be used in building co-occurrence vector.
        These freq will be calculated using Counter object.
        '''

        # create rel_freq

        rel_freq = {}

        rel_freq_counter =  collections.Counter(grammar_relations_list)

        if debug:
            print grammar_relations_list
            print rel_freq_counter

        # iterate over rel_freq_counter and feed in the freq in rel_freq

        for rel_freq_counts  in rel_freq_counter.most_common():
            rel_freq[rel_freq_counts[0]] = rel_freq_counts[1]

        if debug:
            print rel_freq
        
        
        '''
        Build the co-occurrence vector (CV) out of grammar_relations_list. The
        CV shows how many times a relation to a word is co-occurring with
        another word.  Our CV will be a python dict object with name cv_dict. 

        Our grammar_relations_list has relations in the form :
        (rel, word_1, word_2)

        This means  'word_1' has relation 'rel'  with 'word_2' and also, 
        'word_2' has same relation 'rel' with 'word_1'

        Thus for each entry in grammar_relations_list, we will have two entries 
        in CV cv_dict. 

        One entry has word_1 as the key and a list 
        of relation features as the values for that key. This relation feature 
        list in turn will have a dict object as its element. 
        These dict object will have a tuple of (rel,word_2) as the key and
        freq of co-occurrence of word_1 with (rel,word_2)

        Second entry will be word_2 as the key and 
        list of dicts with key (rel,word_1) and co-occurrence freq of word_2 
        with (rel,word_1) as the values.

        For example, if grammar_relations_list has following elements into to 
        it:

        [(nn, George, Bush),(adj, Good, George)]

        Then cv_dict will be like this:

        -----------------------------------------------------------------
        |   word (key)    |   list of dict of relation features (value) |
        -----------------------------------------------------------------
        |   George        | [ {(nn,Bush}:1}, {(adj,Good)}:1]            |
        -----------------------------------------------------------------
        |   Bush          | [ {(nn,George):1} ]                         |
        -----------------------------------------------------------------
        |  Good           | [ {(adj,George):1}                          |
        -----------------------------------------------------------------
        
        Also maintain a dict object feature_freq_dict that will have 
        mapping of each feature relation to its frequency in the 
        grammar_relations_list.
        
        e.g. for above mentioned cv_dict , feature_freq_dict will have 
        following contents
        {(nn,Bush}:1 , (adj,Good):1 , (nn,George):1, (adj,George):1 }

        '''

        # create cv_dict and feature_freq_dict
        cv_dict = {}
        feature_freq_dict = {}

        # iterate over rel_freq dict to build CV

        for rel, freq in rel_freq.iteritems():

            relation = rel[0]
            word_1 = rel[1]
            word_2 = rel[2]

            if debug:
                print rel , freq
                print relation, word_1, word_2
            
            '''
            Form tuples (rel, word_1) and (rel, word_2) to insert them 
            into cv_dict rel features' list
            '''
            tuple_1 = (relation,word_2)
            tuple_2 = (relation,word_1)

            '''
            For the dict objects for elements in rel feature's list
            '''
            feature_dict_1 = {}
            feature_dict_2 = {}
            feature_dict_1[tuple_1] = freq
            feature_dict_2[tuple_2] = freq

            # feed in the values into cv_dict

            if word_1 not in cv_dict.keys():
                new_list = [feature_dict_1]
                cv_dict[word_1] = new_list
            else:
                existing_list = cv_dict[word_1]
                existing_list.append(feature_dict_1)
                cv_dict[word_1] = existing_list
   
            if word_2 not in cv_dict.keys():
                new_list = [feature_dict_2]
                cv_dict[word_2] = new_list
            else:
                existing_list = cv_dict[word_2]
                existing_list.append(feature_dict_2)
                cv_dict[word_2] = existing_list
 
            
            # feed in the values into feature_freq_dict
            if tuple_1 not in feature_freq_dict.keys():
                feature_freq_dict[tuple_1] = freq
            else:
                prev_count_1 = feature_freq_dict[tuple_1]
                feature_freq_dict[tuple_1] = prev_count_1 + freq


            if tuple_2 not in feature_freq_dict.keys():
                feature_freq_dict[tuple_2] = freq
            else:
                prev_count_2 = feature_freq_dict[tuple_2]
                feature_freq_dict[tuple_2] = prev_count_2 + freq

        if debug:
            print cv_dict
            print feature_freq_dict

        '''
        Get the max likelihood Probabilities for features i.e. P(f) of
        section 20.7.2 of JM text. These Probabilities will be stored
        in a dict object p_f which will have features as the keys and
        their Probabilities as the values.

        These Probabilities will be calculated in log space.
        '''
        
        # first get the total count of features 
        total_features = 0

        for feature, freq in feature_freq_dict.iteritems():
            
            total_features = total_features + freq

        if debug:
            print total_features
            
        # create pf_ dict
        p_f ={}

        for feature, freq in feature_freq_dict.iteritems():
            p_f[feature] =  math.log10(freq) - math.log10(total_features)

        if debug:
            print p_f
    
        '''
        Calculate the MLE of joint probability of a feature f with word w from 
        the cv_dict. These joint Probabilities will be stored in a cv_dict  
        only and it corresponds to P(f,w) of section 20.7.2 of JM text.

        Here cv_dict will be modified to hold P(f,w) instead of freq. This 
        modification will avoid creation of another data structure for P(f,w).
    
        First iterate over cv_dict to get sum of counts of related word w', 
        which is used to calculate P(f,w). 
        
        Divide value of each freq by this sum in log space to get P(f,w)
        
        '''
        for word, relation_feature_list in cv_dict.iteritems():
                w_prime_sum = 0
                for relation_feature in relation_feature_list:
                    w_prime_sum = w_prime_sum + relation_feature.values()[0]
                
                for relation_feature in relation_feature_list:
                    for key, value in relation_feature.iteritems():
                        
                        relation_feature[key] = math.log10(value) - \
                        math.log10(w_prime_sum)
                    

        '''
        Next calculate the association measures for the CV. The association 
        measure used in this program is t-test. The association measure for
        each feature and word is stored in the cv_dict only. cv_dict will 
        be modified to hold association measures instead of probabilities here.
        '''
        for word, relation_feature_list in cv_dict.iteritems():
                
            # get P(w) for word from p_w dict
            try:
                word_prob = p_w[word]
            except KeyError:
                word_prob = float(-7)

            for relation_feature in relation_feature_list:
                for key, value in relation_feature.iteritems():
                    assoc_factor_1 = pow(10, value)

                    # get P(f) from p_f dict
                    feat_prob = p_f[key]
                    assoc_factor_2 = pow(10, word_prob + feat_prob)
                    
                    assoc_measure =  float(assoc_factor_1 - assoc_factor_2) /\
                                     float(math.sqrt(assoc_factor_2))
                    relation_feature[key] = assoc_measure


        '''
        Start finding words similar to the words present in target_words_file.
        For finding similarity Jaccard measure will be used. For finding 
        similarity, the CV present for each target word will be compared 
        with CVs of other words using Jaccard's measure formula.
        
        For this, features' list for both target and other word in cv_dict 
        will be fetched first. The unique features from features' list of
        target and other word will be inserted into a composite list.
        
        Using this composite list, the association measures of target word
        and other word will be compared for each word. Sum of minimum of
        association measures for all features and sum of max of association
        measures for all features will be calculated and division of these
        two sums will give us Jaccard's similarity score for target and other
        words. Similarity score of all other words will be put in word_sim dict 
        and top 20 scores will be displayed as output. 
        '''
        
        # iterate over the target word list to fetch target words
        for target_word in target_words_list:

            # create word_sim dict object
            word_sim = {}

            target_word = target_word.replace("\n","")
            
            # get features' list for target word from cv_dict
            target_feature_list = cv_dict[target_word]
            
            # iterate over cv_dict to get other word's features' list

            for key, data in cv_dict.iteritems():
                
                composite_feature_list = []

                other_feature_list = data
                
                ''' 
                form a composite list containing unique features from both
                target features list and other word's feature list
                '''
                for feature in target_feature_list:
                    composite_feature_list.append(feature.keys()[0])

                for feature in other_feature_list:
                    if feature.keys()[0] not in composite_feature_list:
                        composite_feature_list.append(feature.keys()[0])

                
                '''
                Iterate over composite list to get sum of min and sum of max 
                of the two lists.
                '''
                sum_of_min = 0
                sum_of_max = 0

                for element in composite_feature_list:
                    target_assoc_measure = 0 
                    other_assoc_measure = 0 
                   
                    
                    for feature in target_feature_list:
                        if element == feature.keys()[0]:
                            target_assoc_measure = feature.values()[0] 
                            break

                    for feature in other_feature_list:
                        if element == feature.keys()[0]:
                            other_assoc_measure = feature.values()[0]
                            break
    
                    min_value = min(target_assoc_measure, other_assoc_measure)
                    max_value = max(target_assoc_measure, other_assoc_measure)


                    sum_of_min = sum_of_min + min_value
                    sum_of_max = sum_of_max + max_value
                
                '''
                Calculate Jaccard's similarity value by dividing sum_of_min
                by sum_of_max
                '''
                try:
                    similarity_value =  sum_of_min / sum_of_max
                except ZeroDivisionError:
                    similarity_value = 0


                word_sim[key] = similarity_value
                
               
            print "Target word: " + target_word  + "\n"
            
            print "Target word frequency in corpus: " + \
                str(word_frq_dict[target_word]) + "\n"
        
    
            print "Similar words and their similarity scores : " + "\n" 

            word_counter = 0
            
            '''
            Sort word similarity dict by values. For this, the code
            given in this link was used to sort a dict by values:
            http://www.saltycrane.com/blog/2007/09/
            how-to-sort-python-dictionary-by-keys/
            '''

            for key, value in sorted(word_sim.iteritems(), \
                                     key=lambda (k,v): (v,k)\
                                , reverse=True):
                if word_counter == num_of_sim_words:
                    break    
                   
                '''
                For table like pretty printing of output, format specifier : 
                is used as described on Python 2.7.3 documentation 
                present at the link:
            
                http://docs.python.org/tutorial/inputoutput.html
            
                The sample code referred from above link was
                print '{0:10} ==> {1:10d}'.format(name, phone)
                '''
 
                print '{0:30}      {1:30}     '.format(key, \
                                                   str(value))
 
                word_counter = word_counter + 1
            
            print "\n\n"

    else:
        print "No parameter passed to the program !"
    
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
# End of word_sim.py program
#############################################################################

