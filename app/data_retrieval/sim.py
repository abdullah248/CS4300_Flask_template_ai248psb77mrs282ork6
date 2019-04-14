from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords
import os, json

nltk.download('stopwords')

json_path = 'Txt_Files/'

json_files = [json_file for json_file in os.listdir(json_path)]
#print(json_files)

stopWords = stopwords.words('english')

print ("\nCalculating document similarity scores...")

dataset = []
for name in json_files:
    file_nam = '/Users/ohadkoronyo/Desktop/justjson/Txt_Files/' + name
    f = open(file_nam)
    docer = str(f.read())
    dataset.append(docer)

train_string = 'pence'

train_set = [train_string] + dataset

tfidf_vectorizer = TfidfVectorizer(stop_words=stopWords)
tfidf_matrix_train = tfidf_vectorizer.fit_transform(train_set)

print("\nInput string is "+train_string)
print("")
mat = cosine_similarity(tfidf_matrix_train[0:1], tfidf_matrix_train)
print ("\nSimilarity Scores:", mat)

tupleList = []
for i in range(len(json_files)):
    #print(str(json_files[i][:-4]) + ": " + str(mat[0][i+1]))
    tupleList.append((json_files[i][:-4],mat[0][i+1]))

sorted_list = sorted(tupleList, key=lambda x: x[1], reverse = True)
for tup in sorted_list:
    print(tup[0] + " with similarity of " + str(tup[1]))
