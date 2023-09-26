"""
API module.
"""
# Import required modules
from flask import Blueprint
from flask_restful import Api

# Import resources
from ecomsync.resources.home import Home
from ecomsync.resources.order import OrderItem
from ecomsync.resources.option import OptionItem, OptionIndividualItem
from ecomsync.resources.product import ProductItem, ProductIndividualItem
from ecomsync.resources.manufacturer import ManufacturerItem, ManufacturerCollection

# Define a Blueprint for the API and set its prefix
api_bp = Blueprint("api", __name__, url_prefix="/api")
# Create an instance of the Flask-RESTful API using the Blueprint
api = Api(api_bp)

# Register the resource classes with the API and map them to their endpoints
api.add_resource(Home, "/")
api.add_resource(ManufacturerCollection, "/manufacturer/", endpoint='ManufacturerCollection')
api.add_resource(ManufacturerItem, "/manufacturer/<int:mid>", endpoint='ManufacturerItem')
api.add_resource(ProductItem, "/product/")
api.add_resource(ProductIndividualItem, '/product/<int:id>', endpoint='ProductIndividualItem')
api.add_resource(OrderItem, "/order/")
api.add_resource(OptionItem, '/option/')
api.add_resource(OptionIndividualItem, '/option/<int:oid>')
