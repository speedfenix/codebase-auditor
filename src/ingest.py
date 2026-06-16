import os
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, ScalarQuantization, ScalarQuantizationConfig, ScalarType

def run_clean_ingestion():
    print("📂 Starting Day 6: Clean Room Ingestion Pipeline...")
    
    # 1. Initialize Qdrant Client (Connecting to your Docker instance)
    client = QdrantClient(host="localhost", port=6333)
    collection_name = "local_codebase"
    
    # 🛡️ Modern API Guard: Replace obsolete recreate_collection with explicit existence checks
    print(f"🔍 Probing database: Checking if collection '{collection_name}' exists...")
    if client.collection_exists(collection_name=collection_name):
        print(f"💥 Purging stale index: Deleting collection '{collection_name}' to prevent vector pollution...")
        client.delete_collection(collection_name=collection_name)
    
    print(f"🏗️  Initializing fresh collection '{collection_name}'...")
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
        # Strict Pydantic v2 compliant structure for local 8GB RAM Optimization
        quantization_config=ScalarQuantization(
            scalar=ScalarQuantizationConfig(
                type=ScalarType.INT8,  
                quantile=0.99,
                always_ram=True        
            )
        )
    )
    
    # 2. Unified active workspace path
    target_dir = "./targets/mock_project"
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        
    source_files = [f for f in os.listdir(target_dir) if f.endswith('.py')]
    print(f"🔍 Scan complete: Found {len(source_files)} source files inside unified path '{target_dir}'")
    
    points_to_upload = []
    idx = 1
    
    for file_name in source_files:
        file_path = os.path.join(target_dir, file_name)
        with open(file_path, "r") as f:
            content = f.read()
        
        # Simple structural chunking emulation
        chunks = [content] if len(content) < 300 else [content[i:i+300] for i in range(0, len(content), 300)]
        print(f"✂️  Split {file_name} into {len(chunks)} logical chunks.")
        
        for chunk in chunks:
            mock_vector = [0.1] * 1536 
            points_to_upload.append({
                "id": idx,
                "vector": mock_vector,
                "payload": {"file_path": file_path, "code_chunk": chunk}
            })
            idx += 1

    # 3. Commit clean payload
    print(f"📦 Uploading {len(points_to_upload)} unique points to local Qdrant instance...")
    client.upsert(collection_name=collection_name, points=points_to_upload)
    print("🟢 SUCCESS! Database completely synchronized with no duplicated entries.\n")

if __name__ == "__main__":
    run_clean_ingestion()