from qdrant_client import QdrantClient
from google import genai

client = QdrantClient(host="localhost", port=6333)
ai_client = genai.Client()