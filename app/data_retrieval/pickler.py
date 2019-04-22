from candidateinfo import *
from TwitterSentiment import *
import pickle, os

cand_sentiments = {}
for underscore, candDict in bigDict.items():
    pos, neg, neu = runTwitterAnalysis(candDict['name'])
    cand_sentiments[underscore] = (pos, neg, neu)

with open('candidates.pickle', 'wb') as f:
    pickle.dump(cand_sentiments, f)
