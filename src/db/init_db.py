from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, ScalarQuantization, ScalarQuantizationConfig, ScalarType

def optimize_and_init():
    print("🛠️  Starting Manual Qdrant Optimization Pipeline...")
    client = QdrantClient(host="localhost", port=6333)
    collection_name = "local_codebase"
    
    # Drop any existing unoptimized collection
    if client.collection_exists(collection_name):
        print(f"🗑️  Removing old unoptimized collection: '{collection_name}'")
        client.delete_collection(collection_name)
        
    print(f"🏗️  Creating optimized collection '{collection_name}' at 3072 dimensions...")
    
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=3072, 
            distance=Distance.COSINE
        ),
        # SENIOR OPTIMIZATION: Compress vector data to protect your 8GB RAM layout
        quantization_config=ScalarQuantization(
            scalar=ScalarQuantizationConfig(
                type=ScalarType.INT8,
                always_ram=True # Keeps the compressed index in memory for blazing fast lookups
            )
        )
    )
    print("🟢 STATUS: Collection created successfully with INT8 Scalar Quantization optimizations!")

if __name__ == "__main__":
    optimize_and_init()
