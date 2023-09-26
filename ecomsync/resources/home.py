#Importing required packages
import json
from flask import Flask, Response, request, abort, jsonify
from flask_restful import Api, Resource

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from jsonschema import validate, ValidationError, draft7_format_checker
from werkzeug.exceptions import NotFound
from werkzeug.routing import BaseConverter

#Importing from the project
from ecomsync.models import Product
from ecomsync import db
from ecomsync.utils import require_admin


#Defining constants
JSON = "application/json"

class Home(Resource):
    # GET request handler
    def get(self):
        responseMessage = 'Home Page'
        response = Response(responseMessage, status=201)
        return response