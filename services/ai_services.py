import os
from flask import request, jsonify
from dotenv import load_dotenv
from langchain_mistralai import MistralAIEmbeddings
from langchain_community.vectorstores.upstash import UpstashVectorStore
from langchain_core.documents import Document

load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
UPSTASH_VECTOR_REST_URL_FOUND = os.getenv("UPSTASH_VECTOR_REST_URL_FOUND")
UPSTASH_VECTOR_REST_TOKEN_FOUND = os.getenv("UPSTASH_VECTOR_REST_TOKEN_FOUND")


UPSTASH_VECTOR_REST_URL_LOST = os.getenv("UPSTASH_VECTOR_REST_URL_LOST")
UPSTASH_VECTOR_REST_TOKEN_LOST = os.getenv("UPSTASH_VECTOR_REST_TOKEN_LOST")

# create embeddings and insert into vector store
def embed_service():
    try:
        data = request.get_json()
        text = data["itemDesc"]
        _id = data["_id"]
        itemCategory = data["itemCategory"]

        if itemCategory == "lost":
            UPSTASH_VECTOR_REST_URL = UPSTASH_VECTOR_REST_URL_LOST
            UPSTASH_VECTOR_REST_TOKEN = UPSTASH_VECTOR_REST_TOKEN_LOST
        else:
            UPSTASH_VECTOR_REST_URL = UPSTASH_VECTOR_REST_URL_FOUND
            UPSTASH_VECTOR_REST_TOKEN = UPSTASH_VECTOR_REST_TOKEN_FOUND
        
        embeddings = MistralAIEmbeddings(
            model="mistral-embed",
        )

        # Store the c_id in the metadata for later retrieval
        documents = [Document(page_content=text, metadata={"_id": _id})]

        store = UpstashVectorStore(
            embedding=embeddings,
            index_url=UPSTASH_VECTOR_REST_URL,
            index_token=UPSTASH_VECTOR_REST_TOKEN
        )

        store.add_documents(documents)

        return jsonify({"message": "Successfully inserted vectors"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# query vector store and return index for similar complaints
def query_service():
    try:
        data = request.get_json()
        query_text = data["itemDesc"]

        embeddings = MistralAIEmbeddings(
            model="mistral-embed",
        )

        store = UpstashVectorStore(
            embedding=embeddings
        )

        results = store.similarity_search(query_text, k=5)

        # Extract c_ids from the metadata of similar documents
        similar_complaints = []
        for doc in results:
            if "_id" in doc.metadata:
                similar_complaints.append({
                    "_id": doc.metadata["_id"],
                    "content_preview": doc.page_content[:100] + "..." if len(doc.page_content) > 100 else doc.page_content
                })

        return jsonify({"similar_complaints": similar_complaints}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400
