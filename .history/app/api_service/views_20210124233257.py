from flask import jsonify, Blueprint, flash, render_template, request, session, abort, redirect, url_for
from flask.views import MethodView
import requests
import os
import 

api_service = Blueprint('apis', __name__, url_prefix='/apis/')

@api_service.route("/")
def hello():
    return render_template('pages/api.html')



