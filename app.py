from flask import Flask, abort
import requests
import json 
import os

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, this is a Proxy Flask Api Gateway!"
    
@app.route("/events")
def events():
	
	data = []
	try:
		
		# basic way to get the env data for the facebook api
		# with open('env.json') as data_file:    
		#	data = json.load(data_file)
	
		# pageid = data['pageid']
		# accesstoken = data['accesstoken']
		
		# should get the environmental value from the heroku
		pageid = os.environ.get('pageid')
		accesstoken = os.environ.get('accesstoken') 
		
		r = requests.get(url='https://graph.facebook.com/v2.8/%s/events?access_token=%s' % (pageid,accesstoken))    
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

if __name__ == "__main__":
    app.run(use_reloader=True)
