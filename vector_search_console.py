lemmas_tfidf_files_folder = "lemmas/"

lemmas_tfidf = []

for i in range(0, 100):
    with open(lemmas_tfidf_files_folder + str(i) + ".txt", 'r', encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            arr = line.split(' ')
            lemmas_tfidf.append({arr[0]: (int(arr[1]), int(arr[2]))})
# взять вектор запроса
# цикл 0-100
#    косинусное сходство со страницей
#    результат записать в массив с номером i
# убрать 0-вые результаты и отсортировать
# вывести url страниц
