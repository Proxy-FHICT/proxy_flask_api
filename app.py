from flask import Flask, abort, send_from_directory
from flask_cors import CORS, cross_origin
import requests
import json 
import os
import random

app = Flask(__name__)
CORS(app)

def geteventdata(limit=25):
	# basic way to get the env data for the facebook api
	# with open('env.json') as data_file:    
	#	data = json.load(data_file)

	# pageid = data['pageid']
	# accesstoken = data['accesstoken']
	
	# should get the environmental value from the heroku
	pageid = os.environ.get('pageid')
	accesstoken = os.environ.get('accesstoken') 
	
	r = requests.get(url='https://graph.facebook.com/v2.8/%s/events?access_token=%s&limit=%s' % (pageid,accesstoken,limit))    
	# returns only data, do not want to show pagination, 
	# workaround can be found (either increasing the limit or wrapping the paginantion links somehow)
	# , but for now we can just display up to 25  
	return r

@app.route("/")
def hello():
    return "Hello, this is a Proxy Flask Api Gateway!"
    
@app.route("/events")
def events():
	try:
		
		r = geteventdata()
		# returns only data, do not want to show pagination, 
		# workaround can be found (either increasing the limit or wrapping the paginantion links somehow)
		# , but for now we can just display up to 25  
		return json.dumps(r.json()['data'],indent=4)
	
	except Exception as inst:
		# console logging
		print(type(inst))
		print(inst.args)
		print(inst)
		
		abort(500)

@app.route("/events/<limit>")
def eventslimit(limit):
	try:
		r = geteventdata(limit)
		return json.dumps(r.json()['data'],indent=4)
	except Exception as inst:
		# console logging
		print(type(inst))
		print(inst.args)
		print(inst)
		abort(500)
		
@app.route("/img/random")		
def imagerandom():
	try:
		files = [];	
		for filename in os.listdir("./img"):
			print(os.path.join(".\\img", filename))
			files.append(filename)
		# randomly select a file	
		path=".\\img\\"
		try:
			path = random.choice(files)
		except:
			path="14352107_887952714668641_7104487585079782535_o.jpg"
		return send_from_directory('./img', path)
		
	except Exception as inst:		
		# console logging
		print(type(inst))
		print(inst.args)
		print(inst)
		abort(500)
		
@app.route("img/welcome")
def imagewelcome():
	try:
		path = "welcome.jpeg"
		return send_from_directory('./img/welcome_bg', path)
		
	except Exception as inst:		
		# console logging
		print(type(inst))
		print(inst.args)
		print(inst)
		abort(500)		
		
if __name__ == "__main__":
    app.run(use_reloader=True)
