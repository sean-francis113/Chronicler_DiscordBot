from flask import Flask
from threading import Thread
#from os import system

app = Flask('')

@app.route('/')
def home():
    return "The Chronicler is currently running.\n\nThere are no plans for maintenance at this time."

def run():
	app.run(host='0.0.0.0',port=8080)
	#Saved In Case 'Address Already In Use' Error Reappears
	#system("pkill -9 python")

def keep_alive():  
    t = Thread(target=run)
    t.start()