import os, json

json_path = 'Candidate_JSONs/'

json_files = [json_file for json_file in os.listdir(json_path)]

candidate_to_vector = {}

for json_file in json_files:
    with open(os.path.join(json_path, json_file), encoding='utf-8-sig') as js:
        json_loaded = json.load(js)
        # print(json_loaded)
        vector = []
        for i in range(1, 21):
            for key in json_loaded[i]:
                s = json_loaded[i][key].split('\n')
                str = s[0]

                if str == 'Strongly Opposes':
                    vector.append(0)
                elif str == 'Opposes':
                    vector.append(1)
                elif str == 'No opinion on':
                    vector.append(2)
                elif str == 'Favors':
                    vector.append(3)
                else:
                    vector.append(4)


        candidate_to_vector[json_file.split('.')[0]] = vector

print(candidate_to_vector)
