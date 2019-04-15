import random
import numpy as np
import math

import os, json

json_path = 'Candidate_JSONs/'

json_files = [json_file for json_file in os.listdir(json_path)]

candidate_to_vector = {}

for json_file in json_files:
    with open(os.path.join(json_path, json_file), encoding='utf-8-sig') as js:
        json_loaded = json.load(js)
        vector = []
        for i in range(1, 21):
            for key in json_loaded[i]:
                s = json_loaded[i][key].split('\n')
                stri = s[0]

                if stri == 'Strongly Opposes':
                    vector.append(0)
                elif stri == 'Opposes':
                    vector.append(1)
                elif stri == 'No opinion on':
                    vector.append(2)
                elif stri == 'Favors':
                    vector.append(3)
                else:
                    vector.append(4)


        candidate_to_vector[json_file.split('.')[0]] = vector


print(candidate_to_vector)

input = []
numberIssues = 20

for i in range(numberIssues):
    input.append(random.randint(1,5))
input = np.array(input)
print("\nInput is "+str(input))

data = candidate_to_vector
#print(data)
tupleList = []
for k in data: #k is name of candidate
    data[k] = np.array(data[k])
    v = input-data[k]
    #print(v)
    sum = math.sqrt(np.sum(np.square(v))) #Difference between vectors calculation
    #print(sum)
    tupleList.append((k,sum))

sorted_list = sorted(tupleList, key=lambda x: x[1])
print(sorted_list)

# top5Candidates = []
for tup in sorted_list:
    n = math.sqrt(16*numberIssues)
    #print(n)
    # top5Candidates.append(tup[0])
    accuracy = 100 - (abs(tup[1])/n)*100
    print(tup[0].replace('_', ' ') + " with similarity of " + str(round(accuracy,2)) + "%")


# top5Candidates = []
