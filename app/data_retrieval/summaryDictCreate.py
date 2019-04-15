import os

candidate_to_summary = {}
for file in os.listdir('summaries/'):
    with open(os.path.join('summaries/', file)) as txtfile:
        summary = txtfile.read()
        candidate_to_summary[file.split('.')[0]] = summary

#print(candidate_to_summary)
