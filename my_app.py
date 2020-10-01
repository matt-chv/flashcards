"""
v0.1: shows cards, talks back, checks answers
v0.2: talks back to cars back-end
"""

#import standard modules
import logging
from os.path import exists, join
from urllib.parse import unquote

#import pip modules

from flask import Flask, json, request, Response, send_from_directory

#import own
from FlashCards import load_deck
from db import view_users_activities_log

app_data_folder = "/var/www/DrillMaster/DrillMaster/"

root_logger= logging.getLogger()
root_logger.setLevel(logging.DEBUG)
#note important to keep encoding utf-8 to log request with cards
#content in utf-8 format
handler = logging.FileHandler(join(app_data_folder,"debug.log"), encoding='utf-8')
formatter = logging.Formatter('%(name)s %(message)s')
handler.setFormatter(formatter) # Pass handler as a parameter, not assign
root_logger.addHandler(handler)


students = [{"id":0, "name": "demo", "deck":"demo.json"},
            {"id": '4', "name": "elodie","deck":"Elodie.json"},
           {"id": 5, "name": "camille", "deck":"Camille.json"}]

api = Flask(__name__,static_url_path='/static')

api.config["APPLICATION_ROOT"] = "/drillmaster"


@api.route('/students', methods=['GET'])
def get_students():
  return json.dumps(students)

@api.route("/deck", methods=['GET','POST'])
def get_deck():
  user_id = request.args.get('id')
  deck = None
  root_logger.debug("hello")
  for user in students:
    if user["id"]==user_id:
      deck=user["deck"]
  if deck is None:
    deck="demo.json"
    user_id="0"
  
  
  root_logger.info("request method: %s",request.method)
  root_logger.info("request json : %s",request.json)
  res =load_deck(deck,None,app_data_folder)
  
  #res =load_deck("Elodie.json",None,"/var/www/FlaskApp/FlaskApp/")
  if request.method == 'GET':
    if not res.shuffled:
      res.shuffle_cards()
    qs = res.shuffled
    deck = {}
    for q in qs:
      deck[q]=res.json[q]
  elif request.method == 'POST':
    myjson = request.json
    logging.debug("received json: %s",json.dumps(myjson))
    for card in myjson:
      for key in card:
        logging.debug("debug received card: %s",card[key])
      res.update_card(card["question"],float(card["timer"]),card["answer"],card["number_attempts"], card["timestamp"])
      res.save_hdd()
    qs = []
    for i in range(10):
      qs.append(res.next_q())
    deck = {}
    for q in qs:
      logging.debug("POST - adding q: %s",q)
      deck[q]=res.json[q] 
  #logging.debug("submitted deck: %s",json.dumps(deck))
  return json.dumps(deck)

@api.route('/educator')
def educator():
  df = view_users_activities_log()
  return df.to_html()

@api.route('/student')
def student():
  args = request.args
  id = args['id']
  for s in students:
    if s["id"]==id:
      name = s["name"]
    return api.send_static_file('cards.html')

@api.route('/favicon.ico')
def favicon():
	return api.send_static_file("favicon.ico")

@api.route("/drillmaster/")
@api.route('/')
@api.route('/index')
def index():
    return api.send_static_file('index.html')
    #return index_html

@api.route('/<path:filename>')
def manifest(filename):
  if filename=="manifest.json":
    root_logger.info("returning manifest.json")
    if exists(join("/var/www/DrillMaster/DrillMaster","manifest.json")):
      root_logger.info("manifest exists")
    else:
      root_logger.info("manifest does not exists")
    return send_from_directory("/var/www/DrillMaster/DrillMaster","manifest.json")
  elif filename=="sw.js":
    return send_from_directory("/var/www/DrillMaster/DrillMaster","sw.js")

if __name__ == '__main__':
  logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
  root_logger.setLevel(logging.DEBUG)
  consoleHandler = logging.StreamHandler()
  consoleHandler.setFormatter(logFormatter)
  root_logger.addHandler(consoleHandler) 
  api.run(debug=True, port=5005)
