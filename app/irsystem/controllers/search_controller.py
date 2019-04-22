from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.data_retrieval.inputoutput import getInput

project_name = "Civic Duty"
net_id = "Abdullah Islam: ai248, Prathamesh Bang: psb77, Milan Shah: mrs282, Ohad Koronyo: ork6 "

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	arr = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	positions = ["Abortion is a woman's unrestricted right",
				 "Legally require hiring women & minorities",
				 "Comfortable with same-sex marriage",
				 "Keep God in the public sphere",
				 "Expand ObamaCare",
				 "Privatize Social Security",
				 "Vouchers for school choice",
				 "Fight EPA regulatory over-reach",
				 "Stricter punishment reduces crime",
				 "Absolute right to gun ownership",
				 "Higher taxes on the wealthy",
				 "Pathway to citizenship for illegal aliens",
				 "Support & expand free trade",
				 "Support American Exceptionalism",
				 "Expand the military",
				 "Make voter registration easier",
				 "Avoid foreign entanglements",
				 "Prioritize green energy",
				 "Marijuana is a gateway drug",
				 "Stimulus better than market-led recovery"]
	idxStance = ["Strongly Opposes", "Opposes", "Neutral", "Favors", "Strongly Favors"]
	count = 0
	basestr = "select"
	baserange = "range"
	select = request.args.get(basestr+str(count))
	ranger = request.args.get(baserange +str(count))
	noneChanged = True
	while select!=None and ranger!=None:
		arr[int(select)] = int(ranger)
		count = count +1
		select = request.args.get(basestr+str(count))
		ranger = request.args.get(baserange +str(count))
		noneChange=False
	# while(select)
	q = request.args


	if not query and count==0 and noneChanged:
		data = []
		output_message = ''
		stances = []
		stanceP = []
	else:
		if not query:
			query=''
		data = getInput(arr,query)
		stances = []
		stanceP = []
		for i in range(20):
			if (arr[i] != 0):
				stances.append(positions[i])
				stanceP.append((idxStance[arr[i]-1], positions[i]))
	return render_template('search.html', name=project_name, netid=net_id, query=query, stances=stances, stanceP=stanceP, data=data)
