import urllib.error
from urllib.request import urlopen

from bs4 import BeautifulSoup
from natasha import Doc, Segmenter, NewsEmbedding, NewsMorphTagger, MorphVocab

is_skip_downloading = True

files_folder = "pages/"
index_file_name = "index.txt"

all_tokens_file = "tokens.txt"
lemmas_tokens_file = "lemmas.txt"
inverted_indexes_file = "inverted_indexes.txt"

""" task 1 """

if not is_skip_downloading:
    main_link = "https://habr.com/ru/post/"
    post_id = 717142

    # url = "https://habr.com/ru/post/717142" # normal
    # url = "https://habr.com/ru/post/708442" # moved
    # url = "https://habr.com/ru/post/708042" # removed

    index_file = open(index_file_name, 'w', encoding="utf-8")
    delta_i = 0
    for i in range(0, 100):
        while True:
            current_i = i + delta_i
            url = main_link + str(post_id - current_i * 100)
            try:
                with urlopen(url) as response:
                    body = response.read().decode()
                    with open(files_folder + str(i) + ".txt", 'w', encoding="utf-8") as f:
                        f.write(body)
                    index_file.write(str(i) + " " + url + "\n")
                print(i, "finished")
                break
            except urllib.error.HTTPError:
                print("Error on page", (post_id - current_i * 100))
                delta_i += 1
    index_file.close()

""" task 2 """

useful_tags = ['ADJ', 'NOUN', 'PROPN', 'VERB']

segmenter = Segmenter()
morph_vocab = MorphVocab()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)

all_lemmas = {}
all_lemmas_indexes = {}

for i in range(0, 100):
    f = open(files_folder + str(i) + ".txt", 'r', encoding="utf-8")
    soup = BeautifulSoup(f.read(), features="html.parser")
    f.close()

    # remove css & js
    for script in soup(["script", "style"]):
        script.extract()
    # get text
    text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = ' '.join(chunk for chunk in chunks if chunk)

    doc = Doc(text)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)

    for token in doc.tokens:
        if token.pos in useful_tags:
            token.lemmatize(morph_vocab)
            lemma = token.lemma.lower()
            if lemma not in all_lemmas:
                all_lemmas[lemma] = set()
                all_lemmas_indexes[lemma] = set()
            all_lemmas[lemma].add(token.text.lower())
            all_lemmas_indexes[lemma].add(i)

# https://melaniewalsh.github.io/Intro-Cultural-Analytics/05-Text-Analysis/13-POS-Keywords.html

# task 3 starts from part of 2 task
lem_f = open(lemmas_tokens_file, 'w', encoding="utf-8")
tot_f = open(all_tokens_file, 'w', encoding="utf-8")
ind_f = open(inverted_indexes_file, 'w', encoding="utf-8")

for key in all_lemmas.keys():
    lem_f.write(key + ":")
    for s_el in all_lemmas[key]:
        lem_f.write(" " + s_el)
        tot_f.write(s_el + "\n")
    lem_f.write("\n")

    ind_f.write(key)
    for i_el in all_lemmas_indexes[key]:
        ind_f.write(" " + str(i_el))
    ind_f.write("\n")

lem_f.close()
tot_f.close()
ind_f.close()

