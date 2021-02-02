from flask import jsonify, Blueprint, flash, render_template, request, session, abort, redirect, url_for
from flask.views import MethodView
import requests
import os
from app import db
from app.models import Champion, Conversation
from app import app
import json
from app.api_service.nlp_processing import *

api_service = Blueprint('apis', __name__, url_prefix='/apis/')

id = 0
def load_data():
    global id
    id += 1
    with open('app/api_service/my_upload/9intents.json') as json_file:
        data = json.load(json_file) 
        keys = list(data.keys())
        values = list(data.values())
        for i in range(len(keys)):
            name = str(keys[i])
            build_item = str(values[i]['build_item'])
            support_socket = str(name + ".png")
            counter = str(values[i]['counter'])
            be_countered = str(values[i]['be_countered'])
            skill_up = str(values[i]['skill_up'])
            how_to_play = str(values[i]['how_to_play'])
            combo = str(values[i]['combo'])
            combine_with = str(values[i]['combine_with'])
            how_to_use_skill = str(values[i]['how_to_use_skill'])
            introduce = str(values[i]['introduce'])
            champion = Champion(name=name, build_item=build_item, support_socket=support_socket, counter=counter, be_countered=be_countered, skill_up=skill_up, how_to_play=how_to_play, combo=combo, combine_with=combine_with, how_to_use_skill=how_to_use_skill, introduce=introduce)
            db.session.add(champion)
            db.session.commit()
            print(champion)



@api_service.route("/")
def hello():
    # load_data()
    return render_template('pages/api.html')

class ChampionView(MethodView):
    def get(self, id=None):
        if not id:
            champions = Champion.query.all()
            print(champions)
            res = {}
            for champion in champions:
                res[champion.id] = {
                    'name': champion.name,
                }
        else:
            champion = Champion.query.filter_by(id=id).first()
            print(champion)
            if not champion:
                abort(404)
            res = {
                'name': champion.name,
            }
        return jsonify(res)    
champion_view = ChampionView.as_view('champion_view')
app.add_url_rule('/champions/', view_func=champion_view, methods=['GET'])
app.add_url_rule('/champions/<int:id>', view_func=champion_view, methods=['GET','PUT'])

model = load_model()

class ConversationView(MethodView):
    
    def get(self):
        conversation_id = 0
        res = dict()
        conversations = Conversation.query.all()
        for conversation in conversations:
            conversation_id = max(conversation_id, conversation.conversation_id)
        c = Conversation(conversation_id=conversation_id+1)
        db.session.add(c)
        db.session.commit()
        return "Successfully created new conversation !"

    def post(self):
        conversation_id = request.json.get('conversation_id')
        message_question = request.json.get('message_question') 
        intent, prob, hero, skill = process_data(model, message_question)
        
        ans = dict()
        entities = dict()
        ans['intent'] = str(intent)
        ans['prob'] = str(prob)
        if hero != "":
            ans['hero'] = str(hero)
            entities['hero']
        if skill != "":
            ans['skill'] = str(skill)
        

        dict_response = getDictPostResponse(conversation_id, message_question, entities, prob, intent)

        # res = dict()
        # res['conversation_id'] = conversation_id
        # res['message_question'] = message_question
        
        # json_string = json.dumps(dict_response,ensure_ascii = False)
        # conversation = Conversation(conversation_id=conversation_id, message_question=message_question, message_answer=dict_response['message_answer'],
        #                 intent=dict_response['intent'], action=dict_response['action'], entities=entities)

        return jsonify(ans)

conversation_view = ConversationView.as_view('conversation_view')
app.add_url_rule('/apis/init/', view_func=conversation_view, methods=['GET'])
app.add_url_rule('/apis/conversation/', view_func=conversation_view, methods=['GET','POST'])