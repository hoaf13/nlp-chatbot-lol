from flask import jsonify, Blueprint, flash, render_template, request, session, abort, redirect, url_for
from flask.views import MethodView
import requests
import os
from app.models import Champion, Conversation
from app import app
import json
api_service = Blueprint('apis', __name__, url_prefix='/apis/')

def load_data(self):
        with open('my_upload/9intents.json') as json_file:
            data = json.load(json_file) 
            

@api_service.route("/")
def hello():
    print(load_data)
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

