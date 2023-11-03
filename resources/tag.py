from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models  import TagModel,StoreModel,ItemModel
from schemas import TagSchema, TagAndItemSchema
from db import db
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("tags", __name__ , description = "Operations on tags")

@blp.route("/store/<string:store_id>/tag")
class TagInStore(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)

        return store.tags.all()

    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        if TagModel.query.filter(TagModel.store_id == store_id, TagModel.name == tag_data["name"]).first():
            abort (400, message = "A tag with that name already exists")
        tag = TagModel(**tag_data, store_id=store_id)

        try:
            db.session.add(tag)
            db.session.commit()

        except SQLAlchemyError as e:
            abort(
                500,
                message = str(e)
            )

        return tag
    

@blp.route("/item/<string:item_id>/tag/<string:tag_id>")
class LinkTagsToItem(MethodView):
    @blp.response(201, TagSchema)
    def post(self,  item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.append(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort (500, message = "An error ocuured while inserting the tag")

        
        return tag
    
    @blp.response(200, TagAndItemSchema)
    def delete(self, item_id, tag_id):      #unlink item from tag
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.remove(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort (500, message = "An error occured while removing a item ")

        return {"message" : "Item removed from the tag", "item": item, "tag": tag}
    






@blp.route("/tag/<string:tag_id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        return tag