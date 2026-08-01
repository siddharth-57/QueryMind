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

# Project Setup

## Prerequisites
- These instructions assume you already have **Docker**, **Git**, and **Python** installed on your host.

---

## 1. Clone the Repository

    git clone https://github.com/siddharth-57/QueryMind.git

    cd QueryMind

---

## 2. Create and Activate a Virtual Environment

Create a virtual environment using Python 3.11:

    python3.11 -m venv venv

Activate the virtual environment:

    source venv/bin/activate

---

## 3. Install Project Dependencies

    pip install -r requirements.txt

---

## 4. Configure Environment Variables

Copy the example environment file:

    cp .env.example .env

Fill the `.env` file with the required credentials.

---

## 5. Setup Ollama

Use Ollama to run open-source models locally on your host.

### Install Ollama

    brew install ollama

### Start the Ollama Server

    ollama serve

> **Note:** Keep this terminal window open.

### Download Required Models

Pull the embedding model:

    ollama pull qwen3-embedding:4b

Pull the LLM model:

    ollama pull qwen3:8b

> **Note:** You can replace these model names with other models available on Ollama or even use an API to access any other model.

---

## 6. Start Docker Containers

    docker compose up -d

---

## 7. Enable the pgvector Extension

Connect to the PostgreSQL database:

    docker exec -it QueryMind-postgres psql -U postgres -d QueryMind

Inside PostgreSQL, enable the extension:

    CREATE EXTENSION IF NOT EXISTS vector;

To verify that the extension has been enabled:

    \dx

> Although the pgvector image includes the extension binaries, PostgreSQL still requires you to enable the extension once per database using `CREATE EXTENSION`.

---

## 8. Run Database Migrations

Generate the migration:

    alembic revision --autogenerate -m "create tables"

Apply the migration:

    alembic upgrade head

---

# Running the Project

Run the following scripts in order.

### 1. Synchronize Emails

    python3 -m QueryMind.scripts.test_sync_service

### 2. Run the Preprocessing Pipeline

    python3 -m QueryMind.scripts.test_preprocessing_pipeline

### 3. Test the Qdrant Connection

    python3 -m QueryMind.scripts.test_qdrant

### 4. Index the Document Chunks

    python3 -m QueryMind.scripts.index_chunks

### 5. Test Retrieval

    python3 -m QueryMind.scripts.test_retrieval
