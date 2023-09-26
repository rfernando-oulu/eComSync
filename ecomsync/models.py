"""
Model module.

This module provides models.
"""
import hashlib
from datetime import datetime
import click
from flask.cli import with_appcontext
from ecomsync import db

class ApiKey(db.Model):
    """
    Model representing an API key.

    API keys are used for authentication. 
    Each API key is unique, and some API keys have admin privileges.
    """
    key = db.Column(db.String(32), nullable=False, unique=True, primary_key=True)
    admin =  db.Column(db.Boolean, default=False)
    @staticmethod
    def key_hash(key):
        """
        Generates a hashed version of a given API key.

        The key is hashed using SHA-256, which provides a high level of security. 
        The resulting hash is unique for         each unique key input, and it 
        is extremely difficult (if not practically impossible) to derive the original 
        key from the hash. This means that even if someone gains access to 
        the hashed keys, they can't determine what the original keys were.

        Args:
            key (str): The API key to be hashed.

        Returns:
            bytes: The hashed key.
        """
        return hashlib.sha256(key.encode()).digest()

# Define the Options model
class ProductOption(db.Model):
    """
    Model representing a product option in the database.

    Each product option is linked to a specific product and a specific option. 
    This allows us to represent
    many-to-many relationships between products and options.
    """
    product_option_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.product_id"))
    option_id = db.Column(db.Integer, db.ForeignKey("options.option_id"))
    # Define a relationship to the Product model
    product = db.relationship("Product", back_populates="product_option" , \
                              foreign_keys=[product_id])
    options = db.relationship("Options", back_populates="product_option" , foreign_keys=[option_id])

# Define the Options model
class Options(db.Model):
    """
    Model representing an option in the database.

    Each option can be linked to multiple products through the ProductOption model,
    forming a many-to-many relationship.
    """
    option_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=True)
    image = db.Column(db.String(255), nullable=True)
    # Define a relationship to the Product model
    product_option = db.relationship("ProductOption", back_populates="options", \
                                     foreign_keys="ProductOption.option_id")
    # Define a method to serialize the Options model data to a dictionary
    def serialize(self):
        """
        Converts the Option instance into a dictionary for easier serialization.

        Returns:
            dict: A dictionary representation of the Option instance.
        """
        doc = {
            "id": self.option_id,
            "name": self.name,
            "image": self.image
        }
        return doc

# Define the Product model
class Product(db.Model):
    """
    Model representing a product in the database.

    Each product has various attributes such as name, description, 
    SKU, quantity, image, price, width,
    date added and a foreign key link to a manufacturer. 
    Relationships to the Order and Manufacturer
    models are also defined.
    """
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    description = db.Column(db.String(255), nullable=True)
    manufacturer_id = db.Column(db.Integer, db.ForeignKey("manufacturer.manufacturer_id"))
    sku = db.Column(db.String(64), nullable=True)
    quantity = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    width = db.Column(db.Float, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    # Define relationships to the Order and Manufacturer models
    order = db.relationship("Order", back_populates="product")
    manufacturer = db.relationship("Manufacturer", back_populates="product")
    product_option = db.relationship("ProductOption", back_populates="product")

    def serialize(self, short_form=False):
        """
        Converts the Product instance into a dictionary for easier serialization.

        Parameters:
            short_form (bool): 
            Determines the depth of serialization. If True, only critical
            information is included. If False, all attributes are included.
                               
        Returns:
            dict: A dictionary representation of the Product instance.
        """
        doc = {
            "id": self.product_id,
            "name": self.name
        }
        if short_form:
            doc["description"] = self.description
            doc["manufacturer_id"] = self.manufacturer_id
            doc["sku"] = self.sku
            doc["quantity"] = self.quantity
            doc["image"] = self.image
            doc["price"] = self.price
            doc["width"] = self.width
            doc["date_added"] = str(self.date_added)
        return doc

class Manufacturer(db.Model):
    """
    Represents a manufacturer with related products. 
    Contains methods to generate a JSON schema for 
    a manufacturer and serialize a manufacturer object.
    """
    manufacturer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=True)
    image = db.Column(db.String(255), nullable=True)
    description = db.Column(db.String(255), nullable=True)
    # Define a relationship to the Product model
    product = db.relationship("Product", back_populates="manufacturer")
    @staticmethod
    def json_schema():
        """
        Generates a JSON schema for a manufacturer object.
        
        Returns:
            dict: JSON schema defining a manufacturer.
        """
        schema = {
            "type": "object",
            "required": ["name", "image", "description"]
        }
        props = schema["properties"] = {}
        props["name"] = {
            "description": "handle of the Product",
            "type": "string"
        }
        props["image"] = {
            "description": "weight of the Product",
            "type": "string"
        }
        props["description"] = {
            "description": "Price of the Product",
            "type": "string"
        }
        return schema

    def serialize(self, short_form=False):
        """
        Serialize the Manufacturer model data to a dictionary.

        Parameters:
            short_form (bool):
            Determines whether to include all fields in the serialized output.
            If True, only includes 'name' in the output. 
            If False (default), includes 'name', 'image', and 'description' in the output.

        Returns:
            dict: Serialized Manufacturer data.
        """
        doc = {
            "name": self.name,
        }
        if not short_form:
            doc["description"] = self.description
        return doc

class Order(db.Model):
    """
    Model representing an order in the database.

    Each order has various attributes like firstname, 
    lastname, email, telephone, payment_address_1,
    payment_city, payment_postcode, payment_country, 
    total, date_added and a foreign key link to a 
    product. A relationship to the Product model is also defined.
    """
    order_id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(32), nullable=False)
    lastname = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(96), nullable=False)
    telephone = db.Column(db.String(32), nullable=False)
    product_id =  db.Column(db.Integer, db.ForeignKey("product.product_id"))
    payment_address_1 = db.Column(db.String(128), nullable=False)
    payment_city = db.Column(db.String(128), nullable=False)
    payment_postcode = db.Column(db.String(10), nullable=False)
    payment_country = db.Column(db.String(128), nullable=False)
    total = db.Column(db.Float, nullable=False)
    date_added = db.Column(db.DateTime, nullable=False)
    # Define a relationship to the Product model
    product = db.relationship("Product", back_populates="order")

    def serialize(self, short_form=False):
        """
        Converts the Order instance into a dictionary for easier serialization.

        Parameters:
            short_form (bool): Determines the depth of serialization. 
            If True, only critical
            information is included. If False, all attributes are included.
                               
        Returns:
            dict: A dictionary representation of the Order instance.
        """
        doc = {
            "firstname": self.firstname,
            "email": self.email,
        }
        if not short_form:
            doc["telephone"] = self.telephone
            doc["payment_address_1"] = self.payment_address_1
            doc["payment_city"] = self.payment_city
            doc["payment_postcode"] = self.payment_postcode
            doc["payment_country"] = self.payment_country
            doc["total"] = self.total
            doc["date_added"] = str(self.date_added)
        return doc

@click.command("masterkey")
@with_appcontext
def generate_master_key():
    """
    Command to generate a master API key. This key is randomly generated, hashed,
    stored in the database, and then printed to the console.

    This command does not take any arguments.

    Usage:
        flask masterkey
    """
    import secrets
    token = secrets.token_urlsafe()
    db_key = ApiKey(
        key=ApiKey.key_hash(token),
        admin=True
    )
    db.session.add(db_key)
    db.session.commit()
    print(token)

# Define a command line command to create the database tables
@click.command("init-db")
@with_appcontext
def init_db_command():
    """
    Command to initialize the database. This command creates all tables defined
    in the database model.

    This command does not take any arguments.

    Usage:
        flask init-db
    """
    db.create_all()

@click.command("populate-db")
@with_appcontext
def generate_test_data():
    """
    Command to populate the database with test data.

    This command does not take any arguments.

    Usage:
        flask populate-db
    """
    # from datetime import datetime
    # Add Product Options Data
    product_options_data = [
        (1, 1, 1),
        (2, 1, 2),
        (3, 1, 3),
        (4, 1, 4),
        (5, 2, 5),
        (6, 2, 6),
        (7, 2, 7),
        (8, 2, 8),
        (9, 3, 9),
        (10, 3, 10),
        (11, 3, 11),
        (12, 4, 12),
        (13, 4, 1),
        (14, 4, 2)
    ]
    # Add Options Data
    options_data = [
        (1, 'Black','/image/options/black.jpg'),
        (2, 'Black Gradient','/image/options/black-gradient.jpg'),
        (3, 'Brown','/image/options/brown.jpg'),
        (4, 'Brown Gradient','/image/options/brown-gradient.jpg'),
        (5, 'Green','/image/options/green.jpg'),
        (6, 'Flash Silver','/image/options/flash-silver.jpg'),
        (7, 'Purple Blue','/image/options/purple-blue.jpg'),
        (8, 'Light Blue','/image/options/light-blue.jpg'),
        (9, 'Yellow','/image/options/yellow.jpg'),
        (10, 'Rose Gold','/image/options/rose-gold.jpg'),
        (11, 'Red Orange','/image/options/red-orange.jpg'),
        (12, 'Blue','/image/options/blue.jpg')
    ]
    # Add Manuffacturer Data
    manufacturer_data = [
        (1, 'Ray Ban','/image/ray-ban.jpg','Ray Ban Sunglass Lenses'),
        (2, 'Arnette','/image/arnette.jpg','Arnette Sunglass Lenses'),
        (3, 'Oakley','/image/oakley.jpg','Oakley Sunglass Lenses'),
        (4, 'Burberry','/image/burberry.jpg','Burberry Sunglass Lenses'),
        (5, 'Dior','/image/dior.jpg','Dior Sunglass Lenses'),
        (6, 'Dolce & Gabbana','/image/dolce-gabbana.jpg','Dolce & Gabbana Sunglass Lenses'),
        (7, 'Emporio Armani','/image/emporio-armani.jpg','Emporio Armani Sunglass Lenses'),
        (8, 'Fendi','/image/fendi.jpg','Fendi Sunglass Lenses'),
        (9, 'Gucci','/image/gucci.jpg','Gucci Sunglass Lenses'),
        (10, 'Hugo Boss','/image/hugo-boss.jpg','Hugo Boss Sunglass Lenses'),
        (11, 'Jimmy Choo','/image/jimmy-choo.jpg','Jimmy Choo Sunglass Lenses'),
        (12, 'Kate Spade','/image/kate-spade.jpg','Kate Spade Sunglass Lenses'),
        (13, 'Lacoste','/image/lacoste.jpg','Lacoste Sunglass Lenses'),
        (14, 'Marc Jacobs','/image/marc-jacobs.jpg','Marc Jacobs Sunglass Lenses'),
        (15, 'Michael Kors','/image/michael-kors.jpg','Michael Kors Sunglass Lenses'),
        (16, 'Miu Miu','/image/miu-miu.jpg','Miu Miu Sunglass Lenses'),
        (17, 'Prada','/image/prada.jpg','Prada Sunglass Lenses'),
        (18, 'Polo Ralph Lauren','/image/polo-ralph-lauren.jpg',\
         'Polo Ralph Lauren Sunglass Lenses'),
        (19, 'Versace','/image/versace.jpg','Versace Sunglass Lenses'),
        (20, 'Swarovski','/image/swarovski.jpg','Swarovski Sunglass Lenses'),
        (21, 'Tom Ford','/image/tom-ford.jpg','Tom Ford Sunglass Lenses')
    ]
    # Add Product Data
    products = [
        (1, 'Rage 4025','Arnette Rage 4025 Sunglass','2','ANX4025000008BF2',\
         '1000','/image/products/rage_4025.jpg',39.55,3,'2023-02-27T02:14:38+00:00'),
        (2, 'RB3357','Ray Ban RB3357 Sunglass','1','RBX335700000006B',\
         '1000','/image/products/RB3357.jpg',39.55,3,'2023-02-27T02:14:38+00:00'),
        (3, 'GG2598','Gucci GG2598 Sunglass','9','GUCXGG259800006B',\
         '1000','/image/products/GG2598.jpg',39.55,3,'2023-02-27T02:14:38+00:00'),
        (4, 'Hijinx OO9021','Oakley Hijinx Sunglass','3','OAKXHIJINX006BF1',\
         '1000','/image/products/hijinx_OO9021.jpg',39.55,3,'2023-02-27T02:14:38+00:00')
    ]
    # Add Order Data
    orders = [
        (1, 'Roshan','Fernando','roshan@gmail.com','0123654789',1,\
         'yliopistokatu','Oulu','90570', 'Finland', 39.55,'2019-02-27T02:14:38+00:00'),
        (2, 'Dilshani','Vithanage','dilshani@gmail.com','0123654789',2,\
         'yliopistokatu','Oulu','90570', 'Finland', 39.55,'2019-02-27T02:14:38+00:00'),
        (3, 'Mithum','Fernando','mithum@gmail.com','0123654789',3,\
         'yliopistokatu','Oulu','90570', 'Finland', 39.55,'2019-02-27T02:14:38+00:00'),
    ]
    # date_added = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    for data in orders:
        order_item = Order(
            order_id=data[0],
            firstname=data[1],
            lastname=data[2],
            email=data[3],
            telephone=data[4],
            product_id=data[5],
            payment_address_1=data[6],
            payment_city=data[7],
            payment_postcode=data[8],
            payment_country=data[9],
            total=data[10],
            date_added=datetime.fromisoformat(data[11])
        )
        db.session.add(order_item)

    for data in products:
        product_item = Product(
            product_id=data[0],
            name=data[1],
            description=data[2],
            manufacturer_id=data[3],
            sku=data[4],
            quantity=data[5],
            image=data[6],
            price=data[7],
            width=data[8],
            date_added=datetime.fromisoformat(data[9])
        )
        db.session.add(product_item)

    for data in manufacturer_data:
        manufacturer_item = Manufacturer(
            manufacturer_id=data[0],
            name=data[1],
            image=data[2],
            description=data[3]
        )
        db.session.add(manufacturer_item)

    for data in options_data:
        options_item = Options(
            option_id=data[0],
            name=data[1],
            image=data[2]
        )
        db.session.add(options_item)

    for data in product_options_data:
        product_options_item = ProductOption(
            product_option_id=data[0],
            product_id=data[1],
            option_id=data[2]
        )
        db.session.add(product_options_item)

    db.session.commit()
