from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords
import os, json, operator, editdistance
import numpy as np

nltk.download('stopwords')
# nltk.download('edit_distance')
stopWords = stopwords.words('english')

json_path = 'Txt_Files/'

json_files = [json_file for json_file in os.listdir(json_path)]

il_patho = 'Txt_Files/'

candidate_to_sentence = {}

for il_file in os.listdir(il_patho):
    with open(os.path.join(il_patho, il_file)) as txt:
        candidate_to_sentence[il_file.split('.')[0]] = []
        lines = txt.readlines()
        for line in lines:
            line = line.strip()
            if line != '\n' and len(line) != 0 and line[0] != '=':
                line = line.split('.')
                for l in line:
                    candidate_to_sentence[il_file.split('.')[0]].append(l)

train_string = 'Medicare for all'

train_words = train_string.split(' ')

tfidf_vectorizer = TfidfVectorizer(stop_words=stopWords)

cand_scores = {}

for candidate, sentences in candidate_to_sentence.items():
    train_set = [train_string] + sentences
    tfidf_matrix_train = tfidf_vectorizer.fit_transform(train_set)
    mat = cosine_similarity(tfidf_matrix_train[0], tfidf_matrix_train[1:])
    # eds = []
    # for sentence in sentences:
    #     ed = editdistance.eval(train_string, sentence) + 1
    #     booleansearch = True
    #     count = 0
    #     for word in train_words:
    #         if word not in sentence:
    #             booleansearch = False
    #             break
    #     # if booleansearch:
    #     #     eds.append(10/ed)
    #     # elif count == 0:
    #     #     eds.append(.1/ed)
    #     # else:
    #     #     eds.append(1/ed)
    #     eds.append(1/ed)
    # eds = np.array(eds)
    # # print(eds)
    # mat = mat * eds
    # print(mat.shape)
    cand_scores[candidate] = mat.max()

# print(cand_scores)
sorted_x = sorted(cand_scores.items(), key=lambda x: x[1], reverse=True)

print(sorted_x)
