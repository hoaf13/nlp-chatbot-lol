from flask import jsonify, Blueprint, flash, render_template, request, session, abort, redirect, url_for
from flask.views import MethodView
import requests
import os
from app.api_service.nlp_processing import *
from werkzeug.utils import secure_filename
from app.models import Conversation, Champion
from app import app

api_service = Blueprint('apis', __name__, url_prefix='/apis/')

@api_service.route("/")
def hello():
    return render_template('pages/api.html')
