---
tags: [rag, retrieval, knowledge, embeddings, vector-database, dpr, sources]
last_updated: 2026-04-15
---

# RAG and Knowledge Retrieval

## Provenance
- Theme: `task-aware-routing`
- Registry: [[clipping-registry]]
- Raw-source verification: [[../workflows/raw-source-verification|Raw Source Verification]]

## Sources Included
- `Clippings/Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.md` (Lewis et al., 2020)
- `Clippings/Dense Passage Retrieval for Open-Domain Question Answering.md`
- `Clippings/What are embeddings in machine learning.md`
- `Clippings/What is a vector database  How vector databases work.md`
- `Clippings/Similarity settings  Elasticsearch Reference.md`

---

## Why RAG Matters

LLMs have two types of memory:
- **Parametric memory**: knowledge encoded in model weights (static, limited, can't be updated)
- **Non-parametric memory**: external knowledge retrieved at inference time (dynamic, updateable, inspectable)

RAG combines both: use non-parametric retrieval to ground parametric generation.

**Core limitation RAG solves**: Models cannot update world knowledge, can't cite sources, and hallucinate when asked about facts outside training data.

---

## RAG — Original Formulation (Lewis et al., 2020)

### Architecture
```
Query x
  → Retriever (DPR): p_η(z|x) → top-K documents
  → Generator (BART/seq2seq): p_θ(y|x,z)
  → Output y
```

### Two variants
| Model | Document usage | Formula |
|-------|---------------|---------|
| **RAG-Sequence** | Same document for entire output | Marginalize over docs for full sequence |
| **RAG-Token** | Different document per output token | Marginalize independently at each token |

RAG-Token is more flexible; RAG-Sequence is simpler and often used in practice.

### Key formula (RAG-Sequence)
```
p(y|x) ≈ Σ_{z ∈ top-K} p_η(z|x) · p_θ(y|x,z)
```

### Results
- SOTA on open-domain QA: NaturalQuestions, WebQuestions, TriviaQA, CuratedTrec
- More factual, specific, and diverse language generation than parametric-only baselines
- Knowledge update: replace document index without retraining model

---

## Dense Passage Retrieval (DPR)

The retriever component in RAG. Uses a bi-encoder architecture:

```
p_η(z|x) ∝ exp(d(z)ᵀ q(x))
d(z) = BERT_document(z)      # document encoder
q(x) = BERT_query(x)         # query encoder
```

**Key operation**: Maximum Inner Product Search (MIPS) to find top-K documents — approximate MIPS runs in sub-linear time.

**Initialization**: Pre-trained on TriviaQA and NaturalQuestions; fine-tuned end-to-end with generator.

**Dense vs sparse retrieval**:
| Method | Representation | Speed | Quality |
|--------|---------------|-------|---------|
| BM25 (sparse) | TF-IDF bags of words | Very fast, exact | Good for keyword match |
| DPR (dense) | Learned BERT embeddings | Fast (ANN search) | Better for semantic match |
| Hybrid | Combine both | Moderate | Best of both worlds |

---

## Embeddings

Embeddings are dense vector representations of data (text, images, code) that capture semantic meaning in high-dimensional space.

### Properties
- Semantically similar items → similar vectors (small cosine distance)
- Operations in embedding space have semantic meaning
- Dimensionality: typically 768–4096 dimensions

### How they're produced
1. Pass input through encoder model (BERT, Ada-002, Cohere Embed, etc.)
2. Extract representation from [CLS] token or pooled output
3. Optionally normalize to unit sphere (for cosine similarity)

### Key similarity metrics
| Metric | Formula | Best for |
|--------|---------|----------|
| Cosine similarity | (A·B)/(‖A‖‖B‖) | Unit-normalized vectors, semantic similarity |
| Dot product | A·B | When scale matters; faster than cosine |
| L2 distance | ‖A-B‖₂ | When Euclidean distance is meaningful |

### Elasticsearch similarity settings
- `bm25` (default): sparse term-based similarity
- `dot_product`: requires normalized vectors; equivalent to cosine if normalized
- `cosine`: handles unnormalized vectors; slightly more expensive
- `l2_norm`: Euclidean distance; use for certain geometric embedding spaces

---

## Vector Databases

Specialized databases for approximate nearest-neighbor (ANN) search over embedding vectors.

### Why not use regular databases?
- High-dimensional vector similarity is not supported by traditional B-tree indexes
- Need approximate nearest neighbor algorithms for scalability
- Specialized hardware/SIMD operations for vector math

### Popular vector databases
| Database | Notes |
|---------|-------|
| Pinecone | Managed, production-ready |
| Weaviate | Open-source, hybrid search |
| Qdrant | Rust-based, performant |
| Chroma | Simple, dev-friendly |
| pgvector | PostgreSQL extension |
| FAISS | Facebook library; in-process, not a full DB |

### ANN algorithms
| Algorithm | Approach |
|---------|---------|
| HNSW | Hierarchical Navigable Small World; excellent recall/speed tradeoff |
| IVF | Inverted File; centroid clustering then exhaustive within cluster |
| PQ (Product Quantization) | Compress vectors for memory efficiency |
| LSH | Locality Sensitive Hashing; older, less used now |

### Operational parameters
- **ef_construction**: HNSW build quality (higher = better quality, slower build)
- **ef_search**: Query recall/speed tradeoff (higher = better recall, slower search)
- **nprobe** (IVF): number of clusters to search

---

## RAG Security Considerations

RAG significantly expands the attack surface for prompt injection:

| Attack type | Mechanism |
|------------|-----------|
| **Document poisoning** | Attacker inserts documents into corpus with injected instructions |
| **Indirect prompt injection** | Retrieved document contains instructions that redirect agent behavior |
| **Knowledge base pollution** | Gradually corrupt retrieval index to degrade responses |

**Defenses**:
- Segregate retrieved content from trusted instructions
- Validate and sanitize documents at ingest time
- Apply output filtering to catch anomalies from retrieved content
- Use provenance tracking to identify which retrieved doc influenced output

See [[owasp-llm-top10]] — LLM01 (Prompt Injection, indirect type) and LLM04 (Data Poisoning).

---

## RAG vs Fine-tuning Decision

| Concern | RAG | Fine-tuning |
|---------|-----|-------------|
| Update knowledge without retraining | ✓ (update corpus) | ✗ (retrain) |
| Factual grounding with citations | ✓ | Difficult |
| Style / format adaptation | Limited | ✓ |
| Reduce hallucination | Helps significantly | Helps somewhat |
| Cost | Runtime retrieval cost | Training cost amortized |
| Latency | Additional retrieval step | No extra latency |
| Domain specialization | Moderate | Strong |

---

## Connection to This Project

The wiki memory layer is a form of RAG:
- Clippings/wiki = non-parametric knowledge base
- Each agent request = query into the wiki
- hot.md + preload = approximate "retrieval" for highest-relevance context
- The difference from standard RAG: retrieval is wikilink-based (structured) not embedding-based (semantic)

Future: embedding-based retrieval over the wiki would enable semantic search instead of manual navigation.

---

## Related
- [[../components/knowledge-wiki|Knowledge Wiki]] — current wiki retrieval architecture
- [[owasp-llm-top10]] — RAG-specific security risks (indirect injection, poisoning)
- [[adversarial-ml]] — data poisoning applied to RAG corpora
- [[task-aware-routing]] — routing can use RAG to determine if wiki can answer
- [[../workflows/slm-fine-tuning-pipeline|SLM Fine-Tuning Pipeline]] — fine-tuning as alternative to RAG
