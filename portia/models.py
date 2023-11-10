from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect

db = SQLAlchemy()


class JSONMixin:
    def todict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}


class User(db.Model, JSONMixin):
    id = db.Column(db.Integer, db.Identity(start=1), primary_key=True)
    username = db.Column(db.String(200), unique=True)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.String(1))
    join_date = db.Column(db.DateTime)


class DeliveryAddresses(db.Model, JSONMixin):
    id = db.Column(db.Integer, db.Identity(start=1), primary_key=True)
    username = db.Column(db.String(200), db.ForeignKey('user.username'))
    postcode = db.Column(db.String(5))
    address1 = db.Column(db.String(255))
    address2 = db.Column(db.String(255))
    created_date = db.Column(db.DateTime)
    user = db.relationship("User")


class Goods(db.Model, JSONMixin):
    id = db.Column(db.Integer, db.Identity(start=1), primary_key=True)
    goods_code = db.Column(db.String(255), unique=True)
    goods_name = db.Column(db.String(255))
    price = db.Column(db.Integer)
    goods_photo = db.Column(db.String(255))
    goods_cnt = db.Column(db.Integer)
    goods_description = db.Column(db.Text)
    created_date = db.Column(db.DateTime)


class Orders(db.Model, JSONMixin):
    id = db.Column(db.Integer, db.Identity(start=1), primary_key=True)
    order_str_id = db.Column(db.String(100))
    username = db.Column(db.String(200), db.ForeignKey('user.username'))
    order_date = db.Column(db.DateTime)
    ship_to_name = db.Column(db.String(20))
    ship_to_phone = db.Column(db.String(14))
    ship_to_addresses =db.Column(db.String(150))
    ship_to_postcode = db.Column(db.String(5))
    order_status = db.Column(db.String(4), doc='결제 상태')
    order_items = db.relationship("OrdersItem")


class OrdersItem(db.Model, JSONMixin):
    id = db.Column(db.Integer, db.Identity(start=1), primary_key=True)
    goods = db.Column(db.String(255), db.ForeignKey('goods.goods_code'))
    goods_price = db.Column(db.Integer)
    goods_cnt = db.Column(db.Integer)


class GoodsTracking(db.Model, JSONMixin):
    id = db.Column(db.Integer, db.Identity(start=1), primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    delivery_start_date = db.Column(db.DateTime)
    delivery_end_date = db.Column(db.DateTime)
    tracking_number = db.Column(db.String(50))
    tracking_status = db.Column(db.String(30))


class Basket(db.Model, JSONMixin):
    id = db.Column(db.Integer, db.Identity(start=1), primary_key=True)
    username = db.Column(db.String(200), db.ForeignKey('user.username'))
    goods = db.Column(db.String(255), db.ForeignKey('goods.goods_code'))
    goods_item = db.relationship("Goods")
    goods_cnt = db.Column(db.Integer)
