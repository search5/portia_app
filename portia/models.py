from datetime import datetime
from typing import Optional

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped


class Base(DeclarativeBase):
    def todict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}


db = SQLAlchemy(model_class=Base)


class User(Base):
    id: Mapped[int] = mapped_column(db.Identity(start=1), primary_key=True)
    username: Mapped[str] = mapped_column(db.String(200), unique=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    password: Mapped[str] = mapped_column(db.String(200), nullable=False)
    email: Mapped[str] = mapped_column(db.String(200), nullable=False)
    phone: Mapped[str] = mapped_column(db.String(50), nullable=False)
    is_admin: Mapped[Optional[str]] = mapped_column(db.String(1))
    join_date: Mapped[Optional[datetime]] = mapped_column()


class DeliveryAddresses(Base):
    id: Mapped[int] = mapped_column(db.Identity(start=1), primary_key=True)
    username: Mapped[str] = mapped_column(db.String(200), db.ForeignKey('user.username'))
    postcode: Mapped[Optional[str]] = mapped_column(db.String(5))
    address1: Mapped[Optional[str]] = mapped_column(db.String(255))
    address2: Mapped[Optional[str]] = mapped_column(db.String(255))
    created_date: Mapped[Optional[datetime]] = mapped_column()
    user = db.relationship("User", backref="addresses")


class Goods(Base):
    id: Mapped[int] = mapped_column(db.Identity(start=1), primary_key=True)
    goods_code: Mapped[str] = mapped_column(db.String(255), unique=True)
    goods_name: Mapped[Optional[str]] = mapped_column(db.String(255))
    price: Mapped[Optional[int]] = mapped_column(db.Integer)
    goods_photo: Mapped[Optional[str]] = mapped_column(db.String(255))
    goods_cnt: Mapped[Optional[int]] = mapped_column(db.Integer)
    goods_description: Mapped[Optional[str]] = mapped_column(db.Text)
    created_date: Mapped[Optional[datetime]] = mapped_column()


class Orders(Base):
    id: Mapped[int] = mapped_column(db.Identity(start=1), primary_key=True)
    order_str_id: Mapped[str] = mapped_column(db.String(100), unique=True)
    username: Mapped[str] = mapped_column(db.String(200), db.ForeignKey('user.username'))
    user = db.relationship("User", backref="orders")
    order_date: Mapped[Optional[datetime]] = mapped_column()
    ship_to_name: Mapped[Optional[str]] = mapped_column(db.String(20))
    ship_to_phone: Mapped[Optional[str]] = mapped_column(db.String(14))
    ship_to_addresses: Mapped[Optional[str]] = mapped_column(db.String(150))
    ship_to_postcode: Mapped[Optional[str]] = mapped_column(db.String(5))
    order_status: Mapped[Optional[str]] = mapped_column(db.String(4), doc='결제 상태')
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


class OrdersItem(Base):
    id: Mapped[int] = mapped_column(db.Identity(start=1), primary_key=True)
    order_str_id: Mapped[str] = mapped_column(db.String(100), db.ForeignKey('orders.order_str_id'))
    goods_code: Mapped[str] = mapped_column(db.String(255), db.ForeignKey('goods.goods_code'))
    goods_item = db.relationship("Goods")
    goods_price: Mapped[int] = mapped_column(db.Integer)
    goods_cnt: Mapped[int] = mapped_column(db.Integer)


class Basket(Base):
    id: Mapped[int] = mapped_column(db.Identity(start=1), primary_key=True)
    username: Mapped[Optional[str]] = mapped_column(db.String(200), db.ForeignKey('user.username'))
    goods_code: Mapped[Optional[str]] = mapped_column(db.String(255), db.ForeignKey('goods.goods_code'))
    goods_item = db.relationship("Goods")
    goods_cnt: Mapped[Optional[int]] = mapped_column(db.Integer)
