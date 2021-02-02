from flask import Flask, render_template, url_for, redirect  
import os

app = Flask(__name__)
app.config.from_object('config')

from app.mod_pages.controllers import mod_pages as pages_module
from app.api_service.controller import api_service
app.register_blueprint(pages_module)
app.register_blueprint()

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import models

@app.errorhandler(404)
def not_found(error):  
    return render_template('404.html')

