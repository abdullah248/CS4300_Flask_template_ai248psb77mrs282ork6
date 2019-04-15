from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords
import os, json, operator
import numpy as np
import random
import math
from collections import defaultdict
from candidateinfo import *
from summaryDictCreate import *
nltk.download('stopwords')

def getInput(input, train_string):

    json_path = 'Candidate_JSONs/'

    json_files = [json_file for json_file in os.listdir(json_path)]

    candidate_to_vector = {}
    viewDict = {}

    for json_file in json_files:
        with open(os.path.join(json_path, json_file), encoding='utf-8-sig') as js:
            json_loaded = json.load(js)
            vector = []
            candViewDict ={}
            for i in range(1, 21):
                for key in json_loaded[i]:
                    s = json_loaded[i][key].split('\n')
                    stri = s[0]
                    issue = s[1].split(':')[1]
                    candViewDict[issue] = stri

                    if stri == 'Strongly Opposes':
                        vector.append(1)
                    elif stri == 'Opposes':
                        vector.append(2)
                    elif stri == 'No opinion on':
                        vector.append(3)
                    elif stri == 'Favors':
                        vector.append(4)
                    else:
                        vector.append(5)

            viewDict[json_file.split('.')[0]] = candViewDict
            candidate_to_vector[json_file.split('.')[0]] = vector


    print(candidate_to_vector)
    print(viewDict)

    #input = []
    numberIssues = 20

    #for i in range(numberIssues):
    #    input.append(random.randint(1,5))
    #input = np.array(input)
    print("\nInput is "+str(input))

    data = candidate_to_vector
    #print(data)
    tupleList = []
    for k in data: #k is name of candidate
        data[k] = np.array(data[k])
        temp = np.copy(input)
        for i in range(len(temp)):
            if temp[i] == 0:
                temp[i] = data[k][i]
        #print("Temp is now:")
        #print(temp)
        v = temp-data[k]
        #print(v)
        sum = math.sqrt(np.sum(np.square(v))) #Difference between vectors calculation
        #print(sum)
        tupleList.append((k,sum))

    sorted_list = sorted(tupleList, key=lambda x: x[1])
    #print(sorted_list)
    squaredDistanceList = []

    for tup in sorted_list:
        n = math.sqrt(16*numberIssues)
        accuracy = 100 - (abs(tup[1])/n)*100
        #print(tup[0].replace('_', ' ') + " with similarity of " + str(round(accuracy,2)) + "%")
        squaredDistanceList.append((tup[0], round(accuracy,2)))
    print(squaredDistanceList)


    stopWords = stopwords.words('english')

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

    createOutput(squaredDistanceList,sorted_x,data,viewDict)



def createOutput(firstMetricList,SecondMetricList,data,viewDict):
    outputList = []
    combinedTupleList = []

    for i in range(len(firstMetricList)):
        combinedTupleList.append((firstMetricList[i][0],firstMetricList[i][1]))
    print("\nCombined tuple list is: ")
    print(combinedTupleList)


    for i in range(len(combinedTupleList)):
        cand = bigDict[combinedTupleList[i][0]]
        candSummary = candidate_to_summary[combinedTupleList[i][0]]
        outputList.append({'idx':i,'pic':cand['pic'],'name':cand['name'],
        'party':cand['party'],'Views':{'wikipedia':cand['wikipedia'],'ontheissues':cand['ontheissues'],
        'views':viewDict[combinedTupleList[i][0]],'summary':candSummary}})

    print()
    print()
    print()
    print(outputList)
    return outputList

getInput([5, 2, 5, 2, 5, 1, 5, 1, 1, 2, 2, 5, 2, 1, 1, 5, 5, 5, 1, 0],"I love donald trump")
