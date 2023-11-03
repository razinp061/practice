from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models  import ItemModel
from schemas import ItemSchema, ItemUpdateSchema
from db import db
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("items", __name__ , description = "Operations on items")


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item


    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"Message":"Item deleted"}

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self,item_data, item_id):
        item = ItemModel.query.get(item_id)
        if item:
             item.name = item_data["name"]
             item.price = item_data["price"]

        else:
             item = ItemModel(id=item_id, **item_data)

        db.session.add(item)
        db.session.commit()

        return item





@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
           return ItemModel.query.all()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self,item_data):      
            item = ItemModel(**item_data)

            try:
                 db.session.add(item)
                 db.session.commit()
            except SQLAlchemyError:
                 abort (500, message = "An error occured while inserting the item")



            # for item in items.values():
            #     if (
            #         item_data['name'] == item['name']
            #         and item_data['store_id'] == item['store_id']
            #     ):
            #         abort(404, message= "Item already exists")                      #already checked  while creationg the database models


            # if item_data["store_id"] not in stores:
            #     abort(404, message= "Store  not found")
            
            # item_id = uuid.uuid4().hex
            # item = {**item_data, "id": item_id}
            # items[item_id] = item




            return item,201


