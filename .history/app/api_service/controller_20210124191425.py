from flask import Blueprint, flash, render_template, request, session, abort, redirect, url_for
import requests
import os
from app import app

api_service = Blueprint('pages', __name__, url_prefix='')


@mod_pages.route("/")
def hello():
    # currentSocketId = request.namespace.socket.sessid
    # print("CurrentSocketID: {}".format(currentSocketId))
    return render_template('pages/index.html')