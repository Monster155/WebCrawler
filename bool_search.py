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
        pages_arr = line.split(' ')
        indexes[pages_arr[0]] = {int(k) for k in pages_arr[1:]}

""" search """

search_request = input().replace("(", " ( ").replace(")", " ) ").split(' ')
search_request = list(filter(None, search_request))
brackets_count = 0
for e in search_request:
    if e == '(':
        brackets_count += 1
    if e == ')':
        brackets_count -= 1
if brackets_count > 0:
    search_request = search_request + [')'] * brackets_count
if brackets_count < 0:
    search_request = ['('] * -brackets_count + search_request

# () > not > and > or

search_request_final = "("
for i in range(0, len(search_request)):
    x = search_request[i].lower()
    if x == 'and':
        search_request[i] = x
        search_request_final += ").intersection("
    elif x == 'or':
        search_request[i] = x
        search_request_final += ").union("
    elif x == 'not':
        search_request[i] = x
        search_request_final += ").difference("
    elif x == '(':
        search_request[i] = x
        search_request_final += "("
    elif x == ')':
        search_request[i] = x
        search_request_final += ")"
    else:
        doc = Doc(x)
        doc.segment(segmenter)
        doc.tag_morph(morph_tagger)
        doc.tokens[0].lemmatize(morph_vocab)
        lemma = doc.tokens[0].lemma.lower()
        search_request[i] = lemma
        if lemma in indexes.keys():
            search_request_final += str(indexes[lemma])
        else:
            search_request_final += "set()"  # "{range(0, 100)}"
search_request_final += ")"

# print(search_request)
# print(search_request_final)
search_request_result = eval(search_request_final)

if len(search_request_result) == 0:
    print("Pages not found")
else:
    print(search_request_result)

# pages_arr = []
# if search_request[0] in indexes.keys() and search_request[2] in indexes.keys():
#     if search_request[1].lower() == 'not':
#         pages_arr = [value for value in indexes[search_request[0]] if value not in indexes[search_request[2]]]
#     if search_request[1].lower() == 'and':
#         pages_arr = [value for value in indexes[search_request[0]] if value in indexes[search_request[2]]]
#     if search_request[1].lower() == 'or':
#         pages_arr = indexes[search_request[0]] + indexes[search_request[2]]
# else:
#     if search_request[0] not in indexes.keys() and search_request[1].lower() == 'not':
#         pages_arr = []
#     else:
#         if search_request[0] in indexes.keys():
#             print("Pages only for \"" + search_request[0] + "\"")
#             pages_arr = indexes[search_request[0]]
#         elif search_request[2] in indexes.keys():
#             print("Pages only for \"" + search_request[2] + "\"")
#             pages_arr = indexes[search_request[2]]
#         else:
#             pages_arr = []
#
# if len(pages_arr) == 0:
#     print("Pages not found")
# else:
#     print(set(pages_arr))
