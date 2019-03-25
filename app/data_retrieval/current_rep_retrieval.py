import requests
import pandas as pd
import json


key = 'Insert Key'
url = "https://www.googleapis.com/civicinfo/v2/representatives?address="

df = pd.read_csv('zipcode_list.csv')
zipcodes = df.Zipcode
reps = {}
names = []
states = []
parties = []
twitter_handles = []
facebook_usernames = []
websites = []

for index, row in df.iterrows():
	request = url + str(row['Zipcode']) + "&key=" + str(key)
	r = requests.get(request)
	j = r.json()
	if 'officials' in j:
		state = row['State']
		officials = j['officials']
		for official in officials:
			if 'name' in official:
				name = official['name']
				party = ''
				social_media = []
				twitter_handle = ''
				facebook_name = ''
				weburl = ''
				if 'party' in official:
					party = official['party']
				if 'channels' in official:
					social_media = official['channels']
				for sm in social_media:
					if sm['type'] == 'Facebook':
						facebook_name = sm['id']
					if sm['type'] == 'Twitter':
						twitter_handle = sm['id']
				if 'urls' in official:
					weburl = official['urls'][0]
				if not (name in reps):
					reps[name] = {'party':party,'social_media':social_media}
					names.append(name)
					parties.append(party)
					twitter_handles.append(twitter_handle)
					facebook_usernames.append(facebook_name)
					websites.append(weburl)
					states.append(state)
		with open('data/reps_by_zipcode/'+str(row['Zipcode'])+'.txt', 'w') as outfile:  
			json.dump(r.json(), outfile)
		print('wrote zipcode ' + str(row['Zipcode']) + ' to file')

d = {'Name':names, 'State_Found':states, 'Party':parties, 'Twitter':twitter_handles, 'Facebook':facebook_usernames,'Website':websites}
df = pd.DataFrame(data=d)
df = df[['Name','State_Found', 'Party', 'Twitter', 'Facebook', 'Website']]
df = df.sort_values(by=['Name'])
df.to_csv(path_or_buf='data/rep_summary.csv', index=False)

