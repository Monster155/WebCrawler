import urllib.error
from urllib.request import urlopen

from bs4 import BeautifulSoup
from natasha import Doc, Segmenter, NewsEmbedding, NewsMorphTagger

is_skip_downloading = True

files_folder = "pages/"
index_file_name = "index.txt"

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

pos_set = {''}
pos_dict = {'SYM': [], 'PRON': [], 'SCONJ': [], 'INTJ': [], 'ADJ': [], 'NOUN': [], 'AUX': [], 'PROPN': [],
                'PART': [], 'CCONJ': [], 'X': [], 'ADV': [], 'VERB': [], 'ADP': [], 'NUM': [], 'PUNCT': [], 'DET': []}

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
    print(text)

    segmenter = Segmenter()
    emb = NewsEmbedding()
    morph_tagger = NewsMorphTagger(emb)

    doc = Doc(text)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)

    for t in doc.tokens:
        pos_set.add(t.pos)
        pos_dict[t.pos].append(t.text)

print(pos_set)
print(pos_dict)

# https://melaniewalsh.github.io/Intro-Cultural-Analytics/05-Text-Analysis/13-POS-Keywords.html
# SYM - symbol - символ
# PRON - pronoun - местоимение
# SCONJ - subordinating conjunction - подчинительный союз
# INTJ - interjection - междометие
# ADJ - adjective - прилагательное
# NOUN - noun - существительное
# AUX - auxiliary - вспомогательный
# PROPN - proper noun - имя собственное
# PART - particle - частица
# CCONJ - coordinating conjunction - координирующее соединение
# X - other - другой
# ADV - adverb - наречие
# VERB - verb - глагол
# ADP - adposition - сближение
# NUM - numeral - цифра
# PUNCT - punctuation - пунктуация
# DET - determiner - определитель
