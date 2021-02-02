from flask import Blueprint, flash, render_template, request, session, abort, redirect, url_for
import requests
import os
from app import app

api_service = Blueprint('pages', __name__, url_prefix='/apis/')


@api_service.route("/")
def hello():
    return render_template('pages/index.html')