# Lexical pipeline

This pipeline automatically tags part-of-speech (POS) categories using a large language model for English in spacy (https://spacy.io) and rates several lexical characteristics of all words, including word frequency, age of acquisition (AoA), word familiarity, semantic ambiguity, concreteness, word length (in number of phonemes and syllables). It also measures total number of words, dysfluency counts ("um", "uh", "eh", partial words, repetitions), and lexical diversity in moving-window averaged type-token ratio with varying window sizes (from 15 words to 25 words with a 5-word increment). The program generates three output files: one with the name a user provides when running the pipeline, which includes all summarized measures, another ending in "_full.csv", which includes un-summarized results with word-by-word lexical characteristics, and the other ending in "_simple.csv", which selected summarized measures. In usual use cases, the simple version will suffice users' needs. 

## Dependency
To run this program, you will need to install the following packages:
- spacy
- nltk
- LexicalRichness
- pandas
- numpy

## Check before running the program
- You will need transcripts (whether automatically transcribed or manually transcribed) to run this program. 
- This program assumes that transcripts are in a WebTrans-like format, where 6 or 7 columns are tab-separated in this order: [(Kit,) Audio, Start, End, Text, Speaker, Task]. The column names do not need to be like this, but the order must be in this specific order with the exception that the first column (Kit) can be omited. If not in this format, please reformat your transcripts before running. 

## Citations
It is very important to cite all of the following papers when you use the pipeline:
### For the lexical measures:
- Word frequency:
- Word familiarity:
- Semantic Ambiguity:
- Age of acquisition:
- Concretenss:
- Word length:
- Lexical diversity: 

### For the dependencies used:
- spacy:
- LexicalRichness:
- NLTK:
- CMU Pronouncing Dictionary:

### For the current pipeline:
- 

## Column names
You can check what the column names mean in the lexical_glossary.csv file!

If you encounter any issues, please contact me via csunghye@sas.upenn.edu
