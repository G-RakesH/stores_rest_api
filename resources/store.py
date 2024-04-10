from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models import StoreModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from schemas import StoreSchema

blp = Blueprint("stores", __name__)


@blp.route('/store/<store_id>')
class StoreByStoreId(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return "store"
        # store = StoreModel.query.get_or_404(store_id)
        # db.session.delete(store)
        # db.session.commit()
        # return {"message": "Deleted an item"}


@blp.route('/store')
class Store(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        if db.session.query(StoreModel).filter_by(name=store.name).first():
            return store
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(500, message="Error Occurred while inserting the store at sqlalchemy.")

        except SQLAlchemyError:
            abort(500, message="Error Occurred while inserting the store at sqlalchemy.")

        return store



