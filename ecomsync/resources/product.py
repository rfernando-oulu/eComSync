#Importing required packages
import json
from flask import Response, request, url_for, abort
from flask_restful import Api, Resource

from sqlalchemy.exc import IntegrityError
from datetime import datetime
from jsonschema import  ValidationError
from werkzeug.exceptions import BadRequest

#Importing from the project
from ecomsync.models import Product, ProductOption, Options, Manufacturer
from ecomsync import db
from ecomsync.utils import MasonBuilder
from ecomsync.constants import *
from ecomsync.utils import require_admin


#Defining constants
JSON = "application/json"

class ProductItem(Resource):
       
    # GET request handler
    def get(self):
        form_is = request.args.get('form', 'short')
        final_form = form_is == 'long'

        # Initializing response body
        body = {
            "products": []
        }

        # Iterating through all products and serializing them
        for product in Product.query.all():
            item = product.serialize(final_form)
            masonItem = MasonBuilder(item)
            masonItem.add_control("self", url_for("api.ProductIndividualItem", id=product.product_id))
            body["products"].append(masonItem)


        # Returning response
        return Response(json.dumps(body), 200, mimetype=JSON)
    
    # POST request handler
    def post(self):
        # Checking for JSON content type        
        if not request.json:
            abort(415, description="Request content type must be JSON")

        # Parsing request JSON data
        request_data = request.get_json()

        sku_exist = Product.query.filter_by(sku=request_data['sku']).first()

        if sku_exist:
            responseMessage = 'SKU already exists'
            response = Response(responseMessage, status=400)
            return response

        # Extracting required fields from request JSON data
        name_is = request_data['name']
        description_is = request_data['description']
        manufacturer_id_is = request_data['manufacturerId']
        print(manufacturer_id_is)
        sku_is = request_data['sku']
        quantity_is = request_data['quantity']
        image_is = request_data['image']
        price_is = float(request_data['price'])
        width_is = float(request_data['width'])
        selected_options_are = request_data['selectedOptions']
        print(selected_options_are)
        
        # Parsing and validating date_added field
        try:
            date_added_is = datetime.fromisoformat(request_data['date_added']) 
        except ValidationError as e:
            raise BadRequest(description=str(e))
        


        # Adding new product to the database
        try:
            product_item = Product(
                name = name_is,
                description = description_is,
                manufacturer_id = manufacturer_id_is,
                sku = sku_is,
                quantity = quantity_is,
                image = image_is,
                price = price_is,
                width = width_is,
                date_added = date_added_is
            )

            
            db.session.add(product_item)
            db.session.commit()

            pro_id = product_item.product_id 

            for option in selected_options_are:
                product_options_item = ProductOption(
                    product_id=pro_id,
                    option_id=option  
                )
                db.session.add(product_options_item)

            db.session.commit()

        # Handling errors
        except IntegrityError:
            abort(409)
        except (KeyError, ValueError, IntegrityError):
            abort(400)
        

        # Creating and returning success response
        responseMessage = 'Product Added Successfully'
        response = Response(responseMessage, status=201)
        return response
    


class ProductIndividualItem(Resource):

    def get(self, id):
        form_is = request.args.get('form', 'long')
        final_form = form_is == 'long'

        # Fetching the product from the database using its id
        product = Product.query.filter_by(product_id=id).first()

        if product is None:
            abort(404, description="Product_item not found")

        item = product.serialize(final_form)

        options = Options.query.join(ProductOption, Options.option_id == ProductOption.option_id).\
                    filter(ProductOption.product_id == product.product_id).all()
        
        lens_colors = []
        for option in options:
            lens_colors.append({
            "option_id": option.option_id,
            "option_name": option.name,
            "option_image": option.image
            })   
        
        item["options"] = lens_colors

        manufacturer_item = Manufacturer.query.filter_by(manufacturer_id=product.manufacturer_id).first()
        item["manufacturer_name"] = manufacturer_item.name
        # item.add_control("self", href=url_for(ProductItem, product_id=product.product_id))
        # item.add_control("profile", href=PROFILE_PRODUCT)
        # item.add_control("collection", href=url_for(Products))
        response = item

        # response = {
        #     "product": [
        #         {
        #             "id": product.product_id,
        #             "name": product.name,
        #             "sku": product.sku,
        #             "description": product.description
        #         } 
        #     ]
        # }

        return Response(json.dumps(response), 200, mimetype=JSON)

    # DELETE request handler
    def delete(self, id):
        # Fetching the product from the database using its id
        product = Product.query.filter_by(product_id=id).first()
        print(product)

        # If the product is not found, return a 404 Not Found error
        if product is None:
            abort(404, description="Product not found")

        # Fetching the product options related to the product
        product_options = ProductOption.query.filter_by(product_id=id).all()

        # Deleting the product options from the database
        for option in product_options:
            db.session.delete(option)

        # Deleting the product from the database
        db.session.delete(product)
        db.session.commit()

        # Creating and returning success response
        responseMessage = 'Product Deleted Successfully'
        response = Response(responseMessage, status=200)
        return response
    

    def put(self, id):
        # Checking for JSON content type
        if not request.json:
            abort(415, description="Request content type must be JSON")

        # Parsing request JSON data
        request_data = request.get_json()

        # Finding the product to update
        product = Product.query.filter_by(product_id=id).first()
        if not product:
            abort(404, description="Product not found")

        # Extracting required fields from request JSON data
        name_is = request_data['name_update']
        description_is = request_data['description_update']
        sku_is = request_data['sku_update']
        quantity_is = request_data['quantity_update']
        image_is = request_data['image_update']
        price_is = float(request_data['price_update']) if request_data['price_update'] else 0.0
        width_is = float(request_data['width_update']) if request_data['width_update'] else 0.0

        # Updating the product
        try:
            product.name = name_is
            product.description = description_is
            product.sku = sku_is
            product.quantity = quantity_is
            product.image = image_is
            product.price = price_is
            product.width = width_is

            db.session.commit()

        # Handling errors
        except IntegrityError as e:
            abort(409, description=str(e))
        except (KeyError, ValueError, IntegrityError) as e:
            abort(400, description=str(e))
        

        # Creating and returning success response
        responseMessage = 'Product Updated Successfully'
        response = Response(responseMessage, status=200)
        return response