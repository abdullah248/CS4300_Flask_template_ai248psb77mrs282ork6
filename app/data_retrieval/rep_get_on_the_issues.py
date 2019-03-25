import requests
import pandas as pd
import json

base_url = 'http://www.ontheissues.org/'

df = pd.read_csv('data/rep_summary.csv')
count =  0
failedNum = 0
failed = []
names = []
files = []


for index, row in df.iterrows():
	name = str(row['Name'])
	print(name)
	space = name.find(' ')
	period = name.find('.',space)
	formatted_name =''
	if period == -1:
		period = space
	formatted_name = name[:space] + "_" + name[period+1:]
	formatted_name= formatted_name.replace(' ', '')
	print(formatted_name)
	request = base_url + formatted_name + ".htm"
	r = requests.get(request)
	if r.status_code ==200:
		count +=1
	else:
		request = base_url + 'house/' + formatted_name + ".htm"
		r = requests.get(request)
		if r.status_code ==200:
			count +=1
		else:
			request = base_url + 'senate/' + formatted_name + ".htm"
			r = requests.get(request)
			if r.status_code ==200:
				count +=1
			else: 
				request = base_url + str(row['State_Found']) + '/' + formatted_name + ".htm"
				r = requests.get(request)
				if r.status_code ==200:
					count +=1
				else:
					failedNum+=1
	if r.status_code==200:
		print("Found Website")
		names.append(name)
		files.append('data/rep_on_the_issues/'+str(formatted_name)+'.html')
		file = open('data/rep_on_the_issues/'+str(formatted_name)+'.html', 'w')
		file.write(r.text)
	else:
		print("Failed to find website")
		names.append(name)
		files.append('')
	print("***********")

d = {'Name':names, 'File':files}
df = pd.DataFrame(data=d)
df = df[['Name','File']]
df = df.sort_values(by=['Name'])
df.to_csv(path_or_buf='data/on_the_issues_summary.csv', index=False)


