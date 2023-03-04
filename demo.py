import tkinter
import customtkinter

import webbrowser

from natasha import Doc, Segmenter, MorphVocab, NewsEmbedding, NewsMorphTagger

from numpy import dot
from numpy.linalg import norm

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("450x350")


class MyFrame(customtkinter.CTkScrollableFrame):
    labels = []

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

    def add_new(self, links):
        for label in self.labels:
            label.destroy()
        self.labels = []
        for link in links:
            text_var = tkinter.StringVar(value=link)
            label = customtkinter.CTkLabel(self, textvariable=text_var)
            label.grid(row=len(self.labels), column=0, padx=20)
            label.bind("<Button-1>", lambda e: webbrowser.open_new(link))
            self.labels.append(label)


class Searcher:
    index_file_name = "index.txt"
    lemmas_tfidf_files_folder = "lemmas/"

    def __init__(self):
        self.segmenter = Segmenter()
        self.morph_vocab = MorphVocab()
        emb = NewsEmbedding()
        self.morph_tagger = NewsMorphTagger(emb)

        self.lemmas_tfidf = []

        for i in range(0, 100):
            with open(self.lemmas_tfidf_files_folder + str(i) + ".txt", 'r', encoding="utf-8") as f:
                self.lemmas_tfidf.append({})
                lines = f.readlines()
                for line in lines:
                    arr = line.split(' ')
                    self.lemmas_tfidf[i][arr[0]] = [float(arr[1]), float(arr[2])]

        self.index_to_links = {}

        with open(self.index_file_name, 'r', encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                arr = line.split(' ')
                self.index_to_links[int(arr[0])] = arr[1][:-1]

    def search(self, request):

        # input text
        search_request = request.split(' ')
        search_request = list(filter(None, search_request))

        # reset input words by lemmas
        unique_lemmas = {}
        total_lemmas = 0
        for i in range(0, len(search_request)):
            doc = Doc(search_request[i])
            doc.segment(self.segmenter)
            doc.tag_morph(self.morph_tagger)
            doc.tokens[0].lemmatize(self.morph_vocab)
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
            cur_file_lemmas = self.lemmas_tfidf[i]
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

        sorted_pages_indexes = sorted(results, reverse=True)
        return [self.index_to_links[index] for index in sorted_pages_indexes]


searcher = Searcher()


def button_function():
    links = searcher.search(textbox.get("0.0", "end"))
    my_frame.add_new(links)


textbox = customtkinter.CTkTextbox(app)
textbox.place(relx=0.55, y=30, anchor=tkinter.E)
textbox.configure(state="normal", height=30)

button = customtkinter.CTkButton(master=app, text="Search", command=button_function)
button.place(relx=0.55, y=30, anchor=tkinter.W)

my_frame = MyFrame(master=app, width=400, height=260)
my_frame.place(relx=0.5, y=200, anchor=tkinter.CENTER)

app.mainloop()
