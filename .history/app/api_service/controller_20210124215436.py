from flask import Blueprint, flash, render_template, request, session, abort, redirect, url_for
import requests
import os
from app import app
from app.api_service.nlp_processing import *

api_service = Blueprint('apis', __name__, url_prefix='/apis/')

@api_service.route("/")
def hello():
    
    return render_template('pages/api.html')

