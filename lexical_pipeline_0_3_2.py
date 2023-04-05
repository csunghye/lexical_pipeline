### Usage1: 
# python3 lexical_pipeline_0_3_2.py -output_file ../speechbiomarkers/summarized_lexical_20210413.csv -input_folder ../speechbiomarkers/picture -filetype .txt -label_existing False
## V0.3.2: 2023-April-4

## Check if all packages are installed and if not, install them. 

import spacy
import argparse, glob, platform
import pandas as pd
import numpy as np
from lexicalrichness import LexicalRichness
from lexicalLibs.prep_text import read_transcript, clean_doc
from lexicalLibs.count_words import convert100, count_pos
from lexicalLibs.rate_words import get_phondict, attach_lexical, lexical_summary

# location of the aggregated lexical measure file
LEXICAL_LOOKUP = 'all_measures_raw.csv'

# load nlp model
nlp = spacy.load('en_core_web_lg')

# main function
def main(args):
	# define output file
	outputname = args.output_file

	# check the OS of a user
	user_os = platform.system()
    # assign path separator (backslash or forward-slash depending on the os of the user)
	if user_os == "Windows":
		file_separator = '\\'
	else:
		file_separator = '/'

	# get a list of files to process
	filelist = glob.glob(args.input_folder+file_separator+'*'+args.filetype)
	print("List of files to be processed: ", filelist, " If empty, check your directory path and file extension again.")

	# get lexical measures to use
	measureDict = pd.read_csv(LEXICAL_LOOKUP)
	phonDf = get_phondict()
	
	# initiate result dataframes
	allResults = pd.DataFrame()
	full_df = pd.DataFrame()

	# loop through the file list
	for file in filelist:
		print(file, " is being processed...")
        
		# read a transcript (transcripts need to be tab-separated!)
		text = read_transcript(pd.read_csv(file, sep='\t'), args)
		# run first-pass pos tagging on the entire doc (POS tags are used to exclude repetitions)
		doc = nlp(text)
		# clean the doc
		cleaned_text, total_word, um, uh, eh, hm, yeah, partial, repetition, restart = clean_doc(doc)
		# tally the total word count + dysfluency markers
		total = total_word + um + uh + eh + hm + yeah + partial + repetition
		# run second-pass pos tagging on cleaned texts only (without dysfluency markers)
		doc = nlp(cleaned_text)
		# get lexical diversity measures (lex is used to calculate lexical diversity)
		lex = LexicalRichness(cleaned_text, use_TextBlob = True)

		# count pos categories and dysfluency markers
		pos_counts, tag_counts, uniqueAllCount, uniqueContentCount, uniqueNounCount, uniqueAdjCount, uniqueVerbCount, uniqueAdvCount = count_pos(doc)
		other_dict = {"um":um,"uh":uh,"eh":eh,"hm":hm,"yeah":yeah,"partial":partial,"repetition":repetition, "restart":restart, "uniqueAll": uniqueAllCount, "uniqueContent": uniqueContentCount, "uniqueNoun": uniqueNounCount, "uniqueAdj": uniqueAdjCount, "uniqueVerb": uniqueVerbCount, "uniqueAdv": uniqueAdvCount}
		
		# combine the two dicts
		pos_counts = {**pos_counts, **other_dict}
		# convert to counts per 100 words
		pos100 = convert100(dict(pos_counts), total)
		tag100 = convert100(dict(tag_counts), total)
		# make the counts as a data frame
		pos_all = pd.DataFrame({**pos100, **tag100}, index=[0])

		# rate lexical measures
		lexical = attach_lexical(doc, measureDict, phonDf)
		lexical['filename'] = file.split(file_separator)[-1]
		# combine pos and dysfluency counts and lexical measures 
		full_df = pd.concat([full_df, lexical]) 
		lexical = lexical.drop(['filename'], axis=1)
		
		# calculate averaged lexical measure
		lexicalSumDF = lexical_summary(lexical) 
		# combine counts and lexical measure dfs
		result = pd.concat([pos_all, lexicalSumDF], axis=1)
		# add additional columns to the combined df
		result['filename'] = file.split('/')[-1]
		result['total_words'] = total_word
		result['total_words_plus_others'] = total
		
		# calculate lexical diversity by window and document (lex.words) size
		if lex.words > 25: # if the doc contains more than 25 words, calculate lexical diversity for all window size
			result['lexical_diversity_25'] = lex.mattr(window_size=25)
			result['lexical_diversity_20'] = lex.mattr(window_size=20)
			result['lexical_diversity_15'] = lex.mattr(window_size=15)
		elif lex.words > 20:
			result['lexical_diversity_25'] = np.NaN
			result['lexical_diversity_20'] = lex.mattr(window_size=20)
			result['lexical_diversity_15'] = lex.mattr(window_size=15)
		elif lex.words > 15:
			result['lexical_diversity_25'] = np.NaN
			result['lexical_diversity_20'] = np.NaN
			result['lexical_diversity_15'] = lex.mattr(window_size=15)
		else: # if doc contains fewer than 15 words, lexical diversity is not calculated
			result['lexical_diversity_25'] = np.NaN
			result['lexical_diversity_20'] = np.NaN
			result['lexical_diversity_15'] =np.NaN
		# update the allResults df with the processed doc
		allResults = pd.concat([allResults, result], sort=True)
	# define column names for all pos categories
	col_na = ['ADJ','ADP','ADV','CC','CCONJ','CD','DET','DT','EX','FW','IN','INTJ','JJ','JJR','JJS','MD','NN','NNP','NNPS','NNS','NOUN','NUM','PART','PDT','POS','PRON','PROPN','PRP','PRP$','RB','RBR','RBS','RP','TO','UH','VB','VBD','VBG','VBN','VBP','VBZ','VERB','WDT','WP','WP$','WRB','X','XX']
	# if the doc included zero instances of a given pos count, insert 0 for zero count
	for col in col_na:
		if col in allResults:
			allResults[col].fillna(0, inplace=True)
		else:
			allResults[col] = 0

	# count the number of tense_inflected verbs
	allResults['tense_inflected_verb'] = allResults['MD'] + allResults['VBD'] + allResults['VBP'] + allResults['VBZ']	
	# count total filler counts
	allResults['filler'] = allResults['um']+allResults['uh']+allResults['eh']
	# output allResults df (this is a word by word dataframe)
	allResults.to_csv(outputname, index=False)
	# output a summarized simple result file (this is for collaborators)
	smalldf = allResults[['filename','NOUN','VERB','ADJ','ADV','ADP','DET','PRON','CCONJ','PART','NUM','filler','partial','repetition','tense_inflected_verb','lexical_diversity_15','total_words', 'total_words_plus_others','uniqueContent','concreteness_content','frequency_content','AoA_content','familiarity_content','phone_content','ambiguity_content','total_syll']]
	external_filename = outputname.split('.')[0]+'_simple.csv'
	smalldf.to_csv(external_filename, index=False)
	# output a summarized full result file (this is generally for internal use.)
	full_filename = outputname.split('.')[0]+'_full.csv'
	full_df.to_csv(full_filename, index=False)


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-output_file', type=str, required=True, help='Name the output file')
	parser.add_argument('-input_folder', type=str, required=True, help='Folder containing input documents')
	parser.add_argument('-filetype', type=str, required=True, help='Input file extensions')
	parser.add_argument('-label_existing', required=True, help='Boolean for having a speaker label or not')
	parser.add_argument('-speaker_label', required=False, nargs='+', help='Speaker label of interest')
	args = parser.parse_args()
	main(args)
	
			
