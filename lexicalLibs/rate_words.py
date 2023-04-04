import pandas as pd
import nltk

# calculate number of phonemes and syllables using the CMU pronouncing dict
def get_phondict():
	# get the CMU dict as a dataframe
	phonDf = pd.DataFrame.from_dict(nltk.corpus.cmudict.dict(), orient='index')
	phonDf = phonDf.reset_index()
	# count number of phonemes and make it as a column of df
	phonDf['phon'] = phonDf[0].map(len)
	# drop unnecessary columns and clean the df
	phonDf = phonDf.drop(columns=[1,2,3,4])
	phonDf.columns = ['word','pron','phon']
	# comma-join the phonemes and count syllables 
	phonDf['pronstring'] = [','.join(map(str, l)) for l in phonDf['pron']]
	phonDf['syll'] = phonDf.pronstring.str.count("0|1|2")

	return phonDf

# rate lexical measures for each word
def attach_lexical(document, measureDict, phonDf):
	# make a df from a cleaned text	
	words = pd.DataFrame({'word': [w.text.lower() for w in document], 'lemma':[w.lemma_ for w in document],'pos':[w.pos_ for w in document]})
	# remove punctuation marsk
	words = words[words.pos != "PUNCT"]
	# rate lexical measures based on word and lemma
	word_lexical = pd.merge(words, measureDict, on='word', how='left')
	lemma_lexical = pd.merge(words[["lemma", "pos"]], measureDict, left_on='lemma', right_on='word', how='left')
	# if word-level lexical measures are not available, use lemma-based lexical measures
	df = word_lexical.fillna(lemma_lexical)
	# merge with the phone df
	df = pd.merge(df, phonDf[["word", "phon", "syll"]], on='word', how='left')

	# fill out phoneme and syllable counts for contracted words (not included in the CMU pronunciation dict)
	df.loc[df.word=="'s",["phon","syll"]] = df.loc[df.word=="'ve", ["phon","syll"]] = df.loc[df.word=="'ll", ["phon","syll"]] = df.loc[df.word=="'m", ["phon","syll"]] = df.loc[df.word=="'d", ["phon","syll"]] = df.loc[df.word=="'re", ["phon","syll"]] = [1,0]
	df.loc[df.word=="n't", ["phon","syll"]] = [2,0]
	df.loc[df.word=="gon", ["phon","syll"]] = df.loc[df.word=="wan", ["phon","syll"]] = [3,1] # as in gonna or wanna
	df.loc[df.word=="wo", ["phon","syll"]] = df.loc[df.word=="na", ["phon","syll"]] =[2,1] # as in won't or wanna

	return df 

# summarize lexical measures after rating words
def lexical_summary(lexical_df):
	# get mean values of the rated lexical measures of all words in a given df
	allwords = pd.DataFrame(lexical_df.iloc[:, 3:].mean()).transpose()
	# rename columns
	allwords.columns = ['frequency_all', 'AoA_all','familiarity_all','ambiguity_all','concreteness_all','phone_all','syll_all']
	# count total number of syllables from all words
	total_syll = lexical_df.iloc[:,-1].sum()
    
    # get mean values of the lexical measures of all nouns 
	nouns = lexical_df[lexical_df.pos=='NOUN']
	nouns_mean = pd.DataFrame(nouns.iloc[:, 3:].mean()).transpose()
	nouns_mean.columns = ['frequency_noun', 'AoA_noun','familiarity_noun','ambiguity_noun','concreteness_noun', 'phone_noun', 'syll_noun']
    
    # get mean values of the lexical measures of all content words
	content = lexical_df[(lexical_df.pos=='NOUN') | (lexical_df.pos=="ADV") | (lexical_df.pos=="ADJ") | (lexical_df.pos=="VERB")]
	content_mean = pd.DataFrame(content.iloc[:, 3:].mean()).transpose()
	content_mean.columns = ['frequency_content', 'AoA_content','familiarity_content','ambiguity_content','concreteness_content', 'phone_content', 'syll_content']

    # combine all lexical measure dfs
	all_df = pd.concat([allwords, nouns_mean], axis=1)
	all_df2 = pd.concat([all_df, content_mean], axis=1)
	all_df2['total_syll'] = total_syll

	return all_df2