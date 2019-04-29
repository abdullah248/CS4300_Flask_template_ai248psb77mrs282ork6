from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
from scipy.sparse.linalg import svds
import nltk
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
import os, json, operator
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import random
import math
from collections import defaultdict
from app.data_retrieval.candidateinfo import *
from app.data_retrieval.summaryDictCreate import *
nltk.download('stopwords')
nltk.download('vader_lexicon')
nltk.download('punkt')

def getInput(input, train_string):
    # print('here')
    ps = PorterStemmer()
    original_query = word_tokenize(train_string)
    for i, w in enumerate(original_query):
        original_query[i] = ps.stem(w)
    original_query =  " ".join(original_query)

    json_path = 'app/data_retrieval/Candidate_JSONs/'

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
                    if stri == 'No opinion on':
                        stri = 'No opinion'
                    if stri == 'Neutral on':
                        stri = 'Neutral'
                    issue = s[1].split(':')[1]
                    candViewDict[issue] = stri

                    if stri == 'Strongly Opposes':
                        vector.append(1)
                    elif stri == 'Opposes':
                        vector.append(2)
                    elif stri == 'No opinion' or stri == 'Neutral':
                        vector.append(3)
                    elif stri == 'Favors':
                        vector.append(4)
                    else:
                        vector.append(5)

            viewDict[json_file.split('.')[0]] = candViewDict
            candidate_to_vector[json_file.split('.')[0]] = vector


    # print(candidate_to_vector)
    # print(viewDict)

    #input = []
    numberIssues = 20

    #for i in range(numberIssues):
    #    input.append(random.randint(1,5))
    #input = np.array(input)
    # print("\nInput is "+str(input))

    data = candidate_to_vector
    #print(data)
    tupleList = []
    for k in data: #k is name of candidate
        data[k] = np.array(data[k])
        temp = np.copy(input)
        numPositions = 0
        diff = 0
        for i in range(len(temp)):
            if temp[i] != 0:
                numPositions += 1
                diff += abs(temp[i] - data[k][i])
            # if temp[i] == 0:
            #     temp[i] = data[k][i]
        #print("Temp is now:")
        #print(temp)
        # v = temp-data[k]
        #print(v)
        # sum = math.sqrt(np.sum(np.square(v))) #Difference between vectors calculation
        sum = 1 - diff/(4*numPositions)
        #print(sum)
        tupleList.append((k,sum))

    sorted_list = sorted(tupleList, key=lambda x: x[1])
    #print(sorted_list)
    squaredDistanceList = []

    for tup in sorted_list:
        # n = math.sqrt(16*numberIssues)
        # accuracy = 100 - (abs(tup[1])/n)*100
        accuracy = 100*tup[1]
        #print(tup[0].replace('_', ' ') + " with similarity of " + str(round(accuracy,2)) + "%")
        squaredDistanceList.append((tup[0], round(accuracy,2)))
    # print(squaredDistanceList)


    stopWords = stopwords.words('english')

    il_patho = 'app/data_retrieval/Txt_Files/'

    candidate_to_sentence = {}

    for il_file in os.listdir(il_patho):
        with open(os.path.join(il_patho, il_file)) as txt:
            candidate_to_sentence[il_file.split('.')[0]] = []
            lines = txt.readlines()
            for line in lines:
                line = line.strip()
                if line != '\n' and len(line) != 0 and line[0] != '=':
                    sents = sent_tokenize(line)
                    for sent in sents:
                        the_words = word_tokenize(sent)
                        for y, w in enumerate(the_words):
                            the_words[y] = ps.stem(w)
                        sent = " ".join(the_words)
                        candidate_to_sentence[il_file.split('.')[0]].append(sent)

    train_words = word_tokenize(original_query)

    all_sentences = []
    for sentences in candidate_to_sentence.values():
        all_sentences += sentences

    tfidf_vectorizer = TfidfVectorizer(stop_words=stopWords, min_df=0.001, max_df=0.5)
    my_matrix = tfidf_vectorizer.fit_transform(all_sentences).transpose()
    words_compressed, s, v_trans = svds(my_matrix, 25)
    docs_compressed = v_trans.transpose()

    word_to_index = tfidf_vectorizer.vocabulary_
    index_to_word = {i:t for t,i in word_to_index.items()}

    words_compressed = normalize(words_compressed, axis = 1)

    cand_scores = {}

    train_string = original_query

    for strin in train_words:
        if strin in word_to_index:
            sims = words_compressed.dot(words_compressed[word_to_index[strin],:])
            asort = np.argsort(-sims)[:2+1]
            final_arr = [(index_to_word[i],sims[i]/sims[asort[0]]) for i in asort[1:]]
            for word, val in final_arr:
                train_string = train_string + ' ' + word

    # print(train_string)


    sia = SentimentIntensityAnalyzer()

    query_sentiment = sia.polarity_scores(original_query)['compound']
    # print(query_sentiment)
    for candidate, sentences in candidate_to_sentence.items():
        # for x, sentence in enumerate(sentences):
        #     the_words = word_tokenize(sentence)
        #     for y, w in enumerate(the_words):
        #         the_words[y] = ps.stem(w)
        #     the_words = " ".join(the_words)
        #     sentences[x] = the_words

        train_set = [original_query] + sentences
        tfidf_matrix_train = tfidf_vectorizer.fit_transform(train_set)
        mat = cosine_similarity(tfidf_matrix_train[0], tfidf_matrix_train[1:])
        # print(mat.shape)
        # i = 0
        # for sentence in sentences:
        #     s1 = sia.polarity_scores(sentence)['compound']
        #     # diff = abs(query_sentiment - s1)
        #     # mat[0][i] = mat[0][i] - diff
        #     i += 1



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
        diff = abs(query_sentiment - sia.polarity_scores(sentences[mat[0].argmax()])['compound'])
        cand_scores[candidate] = mat.max() - diff
        # print (candidate, sia.polarity_scores(sentences[mat[0].argmax()])['compound'])

    # print(cand_scores)
    sorted_x = sorted(cand_scores.items(), key=lambda x: x[1], reverse=True)
    # print(sorted_x)

    return createOutput(squaredDistanceList,sorted_x,viewDict,train_string)



def createOutput(firstMetricList,secondMetricList,viewDict,inputString):
    outputList = []
    combinedTupleList = []
    cand_scores = {}
    # print('here')
    for i in range(len(firstMetricList)):
        # combinedTupleList.append((firstMetricList[i][0],firstMetricList[i][1]))
        if inputString != "":
            cand_scores[firstMetricList[i][0]] = max(0, firstMetricList[i][1] - 15)
        else:
            cand_scores[firstMetricList[i][0]] = firstMetricList[i][1]
    if inputString != "":
        k = 15
        for j in range(3):
            cand_scores[secondMetricList[j][0]] = max(0, min(100, k + cand_scores[secondMetricList[j][0]]))
            k -= 5

    sorted_x = sorted(cand_scores.items(), key=lambda x: x[1], reverse=True)
    # print("\nCombined tuple list is: ")
    # print(combinedTupleList)

    with open('app/data_retrieval/candidates.pickle', 'rb') as f:
        cand_sents = pickle.load(f)

    firstMetricList = dict((x, y) for x, y in firstMetricList)
    secondMetricList = dict((x, y) for x, y in secondMetricList)
    for i in range(len(sorted_x)):
        cand = bigDict[sorted_x[i][0]]
        candSummary = candidate_to_summary[sorted_x[i][0]]
        outputList.append({'idx':i,'pic':cand['pic'],'name':cand['name'],
        'party':cand['party'],'views':{'wikipedia':cand['wikipedia'],'ontheissues':cand['ontheissues'],
        'views':viewDict[sorted_x[i][0]],'summary':candSummary}, 'positive_sentiment':cand_sents[sorted_x[i][0]][0],
        'negative_sentiment':cand_sents[sorted_x[i][0]][1], 'neutral_sentiment':cand_sents[sorted_x[i][0]][2],
        'tweet':cand_sents[sorted_x[i][0]][3], 'similarity':round(cand_scores[sorted_x[i][0]], 1), 'slider':firstMetricList[sorted_x[i][0]], 'wiki':secondMetricList[sorted_x[i][0]]})
        print(cand['name'] + ' ' + str(cand_sents[sorted_x[i][0]][3]))
    #
    # print()
    # print()
    # print()
    # print(outputList)
    return outputList

# getInput([5, 2, 5, 2, 5, 1, 5, 1, 1, 2, 2, 5, 2, 1, 1, 5, 5, 5, 1, 0],"I love donald trump")
