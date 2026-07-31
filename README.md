<!-- Project documentation -->
# QueryMind

QueryMind is an AI-powered Retrieval-Augmented Generation (RAG) application that enables users to query unstructured data using natural language. The system ingests documents, generates vector embeddings, stores them in Qdrant, retrieves semantically relevant information, and uses a Large Language Model (LLM) to generate accurate, context-aware responses.

---

## Features

- Document ingestion pipeline
- Automatic text chunking
- Embedding generation
- Vector similarity search using Qdrant
- Retrieval-Augmented Generation (RAG)
- Natural language question answering
- Metadata storage and retrieval
- Dockerized deployment
- Modular LLM provider architecture

---

## Tech Stack

### Backend
- Python
- SQLAlchemy
- Alembic

### Database
- PostgreSQL
- Qdrant (Vector Database)

### AI/ML
- Ollama
- Embedding Models
- Retrieval-Augmented Generation (RAG)

### Infrastructure
- Docker
- Docker Compose

---

## Project Architecture

```
                Documents
                    │
                    ▼
          Document Ingestion
                    │
                    ▼
             Text Chunking
                    │
                    ▼
         Embedding Generation
                    │
                    ▼
      Qdrant Vector Database
                    │
      Vector Similarity Search
                    │
                    ▼
          Retrieved Context
                    │
                    ▼
               Ollama LLM
                    │
                    ▼
          Natural Language Answer
```

---

## How It Works

### 1. Document Ingestion

Documents are read and processed before being stored.

---

### 2. Text Chunking

Large documents are divided into smaller chunks suitable for embedding generation.

---

### 3. Embedding Generation

Each chunk is converted into a dense vector representation using an embedding model.

---

### 4. Vector Storage

Embeddings are stored inside Qdrant along with references to the original documents and associated metadata.

---

### 5. Semantic Retrieval

When a user asks a question:

- The question is converted into an embedding.
- A similarity search retrieves the most relevant document chunks.
- Retrieved context is sent to the LLM.

---

### 6. Response Generation

The LLM generates an answer grounded in the retrieved context instead of relying solely on its pre-trained knowledge.

---

## Example Workflow

```
User Question

        │

        ▼

Generate Query Embedding

        │

        ▼

Qdrant Similarity Search

        │

        ▼

Retrieve Top-k Chunks

        │

        ▼

Send Context + Question to LLM

        │

        ▼

Generate Answer

        │

        ▼

Return Response
```

---

## Future Improvements

- Hybrid Search (Vector + Keyword)
- Multi-document retrieval
- Streaming responses
- Support for multiple LLM providers
- Conversation memory
- User authentication
- Web interface
- Knowledge graph integration
- API endpoints for external applications