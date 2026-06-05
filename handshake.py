import os
from google import genai
from qdrant_client import QdrantClient

def main():
    print("🚀 Starting Day 1 Handshake Verification...")

    # 1. Test the Google AI Studio Cloud Connection
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ ERROR: GEMINI_API_KEY environment variable not found!")
        return
        
    print("🔗 Connecting to Google AI Studio...")
    ai_client = genai.Client()
    
    # We use gemini-2.5-flash: it is lightning fast and free
    response = ai_client.models.generate_content(
        model='gemini-2.5-flash',
        contents='Reply with exactly: Cloud connection successful!',
    )
    print(f"📡 Cloud Response: {response.text.strip()}")

    # 2. Test the Local Qdrant Vector DB Connection
    print("🔗 Connecting to local Qdrant Docker container...")
    db_client = QdrantClient(host="localhost", port=6333)
    
    # Try to create a fresh collection for your codebase vectors
    collection_name = "local_codebase"
    
    # Clean up old test data if it exists
    if db_client.collection_exists(collection_name):
        db_client.delete_collection(collection_name)
        
    # Initialize the collection (using 768 dimensions for standard embeddings)
    db_client.create_collection(
        collection_name=collection_name,
        vectors_config={"size": 768, "distance": "Cosine"}
    )
    
    print(f"📦 Local DB Status: Success! Created collection '{collection_name}'.")
    print("🟢 DAY 1 COMPLETE: Your hybrid environment is fully operational!")

if __name__ == "__main__":
    main()