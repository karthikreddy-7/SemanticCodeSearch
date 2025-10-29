from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F

# Local paths
EMBED_PATH = "C:/Home/models/all-MiniLM-L6-v2"
RERANK_PATH = "C:/Home/models/bge-reranker-base"

# Load locally
embedder = SentenceTransformer(EMBED_PATH)
tokenizer = AutoTokenizer.from_pretrained(RERANK_PATH)
reranker = AutoModelForSequenceClassification.from_pretrained(RERANK_PATH)

query = "How to parse JSON in Python?"
docs = [
    "import json\njson.loads('{\"a\":1}')",
    "console.log('Hello World')",
    "Connection conn = DriverManager.getConnection(url)"
]

# ---- Embedding-based retrieval ----
q_emb = embedder.encode(query, convert_to_tensor=True)
d_embs = embedder.encode(docs, convert_to_tensor=True)
sim_scores = F.cosine_similarity(q_emb, d_embs).tolist()
print("Embedding similarity:", sim_scores)

# ---- Reranking ----
pair_inputs = tokenizer(
    [query] * len(docs),
    docs,
    return_tensors="pt",
    padding=True,
    truncation=True,
    max_length=512
)

with torch.no_grad():
    outputs = reranker(**pair_inputs)
    rerank_scores = outputs.logits.squeeze().tolist()

# Handle single vs multiple docs
if isinstance(rerank_scores, float):
    rerank_scores = [rerank_scores]

print("Reranker scores:", rerank_scores)

best = rerank_scores.index(max(rerank_scores))
print("Best match:", docs[best])
