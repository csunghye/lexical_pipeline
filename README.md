# Lexical pipeline

This pipeline automatically tags part-of-speech (POS) categories using a large language model for English in spacy (https://spacy.io) and rates several lexical characteristics of all words, including word frequency, age of acquisition (AoA), word familiarity, semantic ambiguity, concreteness, word length (in number of phonemes and syllables). It also measures total number of words, dysfluency counts ("um", "uh", "eh", partial words, repetitions), and lexical diversity in moving-window averaged type-token ratio with varying window sizes (from 15 words to 25 words with a 5-word increment). The program generates three output files: one with the name a user provides when running the pipeline, which includes all summarized measures, another ending in "_full.csv", which includes un-summarized results with word-by-word lexical characteristics, and the other ending in "_simple.csv", which contains selected summarized measures. In usual use cases, the simple version will suffice users' needs. 

## Dependency
To run this program, you will need to install the following packages: (need to include versions...)
- spacy
- nltk
- LexicalRichness
- pandas
- numpy

## Check before running the program
- You will need transcripts (whether automatically transcribed or manually transcribed) to run this program. 
- This program assumes that transcripts are in a WebTrans-like format, where 6 or 7 columns are tab-separated in this order: [(Kit,) Audio, Start, End, Text, Speaker, Task]. The column names do not need to be like this, but the order must be in this specific order with the exception that the first column (Kit) can be omited. If not in this format, please reformat your transcripts before running. 

## How this program works
[to be explained soon]

## Citations
It is very important to cite all of the following papers when you use the pipeline:
### For the lexical measures:
- Word frequency: https://link.springer.com/article/10.3758/BRM.41.4.977
- Word familiarity: https://link.springer.com/article/10.3758/s13428-018-1077-9
- Semantic Ambiguity: https://link.springer.com/article/10.3758/s13428-012-0278-x
- Age of acquisition: https://link.springer.com/article/10.3758/s13428-018-1077-9
- Concretenss: https://link.springer.com/article/10.3758/s13428-013-0403-5
- Word length: http://www.speech.cs.cmu.edu/cgi-bin/cmudict
- Lexical diversity: https://www.tandfonline.com/doi/pdf/10.1080/09296171003643098

### For the current pipeline:
- Cho, Sunghye, Naomi Nevler, Sharon Ash, Sanjana Shellikeri, David J. Irwin, Lauren Massimo, Katya Rascovsky, Christopher Olm, Murray Grossman, and Mark Liberman. (2021). Automated analysis of lexical features in Frontotemporal Degeneration. Cortex 137, 215-231. https://www.sciencedirect.com/science/article/abs/pii/S001094522100037X

## Column names
You can check what the column names mean in the lexical_glossary.csv file!

## Things to be done in the future

If you encounter any issues, please contact me via csunghye@sas.upenn.edu
