from natasha import Doc, Segmenter, MorphVocab, NewsEmbedding, NewsMorphTagger

from numpy import dot
from numpy.linalg import norm

segmenter = Segmenter()
morph_vocab = MorphVocab()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)

# input text (moved to top for no waiting before prepared)
search_request = input().split(' ')
search_request = list(filter(None, search_request))

lemmas_tfidf_files_folder = "lemmas/"

lemmas_tfidf = []

for i in range(0, 100):
    with open(lemmas_tfidf_files_folder + str(i) + ".txt", 'r', encoding="utf-8") as f:
        lemmas_tfidf.append({})
        lines = f.readlines()
        for line in lines:
            arr = line.split(' ')
            lemmas_tfidf[i][arr[0]] = [float(arr[1]), float(arr[2])]

# reset input words by lemmas
unique_lemmas = {}
total_lemmas = 0
for i in range(0, len(search_request)):
    doc = Doc(search_request[i])
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    doc.tokens[0].lemmatize(morph_vocab)
    lemma = doc.tokens[0].lemma.lower()
    search_request[i] = lemma
    if lemma not in unique_lemmas.keys():
        unique_lemmas[lemma] = 0
    unique_lemmas[lemma] += 1
    total_lemmas += 1

# get tf-idf for input
search_request_tf = {}
for key in unique_lemmas.keys():
    search_request_tf[key] = unique_lemmas[key] / total_lemmas

# vector search
results = {}
for i in range(0, 100):
    cur_file_lemmas = lemmas_tfidf[i]
    list1 = []
    list2 = []
    for key in cur_file_lemmas.keys():
        list1.append(cur_file_lemmas[key][0])
        list2.append(search_request_tf[key] if key in search_request_tf.keys() else 0.0)
    if norm(list2) == 0:
        continue
    result = dot(list1, list2) / (norm(list1) * norm(list2))
    if result == 0:
        continue
    results[i] = result

print(results)
sorted_pages_indexes = sorted(results, reverse=True)
print(sorted_pages_indexes)

# взять вектор запроса
# цикл 0-100
#    косинусное сходство со страницей
#    результат записать в массив с номером i
# убрать 0-вые результаты и отсортировать
# вывести url страниц
