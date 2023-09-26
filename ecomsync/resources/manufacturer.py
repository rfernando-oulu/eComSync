"""
Manufacturer module.

This module provides resources and methods to handle Manufacturer objects.
"""

# Standard library imports
from datetime import datetime

# Related third party imports
import json
from flask import Flask, Response, request, url_for, abort, jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from jsonschema import validate, ValidationError, draft7_format_checker
from werkzeug.exceptions import NotFound
from werkzeug.routing import BaseConverter

# Local application imports
from ecomsync.models import Manufacturer, Product
from ecomsync import db, api
from ecomsync.utils import MasonBuilder
from ecomsync.constants import *
from ecomsync.utils import require_admin, ManufacturerBuilder



# Constants - JSON content type
JSON = "application/json"

class ManufacturerItem(Resource):
    """Resource for retrieving a single Manufacturer by name."""
    def get(self, mid):
        
        manufacturer_item = Manufacturer.query.filter_by(manufacturer_id=mid).first()

        # If the product is not found, return a 404 Not Found error
        if manufacturer_item is None:
            abort(404, description="Manufacturer_item not found")

        # Fetching all products by the same manufacturer
        products = Product.query.filter_by(manufacturer_id=mid).all()

        # Serializing products
        products_list = []
        for product in products:
            products_list.append({
                "product_id": product.product_id,
                "product_name": product.name,
                "@controls": {
                    "method": "GET",
                    "title": "View product",
                    "href": url_for("api.ProductIndividualItem", id=product.product_id),
				
			}
                # Add other product fields as needed
            })    

        response = {
            "manufacturer": [
                {
                    "id": manufacturer_item.manufacturer_id,
                    "name": manufacturer_item.name,
                    "image": manufacturer_item.image,
                    "description": manufacturer_item.description,
                    "@controls": {
                        "self": {
                            "href": url_for("api.ManufacturerItem", mid=manufacturer_item.manufacturer_id)
                        }
                    },
                    "products": products_list
                } 
            ]
        }

            
        return Response(json.dumps(response), 200, mimetype=JSON)

    def delete(self, mid):
        """Delete method to remove a Manufacturer by ID."""
        manufacturer = Manufacturer.query.filter_by(manufacturer_id=mid).first()

        if manufacturer is None:
            abort(404, description="Product not found")

        db.session.delete(manufacturer)
        db.session.commit()

        return Response('Manufacturer Deleted Successfully', status=200)
    
    def put(self, mid):
        """Put method to update a Manufacturer by ID."""
        if not request.json:
            abort(415, description="Request content type must be JSON")

        request_data = request.get_json()
        manufacturer = Manufacturer.query.filter_by(manufacturer_id=mid).first()

        if not manufacturer:
            abort(404, description="Manufacturer not found")

        name_is = request_data.get('name_update')
        description_is = request_data.get('description_update')
        image_is = request_data.get('image_update')

        try:
            manufacturer.name = name_is
            manufacturer.description = description_is
            manufacturer.image = image_is
            db.session.commit()
        
        except IntegrityError as e:
            abort(409, description=str(e))
        except (KeyError, ValueError, IntegrityError) as e:
            abort(400, description=str(e))
        

        return Response('Manufacturer Updated Successfully', status=200)
    
class ManufacturerCollection(Resource):
    """Resource for retrieving a collection of all Manufacturers."""
    @require_admin
    def get(self):
        """Get method for retrieving all Manufacturers."""
        form_is = request.args.get('form', 'long')
        final_form = form_is == 'short'

        manufacturers = Manufacturer.query.all()
        # Construct the response body containing the serialized Manufacturer objects
        body = {"manufacturers": []}
        body = ManufacturerBuilder()
        body["items"] = []  
        body.add_control_all_manufacturers()

        for manufacturer_item in manufacturers:
            manufacturer_json = ManufacturerBuilder(manufacturer_item.serialize(final_form))
            manufacturer_json.add_control_view_product(manufacturer_item)      
            body["items"].append(manufacturer_json)

            
        return Response(json.dumps(body), 200, mimetype=JSON)
        
    
    def post(self):
        """Post method for creating a Manufacturer."""  
        if not request.json:
            abort(415, description="Request content type must be JSON")

        request_data = request.get_json()
        name_is = request_data['name']
        image_is = request_data['image']
        description_is = request_data['description']

        # Attempt to create a new Manufacturer record in the database
        try:
            manufacture_item = Manufacturer(
                name=name_is,
                image=image_is,
                description=description_is
            )
            db.session.add(manufacture_item)
            db.session.commit()
        
        
        except IntegrityError:
            abort(409)
        except (KeyError, ValueError, IntegrityError):
            abort(400)
        

        # If the record was successfully created, return a 201 Created response
        return Response('Manufacturer Added Successfully', status=201)
    
# class ManufacturerIndividualItem(Resource):
#     """Resource for handling individual Manufacturer items."""
    
#     def delete(self, mid):
#         """Delete method to remove a Manufacturer by ID."""
#         manufacturer = Manufacturer.query.filter_by(manufacturer_id=mid).first()

#         if manufacturer is None:
#             abort(404, description="Product not found")

#         db.session.delete(manufacturer)
#         db.session.commit()

#         return Response('Manufacturer Deleted Successfully', status=200)
    
#     def put(self, mid):
#         """Put method to update a Manufacturer by ID."""
#         if not request.json:
#             abort(415, description="Request content type must be JSON")

#         request_data = request.get_json()
#         manufacturer = Manufacturer.query.filter_by(manufacturer_id=mid).first()

#         if not manufacturer:
#             abort(404, description="Manufacturer not found")

#         name_is = request_data.get('name_update')
#         description_is = request_data.get('description_update')
#         image_is = request_data.get('image_update')

#         try:
#             manufacturer.name = name_is
#             manufacturer.description = description_is
#             manufacturer.image = image_is
#             db.session.commit()
        
#         except IntegrityError as e:
#             abort(409, description=str(e))
#         except (KeyError, ValueError, IntegrityError) as e:
#             abort(400, description=str(e))
        

#         return Response('Manufacturer Updated Successfully', status=200)