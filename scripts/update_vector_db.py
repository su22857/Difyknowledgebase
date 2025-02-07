import os
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from sentence_transformers import SentenceTransformer
from pathlib import Path

# 配置参数
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = "knowledge_base"
MODEL_NAME = "all-MiniLM-L6-v2"

# 初始化模型和客户端
model = SentenceTransformer(MODEL_NAME)
client = QdrantClient(host="qdrant", port=6333)

# 创建集合（如果不存在）
try:
    client.get_collection(COLLECTION_NAME)
except Exception:
    client.if client.collection_exists(collection_name):
    client.delete_collection(collection_name)
client.create_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=384, distance=Distance.COSINE),
)
    )

# 读取所有 Markdown 文件
docs = []
for path in Path(".").rglob("*.md"):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
        docs.append({
            "text": content,
            "source": str(path)
        })

# 生成 Embeddings 并上传
embeddings = model.encode([doc["text"] for doc in docs])
points = [
    {
        "id": idx,
        "vector": embedding.tolist(),
        "payload": doc
    }
    for idx, (doc, embedding) in enumerate(zip(docs, embeddings))
]
client.upsert(collection_name=COLLECTION_NAME, points=points)
print(f"Uploaded {len(points)} documents to Qdrant.")
