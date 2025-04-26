import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask_sqlalchemy import SQLAlchemy
from models.item_model import Item
import grpc
from concurrent import futures
import grpc_server.server_pb2 as pb2
import grpc_server.server_pb2_grpc as pb2_grpc
db = SQLAlchemy()

class ItemService(pb2_grpc.ItemServiceServicer):
    def __init__(self, app):
        self.app = app
        
    def GetAllItems(self, request, context):
        try:
            print("Received request to get all items")
            with self.app.app_context():
                items = db.session.query(Item).all()
                if not items:
                    return pb2.Items(items=[])
                return pb2.Items(items=[item.json() for item in items])
        except Exception as e:
            with self.app.app_context():
                db.session.rollback()
            error = str(e.__dict__['orig']) if hasattr(e, '__dict__') and 'orig' in e.__dict__ else str(e)
            context.set_details(f"Database error: {str(error)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return pb2.Items(items=[])

    def GetMultipleItems(self, request, context):
        try:
            print("Received request to get multiple items")
            with self.app.app_context():
                items = db.session.query(Item).filter(Item._id.in_(request.ids)).all()
                if not items:
                    return pb2.Items(items=[])
                return pb2.Items(items=[item.json() for item in items])
        except Exception as e:
            with self.app.app_context():
                db.session.rollback()
            error = str(e.__dict__['orig']) if hasattr(e, '__dict__') and 'orig' in e.__dict__ else str(e)
            context.set_details(f"Database error: {str(error)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return pb2.Items(items=[])

    def CreateItem(self, request, context):
        try:
            print("Received request to create item")
            with self.app.app_context():
                new_item = Item(
                    item_title=request.item_title,
                    item_description=request.item_description,
                    item_image=request.item_image if request.HasField('item_image') else None,
                    item_category=request.item_category,
                    user_id=request.user_id
                )
                db.session.add(new_item)
                db.session.commit()
                return pb2.sucessResponse(isSuceeded=True)
        except Exception as e:
            with self.app.app_context():
                db.session.rollback()
            error = str(e.__dict__['orig']) if hasattr(e, '__dict__') and 'orig' in e.__dict__ else str(e)
            context.set_details(f"Database error: {str(error)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return pb2.sucessResponse(isSuceeded=False)

    def UpdateItem(self, request, context):
        try:
            print("Received request to update item")
            with self.app.app_context():
                item = db.session.query(Item).filter_by(_id=request.id).first()
                if not item:
                    context.set_details("Item not found")
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    return pb2.sucessResponse(isSuceeded=False)
                
                item.item_title = request.item_title
                item.item_description = request.item_description
                item.item_category = request.item_category
                if request.HasField('item_image'):
                    item.item_image = request.item_image
                
                db.session.commit()
                return pb2.sucessResponse(isSuceeded=True)
        except Exception as e:
            with self.app.app_context():
                db.session.rollback()
            error = str(e.__dict__['orig']) if hasattr(e, '__dict__') and 'orig' in e.__dict__ else str(e)
            context.set_details(f"Database error: {str(error)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return pb2.sucessResponse(isSuceeded=False)

    def DeleteItem(self, request, context):
        try:
            print("Received request to delete item")
            with self.app.app_context():
                item = db.session.query(Item).filter_by(_id=request.id).first()
                if not item:
                    context.set_details("Item not found")
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    return pb2.sucessResponse(isSuceeded=False)
                
                db.session.delete(item)
                db.session.commit()
                return pb2.sucessResponse(isSuceeded=True)
        except Exception as e:
            with self.app.app_context():
                db.session.rollback()
            error = str(e.__dict__['orig']) if hasattr(e, '__dict__') and 'orig' in e.__dict__ else str(e)
            context.set_details(f"Database error: {str(error)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return pb2.sucessResponse(isSuceeded=False)

    def GetItemById(self, request, context):
        try:
            print("Received request to get item by ID")
            with self.app.app_context():
                item = db.session.query(Item).filter_by(_id=request.id).first()
                if not item:
                    context.set_details("Item not found")
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    return pb2.Item()
                
                return pb2.Item(
                    id=item._id,
                    item_title=item.item_title,
                    item_description=item.item_description,
                    item_image=item.item_image if item.item_image else None,
                    item_category=item.item_category,
                    user_id=item.user_id
                )
        except Exception as e:
            with self.app.app_context():
                db.session.rollback()
            error = str(e.__dict__['orig']) if hasattr(e, '__dict__') and 'orig' in e.__dict__ else str(e)
            context.set_details(f"Database error: {str(error)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return pb2.Item()

def serve():
    from flask import Flask
    from config import Config
    
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_ItemServiceServicer_to_server(ItemService(app), server)
    server.add_insecure_port("0.0.0.0:50052")
    server.start()
    print("Server started on port 50052")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()


