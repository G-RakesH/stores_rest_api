from flask import request
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from schemas import ItemUpdateSchema, ItemSchema
import uuid
from models import ItemModel, StoreModel
from sqlalchemy.exc import SQLAlchemyError
from db import db

blp = Blueprint("items", __name__)


@blp.route('/item/<item_id>')
class ItemByItemId(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return "item"
        # item = ItemModel.query.get_or_404(item_id)
        # db.session.delete(item)
        # db.session.commit()
        # return {"message": "Deleted a store"}

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)

        if item:
            item.name = item_data['name']
            item.price = item_data['price']
        else:
            item = ItemModel(id= item_id, **item_data)

        db.session.add(item)
        db.session.commit()

        return item


@blp.route('/item')
class Item(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)
        if db.session.query(ItemModel).filter_by(name=item.name).first():
            return item
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Error Occured while inserting the item at sqlalchemy.")

        return item






