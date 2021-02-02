from flask import Flask, render_template, url_for, redirect  
import os

app = Flask(__name__)
app.config.from_object('config')


from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

@app.errorhandler(404)
def not_found(error):  
    return render_template('404.html')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
db.create_all()

from app.mod_pages.views import mod_pages as pages_module
from app.api_service.views import api_service as api_module

app.register_blueprint(pages_module)
app.register_blueprint(api_module)
