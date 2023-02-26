from natasha import Doc, Segmenter, MorphVocab, NewsEmbedding, NewsMorphTagger

segmenter = Segmenter()
morph_vocab = MorphVocab()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)

inverted_indexes_file = "inverted_indexes.txt"

indexes = {}
with open(inverted_indexes_file, 'r', encoding="utf-8") as f:
    lines = f.readlines()
    for line in lines:
        arr = line.split(' ')
        indexes[arr[0]] = [int(k) for k in arr[1:]]

search_request = input().split(' ')

if search_request[0] in indexes.keys() and search_request[2] in indexes.keys():
    if search_request[1].lower() == 'not':
        arr = [value for value in indexes[search_request[0]] if value not in indexes[search_request[2]]]
        print(set(arr))
    if search_request[1].lower() == 'and':
        arr = [value for value in indexes[search_request[0]] if value in indexes[search_request[2]]]
        print(set(arr))
    if search_request[1].lower() == 'or':
        arr = indexes[search_request[0]] + indexes[search_request[2]]
        print(set(arr))

# () > not > and > or

# search_request = input().replace("(", " ( ").replace(")", " ) ").split(' ')
# search_request = list(filter(None, search_request))
# brackets_count = 0
# for e in search_request:
#     if e == '(':
#         brackets_count += 1
#     if e == ')':
#         brackets_count -= 1
# if brackets_count > 0:
#     search_request = search_request + [')'] * brackets_count
# if brackets_count < 0:
#     search_request = ['('] * -brackets_count + search_request


# search_values = []
#
# doc = Doc(search_request)
# doc.segment(segmenter)
# doc.tag_morph(morph_tagger)
# for token in doc.tokens:
#     token.lemmatize(morph_vocab)
#     search_values.append(token.lemma.lower())
#
# for value in search_values:
#     if value in indexes.keys():
#         print(indexes[value])
#     else:
#         print("Can't find pages with word", value)
