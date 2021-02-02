from flask import Blueprint, flash, render_template, request, session, abort, redirect, url_for
import requests
import os
from app import app

api_service = Blueprint('api', __name__, url_prefix='/apis/')


@api_service.route("/")
def hello():
    # currentSocketId = request.namespace.socket.sessid
    # print("CurrentSocketID: {}".format(currentSocketId))
    return render_template('pages/api.html')