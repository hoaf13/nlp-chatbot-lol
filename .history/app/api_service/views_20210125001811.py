from flask import jsonify, Blueprint, flash, render_template, request, session, abort, redirect, url_for
from flask.views import MethodView
import requests
import os
from app import db
from app.models import Champion, Conversation
from app import app
import json
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

