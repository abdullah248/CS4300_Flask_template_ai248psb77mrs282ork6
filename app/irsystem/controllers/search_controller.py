from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

project_name = "Civic Duty"
net_id = "Abdullah Islam: ai248, Prathamesh Bang: psb77, Milan Shah: mrs282, Ohad Koronyo: ork6 "

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	arr = [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
	count = 0
	basestr = "select"
	baserange = "range"
	select = request.args.get(basestr+str(count))
	range = request.args.get(baserange +str(count))
	blah = request.args.get("askdfjaksdfjas;df")
	while select!=None and range!=None:
		arr[int(select)] = int(range)
		count = count +1
		select = request.args.get(basestr+str(count))
		range = request.args.get(baserange +str(count))

	if blah==None:
		blah1 = str("worked")
	# while(select)
	q = request.args

	if not query:
		data = []
		output_message = ''
	else:
		view = {"Abortion":1,"Taxes":0}
		data = [{"idx":1,"pic":"https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Donald_Trump_official_portrait.jpg/440px-Donald_Trump_official_portrait.jpg","name":"Donald Trump","party":"Republican","views":{"text_match":"blah blah blaaah","views":{"Abortion":"Strongly Opposes", "Taxes": "Opposes"}, "wikipedia" : "https://www.wikipedia.org/", "ontheissues":"http://www.ontheissues.org/default.htm"}},
				{"idx":2,"pic":"https://upload.wikimedia.org/wikipedia/commons/thumb/2/27/Hillary_Clinton_official_Secretary_of_State_portrait_crop.jpg/440px-Hillary_Clinton_official_Secretary_of_State_portrait_crop.jpg","name":"Hillary Clinton","party":"Democrat","views":{"text_match":"blah blah bleeah","views":{"Abortion":"Favors", "Taxes": "Strongly Favors"}, "wikipedia" : "https://www.wikipedia.org/", "ontheissues":"http://www.ontheissues.org/default.htm"}}]
		output_message = "Your search: "  + str(arr)
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)
