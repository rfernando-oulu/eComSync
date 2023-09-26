#Import necessary libraries and modules
import json
from flask import Flask, Response, request, abort, jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from jsonschema import validate, ValidationError, draft7_format_checker
from werkzeug.exceptions import NotFound, BadRequest
from werkzeug.routing import BaseConverter
from ecomsync.models import Order
from ecomsync import db

from ecomsync.utils import require_admin


# Define the JSON content type
JSON = "application/json"

# Define a Flask-RESTful Resource for handling Orders
class OrderItem(Resource):
    def get(self):
        form_is = request.args.get('form', 'long')
        short_form=False
        if form_is == 'short':
            short_form=True


        body = {"orders": []}
        # Query the database for all orders and add them to the JSON response body
        for order in Order.query.all():
            item = order.serialize(short_form)
            body["orders"].append(item)
        
        # Return a Flask Response object containing the JSON response body
        return Response(json.dumps(body), 200, mimetype=JSON)
    
    def post(self):        
        if not request.json:
            abort(415, description="Request content type must be JSON")

        # Parse the request JSON data
        request_data = request.get_json()

        # Extract order data from the request JSON data
        firstname_is = request_data['firstname']
        lastname_is = request_data['lastname']
        email_is = request_data['email']
        telephone_is = request_data['telephone']
        product_id_is = 212
        payment_address_1_is = request_data['payment_address_1']
        payment_city_is = request_data['payment_city']
        payment_postcode_is = request_data['payment_postcode']
        payment_country_is = request_data['payment_country']
        total_is = request_data['total']

        # Validate and extract the date_added field from the request JSON data
        try:
            date_added_is = datetime.fromisoformat(request_data['date_added']) 
        except ValueError as e:
            raise BadRequest(description=str(e))

        try:
            # Create a new Order object with the extracted data
            order_item = Order(
                firstname = firstname_is,
                lastname = lastname_is,
                email = email_is,
                telephone = telephone_is,
                product_id = product_id_is,
                payment_address_1 = payment_address_1_is,
                payment_city = payment_city_is,
                payment_postcode = payment_postcode_is,
                payment_country = payment_country_is,
                total = total_is,
                date_added = date_added_is
            )
            # Add the new Order object to the database session and commit the transaction
            db.session.add(order_item)
            db.session.commit()

        except IntegrityError:
            abort(409)
        except (KeyError, ValueError, IntegrityError):
            abort(400)
        

        # Create a Flask Response object with a success message and return it
        responseMessage = 'Order Added Successfully'
        response = Response(responseMessage, status=201)
        return response