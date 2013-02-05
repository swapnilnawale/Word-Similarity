##############################################################################
# Algorithm     :   This program extracts all sentences from the corpus
#                   files and does the full parsing of those sentences using
#                   Standford parser.
#                   
#                   Steps followed in this program are:
#
#                   1) This program first reads all corpus files and extracts
#                      sentences from first 500000 <P> tags present in the 
#                      corpus files. Only sent. from 50000 <P> tags are 
#                      considered because
#                      Standford Parser takes a lot of time to do parsing of
#                      each sentence.
#                   
#                   2) To extract sentence from <P> tags xml parser is used.
#
#                   3) Each parsed sentence is written to a file.
#                   
#                   4) File generated in step 3 is split into multiple small 
#                      files.
#
#                   5) Each of these small file is given as input to
#                      Standford Parser to create parse file containing
#                      grammatical relations of words in sentences.
##############################################################################

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

# threading module used to do multithreading
import threading

# ElementTree module used for xml parsing
import xml.etree.ElementTree as ET

###############################################################################
# Function      : absoluteFilePaths(directory)
# Description   : This function returns the list containing absolute paths
#                 of all files present in the directory passed as an
#                 argument to it.
# Arguments     : directory - The path of directory for which listing is 
#                             required
# Returns       : List containing absolute paths of files under the directory
###############################################################################

def absoluteFilePaths(directory):
    # create a list to hold absolute path of files
    file_paths = []
    # iterate over the directory listing and fetch absolute paths of file
    for dirpath,_,filenames in os.walk(directory):
        for f in filenames:
            file_paths.append(os.path.abspath(os.path.join(dirpath, f)))
    return file_paths

###############################################################################
# End of absoluteFilePaths function
###############################################################################

###############################################################################
# Function      : parseFile(file_name)
# Description   : This function makes a call to Standford parser to parse
#                 file given as argument to it. It stores the output of parsed
#                 files into a file with name as <file_name>.parse. Note that
#                 <file_name> is same as the file_name argument here.
# Arguments     : file_name- Name of the file to be parsed
# Returns       : None
###############################################################################

def parseFile(file_name):
    print "Parsing " +  file_name + "...."
    
    # Make a call to Standford Parser
    os.system("java -mx2048m -cp \"./*:\" \
              edu.stanford.nlp.parser.lexparser.LexicalizedParser\
              -outputFormat \"typedDependenciesCollapsed\" -maxLength 60  \
              edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz " + \
              file_name+ " >" + file_name + ".parse")

    '''
    Standford parser does full parsing of sentences present in a file.
    The parsing of sentences generates grammatical relations of words
    present in a sentence. The o/p of parsing is stored in parse file.

    A typical grammatical relation in any parse file looks like this:
        
        <grammatical_relation>(<word_1_in_relation> - 
                               <index_of_word_1_in_sentence>, 
                               <word_2_in relation> - 
                               <index_of_word_2_in_sentence>)
        
        E.g. if the original sentence in the file is :
        
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

    '''

###############################################################################
# End of main function
###############################################################################

###############################################################################
# Function      : main()
# Description   : Entry point for the project.
# Arguments     : None. Command Line Arguments in Python are retrieved from
#                 sys.argv variable of sys module.
# Returns       : None.
###############################################################################
def main():

    '''
    Get the values of command line arguments for :
    1) Path of directory containing all corpus files
    2) Path where the files split from corpus files and parsed files
       will be placed
    3) Base path of Standford Parser
    '''
	document_path = sys.argv[1]
	split_file_path = sys.argv[2]
	parser_base_path = sys.argv[3]

    '''
    Create a o/p file named as "op_file". This file will contain the
    all sentences present in <P> tags of the corpus files. As mentioned
    in main program, only few sentences from corpus files will be extracted
    and put into op_file. To be exact, sentences from first 500000 <P> will
    be used here. This file op_file is referred as sentence file hereafter in
    the program.
    '''
	op_file =  open("op_file","w")

	'''
    Create a directory to hold files split from sentence file and to store
    parsed files generated by Standford Parser.

    The code to generate a directory in Python is borrowed from this question
    asked at stackoverflow.com
    
    http://stackoverflow.com/questions/273192/
    python-best-way-to-create-directory-if-it-doesn't-exist-for-file-write
    
    '''
    if not os.path.exists(split_file_path):
		os.makedirs(split_file_path)


    '''
    Get the list of all corpus files present in document_path directory. 
    The code to get directory listing from a directory is borrowed from
    the link:
	http://mail.python.org/pipermail/tutor/2004-August/031232.html
    '''

	docsList=os.listdir(document_path)

	loop_counter = 0

	'''
    Iterate over each corpus file to extract sentences from <P> tags
    '''
    for document in docsList:
		
		print "Processing document " +  document + "..."

        '''
        Open and read corpus file into a list doc_lines
        '''
		doc_handle =  open(document_path + "/" + document,'r')
		doc_lines =  doc_handle.readlines()
		doc_handle.close()

        '''
        Since I want to
        retrieve the sentences of <P> tags, I need to do xml parsing of the
        corpus file. To facilitate xml parsing, add <DUMMY> tag as root
        of all <DOC> tags present in the corpus file. 
        
        This is required as there are many xml files in each corpus file with 
        <DOC> as their root tag. Adding <DUMMY> tag will convert all those
        many xml files as a single xml file with <DUMMY> root tag. The <DUMMY>
        opening and closing tags will be added to doc_lines list.
        '''

		doc_lines.insert(0,"<DUMMY>")
		doc_lines.append("</DUMMY>")
		
        '''
        All corpus files have some xml character entities like &AMP; and &amp;.
        These entities represent the word "and" (basically symbol &). These
        entities cause problem in xml parsing as the xml parser does not 
        recognize them. So replace these entities with word "and".
        And write the converted contents of doc_lines into a file with same
        name as the original corpus file.

        Thus our new corpus file will have <DUMMY> tag as root and all 
        character entities replaced with "and". 
        '''
        
        doc_handle =  open(document,'w')
		
		for line in doc_lines:
			
			if "&AMP;" in line or "&amp;" in line: 
				line = line.replace("&AMP;", "and").replace("&amp;", "and")

			if "&" in line:
				line = line.replace("&", "")

			if line != "\n":
				doc_handle.write(line)

		doc_handle.close()

		
        '''
        Next parse each corpus file using Python's xml parser provided by
        ElementTree module. Extract all sentences present in the <P> tags.

        And write them into op_file. Stop writing after extracting sentences 
        from first 500000 <P> tags. Thus the extracted sentences from these
        first 500000 <P> tags will act as a small subset of corpus and will
        be used for further processing. This is required as Standford Parser
        takes a lot of memory and time to do full parsing. And because of this,
        we will do parsing of sentences of belonging to 
        first 500000 <P> tags only.
        '''
        tree = ET.parse(document)
		root = tree.getroot()

		for child in root.iter():
			if child.tag == "P":
				para_text = str(child.text).rstrip()
				op_file.write(para_text)
				loop_counter = loop_counter + 1


        '''
        Stop when first 500000 <P> tag sentences are extracted. 
        Here, our op_file has sentences from 500000 <P> tags.
        Next split op_file into multiple files containing 10000 lines
        of text. For splitting files, UNIX utility split will be used.
        The total number of lines in op_file was 2,559,717 and after 
        splitting them into files of 10000 lines, we get total 256 
        split files.


        This splitting is required as we can feed these split files to
        Standford Parser in concurrent fashion. These split files will 
        be stored in the directory specified by command line argument
        split_file_path.
        '''
		if loop_counter >= 500000:
			op_file.close()
			os.chdir(split_file_path)
			print "Splitting the output file ..."
			os.system("split -l 10000 ../op_file")
			break

	
    '''
    Get the list of all absolute path of split files from split_file_path.

    The code to get absolute paths of all files from a directory is taken
    from an answer given by stackoverflow forum user "phihag" for a 
    question asked on the forum. That question is present in the link:

    http://stackoverflow.com/questions/9816816/relative-and-absolute-
    paths-of-all-files

    Call absoluteFilePaths function to get directory listing. It takes
    the relative path of directory for which listing is required.
    '''
    
    file_paths = absoluteFilePaths(".")


	os.chdir("../" + parser_base_path)

    '''
    Next start parsing split files using Standford parser in multithreaded
    manner. For multithreading, Python's module threading will be used.

    To do multithreaded call to Stanford Parser, call parseFile function.

    It takes the name of split file (which we need to parse) as input.

    The parsed output of each split file will be store in split_file_path
    directory only with the extension as ".parse".
    '''

	for i in range(0,10):
		t = threading.Thread(target=parseFile, args=[file_paths[i]])
		t.start()
		 
	op_file.close()

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
# End of parse_corpus_sentences.py program
#############################################################################
