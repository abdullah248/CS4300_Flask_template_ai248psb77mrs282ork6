import os

candidate_to_summary = {}
for file in os.listdir('app/data_retrieval/summaries/'):
    with open(os.path.join('app/data_retrieval/summaries/', file)) as txtfile:
        summary = txtfile.read()
        candidate_to_summary[file.split('.')[0]] = summary

#print(candidate_to_summary)
