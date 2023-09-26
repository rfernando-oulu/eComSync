"""
Option module.

This module provides resources and methods to handle Option objects.
"""

# Import necessary libraries and modules
import json  # The json module allows you to use JSON data within Python.
from flask import Flask, Response, request, abort, jsonify  # Importing necessary objects from flask.
from flask_restful import Api, Resource  # Importing the Api and Resource classes from flask_restful.
from flask_sqlalchemy import SQLAlchemy  # Importing the SQLAlchemy class from flask_sqlalchemy.
from sqlalchemy.exc import IntegrityError  # Importing the IntegrityError exception from sqlalchemy.exc.
from datetime import datetime  # Importing the datetime class from the datetime module.
from jsonschema import validate, ValidationError, draft7_format_checker  # Importing necessary objects from jsonschema.
from werkzeug.exceptions import NotFound  # Importing the NotFound exception from werkzeug.exceptions.
from werkzeug.routing import BaseConverter  # Importing the BaseConverter class from werkzeug.routing.
from ecomsync.models import Options  # Importing the Options class from your application's models module.
from ecomsync import db  # Importing the db object from your application module.
from ecomsync.utils import require_admin

# Define the JSON content type
JSON = "application/json"  # Defining a constant for the JSON content type string.


# Define a Flask-RESTful Resource for handling Orders
class OptionItem(Resource):
    @require_admin
    def get(self):
        body = {"options": []}
        # Query the database for all options and add them to the JSON response body
        for option in Options.query.all():
            item = option.serialize()
            body["options"].append(item)
        
        # Return a Flask Response object containing the JSON response body
        return Response(json.dumps(body), 200, mimetype='application/json')
    
    @require_admin
    def post(self):        
        if not request.is_json:
            abort(415, description="Request content type must be JSON")

        # Parse the request JSON data
        request_data = request.get_json()

        # Extract option data from the request JSON data
        name_is = request_data.get('name', None)
        image_is = request_data.get('image', None)  # Optional field

        if not name_is:
            abort(400, description="Missing required field: 'name'")

        try:
            # Create a new Options object with the extracted data
            option_item = Options(
                name=name_is,
                image=image_is,
            )
            # Add the new Options object to the database session and commit the transaction
            db.session.add(option_item)
            db.session.commit()

        except IntegrityError:
            abort(409, description="Integrity Error occurred")

        # Create a Flask Response object with a success message and return it
        response_message = 'Option Added Successfully'
        response = Response(response_message, status=201)
        return response
    
class OptionIndividualItem(Resource):
    """Resource for handling individual Option items."""
    @require_admin
    def delete(self, oid):
        """Delete method to remove an Option by ID."""
        option = Options.query.filter_by(option_id=oid).first()

        if option is None:
            abort(404, description="Option not found")

        db.session.delete(option)
        db.session.commit()

        return Response('Option Deleted Successfully', status=200)


    def put(self, oid):
        """Put method to update an Option by ID."""
        if not request.json:
            abort(415, description="Request content type must be JSON")

        request_data = request.get_json()
        option = Options.query.filter_by(option_id=oid).first()

        if not option:
            abort(404, description="Option not found")

        name_is = request_data.get('name_update')
        image_is = request_data.get('image_update')

        try:
            if name_is is not None:
                option.name = name_is
            if image_is is not None:
                option.image = image_is
            db.session.commit()

        except IntegrityError as e:
            abort(409, description=str(e))
        except (KeyError, ValueError, IntegrityError) as e:
            abort(400, description=str(e))

        return Response('Option Updated Successfully', status=200)
