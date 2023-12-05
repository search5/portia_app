from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from sqlalchemy.ext.hybrid import hybrid_property

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
    phone = db.Column(db.String(50), nullable=False)
    is_admin = db.Column(db.String(1))
    join_date = db.Column(db.DateTime)


class DeliveryAddresses(db.Model, JSONMixin):
    id = db.Column(db.Integer, db.Identity(start=1), primary_key=True)
    username = db.Column(db.String(200), db.ForeignKey('user.username'))
    postcode = db.Column(db.String(5))
    address1 = db.Column(db.String(255))
    address2 = db.Column(db.String(255))
    created_date = db.Column(db.DateTime)
    user = db.relationship("User", backref="addresses")


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
    order_str_id = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(200), db.ForeignKey('user.username'))
    user = db.relationship("User", backref="orders")
    order_date = db.Column(db.DateTime)
    ship_to_name = db.Column(db.String(20))
    ship_to_phone = db.Column(db.String(14))
    ship_to_addresses =db.Column(db.String(150))
    ship_to_postcode = db.Column(db.String(5))
    order_status = db.Column(db.String(4), doc='결제 상태')
    order_items = db.relationship("OrdersItem", order_by="desc(OrdersItem.id)")

    @hybrid_property
    def order_summary_title(self):
        first_order_item = self.order_items[0].goods_item.goods_name
        order_item_cnt = len(self.order_items)
        if order_item_cnt > 1:
            first_order_item = f'{first_order_item} 외 {order_item_cnt - 1}개'
        return first_order_item

    @hybrid_property
    def order_total_price(self):
        total_price = [item.goods_price * item.goods_cnt for item in self.order_items]
        return sum(total_price)

    @hybrid_property
    def order_representative_image_info(self):
        order_item = self.order_items[0].goods_item
        return {"goods_code": order_item.goods_code, "img_path": order_item.goods_photo or ''}


class OrdersItem(db.Model, JSONMixin):
    id = db.Column(db.Integer, db.Identity(start=1), primary_key=True)
    order_str_id = db.Column(db.String(100), db.ForeignKey('orders.order_str_id'))
    goods_code = db.Column(db.String(255), db.ForeignKey('goods.goods_code'))
    goods_item = db.relationship("Goods")
    goods_price = db.Column(db.Integer)
    goods_cnt = db.Column(db.Integer)


class Basket(db.Model, JSONMixin):
    id = db.Column(db.Integer, db.Identity(start=1), primary_key=True)
    username = db.Column(db.String(200), db.ForeignKey('user.username'))
    goods_code = db.Column(db.String(255), db.ForeignKey('goods.goods_code'))
    goods_item = db.relationship("Goods")
    goods_cnt = db.Column(db.Integer)
