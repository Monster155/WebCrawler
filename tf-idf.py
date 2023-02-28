from bs4 import BeautifulSoup
from natasha import Doc, Segmenter, NewsEmbedding, NewsMorphTagger, MorphVocab

files_folder = "pages/"
tokens_tfidf_files_folder = "tokens/"
lemmas_tfidf_files_folder = "lemmas/"
index_file_name = "index.txt"

all_tokens_file = "tokens.txt"
lemmas_tokens_file = "lemmas.txt"
inverted_indexes_file = "inverted_indexes.txt"

useful_tags = ['ADJ', 'NOUN', 'PROPN', 'VERB']

segmenter = Segmenter()
morph_vocab = MorphVocab()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)

#

all_tokens_indexes = {}
all_lemmas_indexes = {}

for i in range(0, 100):
    with open(files_folder + str(i) + ".txt", 'r', encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), features="html.parser")

    for script in soup(["script", "style"]):
        script.extract()
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = ' '.join(chunk for chunk in chunks if chunk)

    doc = Doc(text)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)

    for token in doc.tokens:
        if token.pos in useful_tags:
            token.lemmatize(morph_vocab)
            lemma = token.lemma.lower()
            text = token.text.lower()

            if lemma not in all_lemmas_indexes:
                all_lemmas_indexes[lemma] = set()
            all_lemmas_indexes[lemma].add(i)

            if text not in all_tokens_indexes:
                all_tokens_indexes[text] = set()
            all_tokens_indexes[text].add(i)

#

for i in range(0, 100):
    with open(files_folder + str(i) + ".txt", 'r', encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), features="html.parser")

    for script in soup(["script", "style"]):
        script.extract()
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = ' '.join(chunk for chunk in chunks if chunk)

    doc = Doc(text)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)

    total_tokens_count = 0
    unique_tokens = {}
    unique_lemmas = {}

    for token in doc.tokens:
        if token.pos in useful_tags:
            token.lemmatize(morph_vocab)
            text = token.text.lower()
            lemma = token.lemma.lower()

            total_tokens_count += 1
            if text not in unique_tokens.keys():
                unique_tokens[text] = 0
            unique_tokens[text] += 1
            if lemma not in unique_lemmas.keys():
                unique_lemmas[lemma] = 0
            unique_lemmas[lemma] += 1

    with open(tokens_tfidf_files_folder + str(i) + ".txt", 'w', encoding="utf-8") as f:
        for key in unique_tokens.keys():
            tf = unique_tokens[key] / total_tokens_count
            f.write(key + " " + str(tf) + " " + str(tf * 100 / len(all_tokens_indexes[key])) + "\n")
    with open(lemmas_tfidf_files_folder + str(i) + ".txt", 'w', encoding="utf-8") as f:
        for key in unique_lemmas.keys():
            tf = unique_lemmas[key] / total_tokens_count
            f.write(key + " " + str(tf) + " " + str(tf * 100 / len(all_lemmas_indexes[key])) + "\n")

# tf = in 1 file = word count / all words
# idf = in all files = all files / files with word
