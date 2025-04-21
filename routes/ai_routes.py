from flask import Blueprint
from ..services.ai_services import *

# Create a Blueprint
ai_routes_bp = Blueprint('ai_routes', __name__)

# -------- AI Services APIs --------

@ai_routes_bp.route("/embed_store", methods=["POST"])
def embed_store():
    return embed_service()

@ai_routes_bp.route("/query", methods=["POST"])
def query():
    return query_service()
