from collections import Counter

# define content words' pos (DO NOT CHANGE)
CONTENT = ["NOUN", "ADV", "ADJ", "VERB"]

# calculate number of unique words per pos
def add_unique(word, uniqueAll, uniqueContent, uniqueNoun, uniqueAdj, uniqueVerb, uniqueAdv ):
	if word.pos_ in CONTENT:
		if word.pos_ == "NOUN":
			uniqueNoun.add(word.lemma_)
			uniqueContent.add(word.lemma_)
			uniqueAll.add(word.lemma_)
		elif word.pos_ == "ADJ":
			uniqueAdj.add(word.lemma_)
			uniqueContent.add(word.lemma_)
			uniqueAll.add(word.lemma_)
		elif word.pos_ == "ADV":
			uniqueAdv.add(word.lemma_)
			uniqueContent.add(word.lemma_)
			uniqueAll.add(word.lemma_)
		elif word.pos_ == "VERB":
			uniqueVerb.add(word.lemma_)
			uniqueContent.add(word.lemma_)
			uniqueAll.add(word.lemma_)
		else:
			uniqueContent.add(word.lemma_)
			uniqueAll.add(word.lemma_)
	else:
		uniqueAll.add(word.lemma_)
	return uniqueAll, uniqueContent, uniqueNoun, uniqueAdj, uniqueVerb, uniqueAdv

def count_pos(tagged):
	# initiate lists and sets
	posList = tagList = []
	uniqueAll = uniqueContent = uniqueNoun = uniqueAdj = uniqueVerb = uniqueAdv = set()

	for token in tagged:
		if token.pos_ != "PUNCT":
			posList.append(token.pos_)
			tagList.append(token.tag_)
			uniqueAll, uniqueContent, uniqueNoun, uniqueAdj, uniqueVerb, uniqueAdv = add_unique(token, uniqueAll, uniqueContent, uniqueNoun, uniqueAdj, uniqueVerb, uniqueAdv)
	return Counter(posList), Counter(tagList), len(uniqueAll), len(uniqueContent), len(uniqueNoun), len(uniqueAdj), len(uniqueVerb), len(uniqueAdv)


def convert100(dict_item, total):
	dict100 = {k: (v / total)*100 for k, v in dict(dict_item).items()}
	return dict100
