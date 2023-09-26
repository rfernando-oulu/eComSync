
import json
import os
import pytest
import tempfile
import time
from datetime import datetime
from flask.testing import FlaskClient
from jsonschema import validate
from sqlalchemy.engine import Engine
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError, StatementError
from werkzeug.datastructures import Headers
from jsonschema import validate, ValidationError, draft7_format_checker


from ecomsync import create_app, db
from ecomsync.models import *


@pytest.fixture
def client():
    db_fd, db_fname = tempfile.mkstemp()
    config = {
        "SQLALCHEMY_DATABASE_URI": "sqlite:///" + db_fname,
        "TESTING": True
    }
    
    app = create_app(config)
    
    with app.app_context():
        db.create_all()
        _populate_db()
        
    # app.test_client_class = AuthHeaderClient
    yield app.test_client()
    
    os.close(db_fd)
    os.unlink(db_fname)

def _populate_db():
    from datetime import datetime
    # Add Manufacturer data
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

class TestManufacturerCollection(object):
    
    RESOURCE_URL = "/api/manufacturer/"

    def test_get(self, client):
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200

class TestManufacturerItem(object):
    
    RESOURCE_URL = "/api/manufacturer/1"

    def test_get(self, client):
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200

class TestProductCollection(object):
    
    RESOURCE_URL = "/api/product/"

    def test_get(self, client):
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200

class TestProductItem(object):
    
    RESOURCE_URL = "/api/product/1"

    def test_get(self, client):
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200

class TestOrderCollection(object):
    
    RESOURCE_URL = "/api/order/"

    def test_get(self, client):
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200