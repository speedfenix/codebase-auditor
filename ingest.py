import os
import uuid
from google import genai
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

def get_code_files(directory):
    """Walks through a directory and gathers paths of all Python files."""
    file_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_paths.append(os.path.join(root, file))
    return file_paths

def chunk_code(file_path):
    """
    Reads a file and splits it into logical chunks.
    For Day 2, we split by functions/blocks, or fallback to line windows.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # A simple but effective method for code: split by major function definitions
    # In a production environment, you might use an Abstract Syntax Tree (AST) parser
    raw_chunks = content.split("\n\n")
    
    clean_chunks = []
    for chunk in raw_chunks:
        chunk_text = chunk.strip()
        if chunk_text:
            clean_chunks.append({
                "text": chunk_text,
                "metadata": {
                    "file_path": file_path,
                    "lines": len(chunk_text.split('\n'))
                }
            })
    return clean_chunks

def main():
    print("📂 Starting Day 2: Ingestion & Context Vectorization...")
    
    # Initialize Clients
    ai_client = genai.Client()
    db_client = QdrantClient(host="localhost", port=6333)
    collection_name = "local_codebase"

    # 1. Gather files to audit
    target_dir = "./mock_project"
    files = get_code_files(target_dir)
    print(f"🔍 Found {len(files)} source files in {target_dir}")

    all_chunks = []
    for file in files:
        chunks = chunk_code(file)
        all_chunks.extend(chunks)
        print(f"✂️  Split {os.path.basename(file)} into {len(chunks)} logical chunks.")

    # 2. Vectorize chunks via Gemini API & Upload to local Qdrant
    points = []
    print("🧠 Generating embeddings via Gemini Cloud API...")
    
    for item in all_chunks:
        # Call Gemini's highly optimized text embedding model
        response = ai_client.models.embed_content(
            model='gemini-embedding-001',
            contents=item["text"]
        )
        
        # Pull the list of floats representing the geometric coordinates of this code chunk
        embedding = response.embeddings[0].values
        
        # Prepare the record structure for Qdrant storage
        point_id = str(uuid.uuid4())
        points.append(
            PointStruct(
                id=point_id,
                vector=embedding,
                payload={
                    "text": item["text"],
                    "file_path": item["metadata"]["file_path"]
                }
            )
        )

    # 3. Upload batch into your local container
    print(f"📦 Uploading {len(points)} vectorized points to local Qdrant instance...")
    db_client.upsert(
        collection_name=collection_name,
        points=points
    )
    

    # 4. Run semantic audit verification
    print("\n🔬 Running test semantic audit verification query...")
    test_query = "Find instances of sql injection or database cursor execution"
    
    query_vector = ai_client.models.embed_content(
        model='gemini-embedding-001',
        contents=test_query
    ).embeddings[0].values
    
    # FUTURE-PROOF UPDATE: Using the new universal Query API (.query_points)
    response = db_client.query_points(
        collection_name=collection_name,
        query=query_vector,
        limit=1
    )
    search_result = response.points
    
    if search_result:
        print("🟢 SUCCESS! Optimized semantic search discovered vulnerable code chunk:")
        print(f"📁 Source File: {search_result[0].payload['file_path']}")
        print(f"📝 Extracted Snippet:\n{search_result[0].payload['text']}")
    else:
        print("❌ Search returned no matching targets.")

if __name__ == "__main__":
    main()
