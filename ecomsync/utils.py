"""
Util module.
"""
import json
import secrets
from flask import Response, request, url_for
from werkzeug.exceptions import Forbidden, NotFound
from werkzeug.routing import BaseConverter

from ecomsync.models import Manufacturer, Product, ApiKey

class MasonBuilder(dict):
    """
    A convenience class for managing dictionaries that represent Mason
    objects. It provides nice shorthands for inserting some of the more
    elements into the object but mostly is just a parent for the much more
    useful subclass defined next. This class is generic in the sense that it
    does not contain any application specific implementation details.
    
    Note that child classes should set the *DELETE_RELATION* to the application
    specific relation name from the application namespace. The IANA standard
    does not define a link relation for deleting something.
    """

    DELETE_RELATION = ""

    def add_error(self, title, details):
        """
        Adds an error element to the object. Should only be used for the root
        object, and only in error scenarios.
        Note: Mason allows more than one string in the @messages property (it's
        in fact an array). However we are being lazy and supporting just one
        message.
        : param str title: Short title for the error
        : param str details: Longer human-readable description
        """

        self["@error"] = {
            "@message": title,
            "@messages": [details],
        }

    def add_namespace(self, nameSpace, uri):
        """
        Adds a namespace element to the object. A namespace defines where our
        link relations are coming from. The URI can be an address where
        developers can find information about our link relations.
        : param str ns: the namespace prefix
        : param str uri: the identifier URI of the namespace
        """

        if "@namespaces" not in self:
            self["@namespaces"] = {}

        self["@namespaces"][nameSpace] = {
            "name": uri
        }

    def add_control(self, ctrl_name, href, **kwargs):
        """
        Adds a control property to an object. Also adds the @controls property
        if it doesn't exist on the object yet. Technically only certain
        properties are allowed for kwargs but again we're being lazy and don't
        perform any checking.
        The allowed properties can be found from here
        https://github.com/JornWildt/Mason/blob/master/Documentation/Mason-draft-2.md
        : param str ctrl_name: name of the control (including namespace if any)
        : param str href: target URI for the control
        """

        if "@controls" not in self:
            self["@controls"] = {}

        self["@controls"][ctrl_name] = kwargs
        self["@controls"][ctrl_name]["href"] = href

    def add_control_post(self, ctrl_name, title, href, schema):
        """
        Utility method for adding POST type controls. The control is
        constructed from the method's parameters. Method and encoding are
        fixed to "POST" and "json" respectively.
        
        : param str ctrl_name: name of the control (including namespace if any)
        : param str href: target URI for the control
        : param str title: human-readable title for the control
        : param dict schema: a dictionary representing a valid JSON schema
        """

        self.add_control(
            ctrl_name,
            href,
            method="POST",
            encoding="json",
            title=title,
            schema=schema
        )

    def add_control_put(self, title, href, schema):
        """
        Utility method for adding PUT type controls. The control is
        constructed from the method's parameters. Control name, method and
        encoding are fixed to "edit", "PUT" and "json" respectively.
        
        : param str href: target URI for the control
        : param str title: human-readable title for the control
        : param dict schema: a dictionary representing a valid JSON schema
        """

        self.add_control(
            "edit",
            href,
            method="PUT",
            encoding="json",
            title=title,
            schema=schema
        )

    def add_control_delete(self, title, href):
        """
        Utility method for adding PUT type controls. The control is
        constructed from the method's parameters. Control method is fixed to
        "DELETE", and control's name is read from the class attribute
        *DELETE_RELATION* which needs to be overridden by the child class.

        : param str href: target URI for the control
        : param str title: human-readable title for the control
        """

        self.add_control(
            "mumeta:delete",
            href,
            method="DELETE",
            title=title,
        )

class ManufacturerBuilder(MasonBuilder):
    """
    Represents a builder for Manufacturer objects, 
    which provides methods to add hypermedia controls.

    Extends MasonBuilder from the Flask-Mason library, 
    which helps build hypermedia-based APIs.
    """
    def add_control_all_manufacturers(self):
        """
        Adds a hypermedia control for retrieving 
        all manufacturers.

        This control, when followed, allows a client 
        to retrieve a list of all manufacturers.
        """
        self.add_control(
            "storage:manufacturer-all",
            url_for("api.ManufacturerCollection"),
            method="GET",
            title="List of all products"
        )

    def add_control_view_product(self, manufacturer):
        """
        Adds a hypermedia control for retrieving a specific manufacturer.

        This control, when followed, allows a client to retrieve 
        information about a specific manufacturer.

        Parameters:
            manufacturer (Manufacturer): The manufacturer object 
            for which the control is added.
        """
        self.add_control(
            "storage:manufacturer",
            url_for("api.ManufacturerItem", mid=manufacturer.manufacturer_id),
            method="GET",
            title="View a manufacturer",
            schema=Manufacturer.json_schema()
        )

class ProductConverter(BaseConverter):
    """
    Custom URL converter for Flask routes, converting product IDs to 
    Product instances and vice versa.

    Extends BaseConverter from Werkzeug (which Flask uses for URL routing).
    """
    def to_python(self, prod_id):
        """
        Converts a product_id to a Product instance.

        Args:
            product_id (str): The product_id as specified in the URL.

        Returns:
            Product: The Product instance associated with the given product_id.

        Raises:
            NotFound: If no Product is found with the given product_id.
        """
        product_item = Product.query.filter_by(product_id=prod_id).first()

        if product_item is None:
            raise NotFound

        return product_item

    def to_url(self, product):
        """
        Converts a Product instance to a product_id string.

        Args:
            product (Product): The Product instance.

        Returns:
            str: The product_id of the Product instance.
        """
        return str(product.product_id)

class ManufacturerConverter(BaseConverter):
    """
    Custom URL converter for Flask routes, converting manufacturer 
    IDs to Manufacturer instances and vice versa.

    Extends BaseConverter from Werkzeug (which Flask uses for URL routing).
    """
    def to_python(self, manu_id):
        """
        Converts a manufacturer_id to a Manufacturer instance.

        Args:
            manufacturer_id (str): The manufacturer_id as specified in the URL.

        Returns:
            Manufacturer: The Manufacturer instance associated with 
            the given manufacturer_id.

        Raises:
            NotFound: If no Manufacturer is found with the given manufacturer_id.
        """
        manufacturer = Manufacturer.query.filter_by(manufacturer_id=manu_id).first()

        if manufacturer is None:
            raise NotFound

        return manufacturer

    def to_url(self, manufacturer):
        """
        Converts a Manufacturer instance to a manufacturer_id string.

        Args:
            manufacturer (Manufacturer): The Manufacturer instance.

        Returns:
            str: The manufacturer_id of the Manufacturer instance.
        """
        return str(manufacturer.manufacturer_id)

def require_admin(func):
    """
    Decorator function to require admin privileges for a function.

    This decorator verifies the access key present in the request headers. It first hashes the key,
    then compares the hashed key with the stored hash of the admin key. If they match, 
    the wrapped function is executed. Otherwise, a Forbidden exception is raised.

    Parameters:
    func (function): The function to be wrapped.

    Returns:
    wrapper (function): The wrapped function.
    """
    def wrapper(*args, **kwargs):
        key_hash = ApiKey.key_hash(request.headers.get("access-Key", "").strip())
        db_key = ApiKey.query.filter_by(admin=True).first()
        if secrets.compare_digest(key_hash, db_key.key):
            return func(*args, **kwargs)
        raise Forbidden
    return wrapper
