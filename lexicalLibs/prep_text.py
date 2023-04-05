import sys

# lists of predefined words
FILLERS = ['um','uh','eh']
BACKCHANNELS = ['hm', 'yeah', 'mhm', 'huh']
EXCEPTION_RULES = ["that 's that", "that is that", "as well as", "as much as", "as ADJ as", "the NOUN the", "do n't do"]
PUNCT = ['.','?',"'"]

# read transcripts and return texts of a speaker only
def read_transcript(transcript, args):
    if 'Text' in transcript.columns:
        pass
    # if a header does not exist, assign a header
    else:
        if len(transcript.columns) == 6:
            transcript.columns = ['Audio', 'Beg', 'End', 'Text', 'Speaker', 'Section']
        elif len(transcript.columns) == 7:
            transcript.columns = ['Kit', 'Audio', 'Beg', 'End', 'Text', 'Speaker', 'Section']
        else:
            sys.exit('The transcript file is not in the right format. Please check again.')

    # if speaker label is used, only return speech of the speaker
    if args.speaker_label:
        text = ' '.join(transcript[transcript['Speaker']==args.speaker_label]['Text'].tolist())
    else:
        text = ' '.join(transcript['Text'].tolist())

    return text

# update the list of previous words to count repetitions
def update_words(prev_bi, prev, word):
	penult_bi = prev_bi
	prev_bi = prev+word.text.lower()
	penult = prev
	prev = word.text.lower()
	prev_pos = word.pos_
	return penult_bi, prev_bi, penult, prev, prev_pos

# count fillers (uses previously defined list)
def count_fillers(word, um, uh, eh):
	if word in FILLERS:
		if word == "um":
			um += 1
		elif word == "uh":
			uh += 1
		else:
			eh += 1
	else: 
		pass

# count backchannels (uses previously defined list)
def count_backchannels(word, hm, yeah):
	if word in BACKCHANNELS:
		if word == "hm":
			hm += 1
		elif word == "yeah":
			yeah += 1
		else:
			pass
	else:
		pass

# clean the transcripts by excluding dysfluency markers and repetitions => This helps improving the pos tagging accuracy. 
def clean_doc(doc):
	# initiate dysfluency marker counts
	um = uh = eh = hm = yeah = partial = restart = 0
	repetitionList = [] 

	# initiate previous words
	prev_bi = penult_bi = prev = penult = prev_pos = 'NA'

	# list of cleaned words to be used for second-pass pos tagging
	cleaned = []

    # loope through words in a doc
	for word in doc:
		if word.pos_ != "SPACE" and word.text != ",":
            # count dysfluency markers
			if (word.text.lower() in FILLERS) or (word.text.lower() in BACKCHANNELS)  or word.text.endswith('-') or word.text.endswith('=') or (word.text == "#"):
				count_fillers(word.text.lower(), um, uh, eh)
				count_backchannels(word.text.lower(), hm, yeah)
				if word.text.endswith('-'):
					partial += 1
				elif word.text.endswith('='):
					repetitionList.append(word.text)
				elif word.text == '#':
					restart += 1 

			else:
                # remove repetitions
				if word.text.lower() != prev: # check if a given word is a repetition of a previous word (e.g., this, <this> boy is ...)
					if word.text.lower() != penult: # check if a given word is a repetition of a preceding word of the previous word (e.g., this, uh, <this> boy ... )
						# if a phrase is not repeated, do not count as a repetition (e.g., This boy, this girl is ... )
						if prev_bi != prev.lower()+word.text.lower() and penult_bi != prev.lower()+word.text.lower():
							cleaned.append(word.text)
							penult_bi, prev_bi, penult, prev, prev_pos = update_words(prev_bi, prev, word)
						else:
							cleaned.pop(-1)
					# do not count as repetition if a phrase is in the exception rules (e.g., as soon <as> possible)	
					elif penult+" "+ prev+" "+ word.text.lower() in EXCEPTION_RULES or penult+" "+prev_pos+" "+word.text.lower() in EXCEPTION_RULES:
						cleaned.append(word.text)
						penult_bi, prev_bi, penult, prev, prev_pos = update_words(prev_bi, prev, word)
					# if the preceding word is a sentence boundary, do not count as a repetition (e.g., She ate this. <This> boy is ...)	
					elif word.text.lower() == penult and (prev == "." or prev == "?"):
						cleaned.append(word.text)
						penult_bi, prev_bi, penult, prev, prev_pos = update_words(prev_bi, prev, word)
					# pass repetition of punctuation marks
					elif word.text in PUNCT and penult in PUNCT:
						pass
					# if a given word is a sentence boundary, do not count as a repetition 
					elif word.text =="." or word.text == "?":
						penult_bi, prev_bi, penult, prev, prev_pos = update_words(prev_bi, prev, word)

					else: # if a preceding word of a previous word is a copy of the given word, count it as a repetition
						repetitionList.append(word)
						penult_bi, prev_bi, penult, prev, prev_pos = update_words(prev_bi, prev, word)
					
				elif word.text in PUNCT and prev in PUNCT:
					pass

				elif word.text == "mm" and prev == "mm": 
					cleaned.pop(-1)
				elif word.text == "mhm" and prev == "mhm":
					cleaned.pop(-1)

				else: # if a previous word is an exact copy of the given word, count it as a repetition
					repetitionList.append(word)
					penult_bi, prev_bi, penult, prev, prev_pos = update_words(prev_bi, prev, word)


	return ' '.join(cleaned), len(cleaned), um, uh, eh, hm, yeah, partial, len(repetitionList), restart
