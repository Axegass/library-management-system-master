from flask import Flask, g, escape, session, redirect, render_template, request, jsonify, Response
from Misc.functions import *
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', '#$ab9&^BB00_.')

# Setting DAO Class (will pick MongoDB if MONGODB_URL is present)
from Models.DAO import DAO

DAO = DAO(app)

# Registering blueprints
from routes.user import user_view
from routes.book import book_view
from routes.admin import admin_view

# Registering custom functions to be used within templates
app.jinja_env.globals.update(
    ago=ago,
    str=str,
)

app.register_blueprint(user_view)
app.register_blueprint(book_view)
app.register_blueprint(admin_view)