# Ancient Egypt RAG Assistant

A Retrieval-Augmented Generation (RAG) application that answers questions about Ancient Egypt using information retrieved from a provided historical document.

The project uses a Chroma vector store for retrieval, Hugging Face embeddings for semantic search, Groq for LLM generation, FastAPI for the backend API, and Streamlit for the frontend interface.

## Setup

### 1. Clone the Repository

```bash
git clone <https://github.com/esraa-sobhy/rag-assistant-project.git>
cd rag-assistant-project
```

### 2. Create and Activate a Virtual Environment

Create a virtual environment:

```bash
py -m venv .venv
```

Activate it in Git Bash:

```bash
source .venv/Scripts/activate
```

### 3. Install Backend Requirements

```bash
cd backend
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file inside the `backend` folder based on `.env.example`.

Example:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-20b
VECTOR_STORE_PATH=data/vector_store
FRONTEND_ORIGIN=http://localhost:8501
```

Do not commit the real `.env` file or API key to GitHub.

---

## Project Architecture

```text
User
 │
 ▼
Streamlit Frontend
 │
 ▼
FastAPI Backend
 │
 ├── Query
 │    │
 │    ▼
 │  Chroma Vector Store
 │    │
 │    ▼
 │  Relevant Documents
 │
 ▼
Groq LLM
 │
 ▼
Grounded Answer + Sources
```

## Features

* Document-based question answering
* Semantic document retrieval using embeddings
* Persistent Chroma vector store
* Grounded answers based only on retrieved context
* Source/chunk references in responses
* FastAPI REST API
* Streamlit chat-style interface
* Backend health check
* Automated API tests
* Environment variables for API configuration
* Retrieval and generation pipeline
* Evaluation using sample questions

## Technologies

* Python
* LangChain
* Chroma
* Hugging Face Sentence Transformers
* Groq API
* FastAPI
* Pydantic
* Streamlit
* Requests
* Pytest

## Models

### Embedding Model

```text
sentence-transformers/all-MiniLM-L6-v2
```

### Language Model

```text
openai/gpt-oss-20b
```

The language model is accessed through the Groq API.

## Project Structure

```text
rag-assistant-project/
│
├── notebooks/
│   ├── rag_assistant.ipynb
│   └── rag_llm.ipynb
│
├── Data/
│   └── ancient_egypt.html
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   │   └── routes/
│   │   │       └── query.py
│   │   ├── core/
│   │   │   └── config.py
│   │   ├── schemas/
│   │   │   └── query.py
│   │   ├── services/
│   │   │   ├── retrieval.py
│   │   │   └── generation.py
│   │   └── utils/
│   │       └── logging_config.py
│   │
│   ├── data/
│   │   └── vector_store/
│   │
│   ├── tests/
│   │   └── test_query.py
│   │
│   ├── .env.example
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── app.py
│   ├── api_client.py
│   ├── .env.example
│   └── requirements.txt
│
├── .gitignore
├── README.md
└── requirements.txt
```

## RAG Pipeline

### 1. Document Loading

The Ancient Egypt document is loaded from the provided HTML file.

```text
Data/ancient_egypt.html
```

The document is processed by the RAG pipeline before being stored in the vector database.

### 2. Text Splitting

The document is divided into smaller chunks using recursive chunking.

Configuration:

```text
Chunk size: 1000
Chunk overlap: 150
```

The overlap helps preserve contextual information between neighboring chunks.

### 3. Embeddings

Each chunk is converted into a vector representation using:

```text
sentence-transformers/all-MiniLM-L6-v2
```

The same embedding model is used when querying the persisted vector store.

### 4. Vector Store

The generated embeddings are stored in Chroma as a persistent vector store.

```text
backend/data/vector_store/
```

The vector store is produced by the notebook and then served by the FastAPI backend.

This allows the backend to retrieve relevant document chunks without rebuilding the vector database for every request.

### 5. Retrieval

When the user asks a question, the system performs semantic similarity search and retrieves the most relevant chunks.

The current retrieval configuration uses:

```text
k = 2
```

This means that the top two most relevant chunks are retrieved for each question.

### 6. Generation

The retrieved context is passed to the Groq language model.

The prompt instructs the model to:

* Use only the provided context
* Avoid relying on outside knowledge
* Avoid making up information
* Generate a grounded answer
* Mention the relevant source information

## Evaluation

The RAG pipeline includes retrieval and answer evaluation using a set of sample questions.

The evaluation checks whether:

* The retrieved chunks are relevant to the question
* The generated answer is grounded in the retrieved context
* The answer correctly addresses the question

The final notebook contains an evaluation table with the tested questions and their evaluation results.

## Backend API

The backend is implemented using FastAPI.

### Health Check

```http
GET /health
```

Example response:

```json
{
  "status": "ok"
}
```

### Query Endpoint

```http
POST /query
```

Request:

```json
{
  "question": "What was the importance of the Nile River to Ancient Egypt?"
}
```

Response:

```json
{
  "answer": "The Nile was essential to Ancient Egypt...",
  "sources": [
    "Chunk 1 — ancient_egypt.html",
    "Chunk 2 — ancient_egypt.html"
  ]
}
```

## Running the Backend

From the `backend` directory:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

Health check:

```text
http://127.0.0.1:8000/health
```

## Running the Frontend

Open a second terminal.

Activate the virtual environment and move to the frontend directory:

```bash
cd frontend
```

Install the frontend requirements:

```bash
pip install -r requirements.txt
```

Create a `.env` file based on `.env.example`:

```env
API_BASE_URL=http://localhost:8000
```

Run Streamlit:

```bash
streamlit run app.py
```

The frontend will normally be available at:

```text
http://localhost:8501
```

The frontend communicates with the FastAPI backend using the URL stored in the `API_BASE_URL` environment variable.

## Testing

The backend includes automated tests for:

* Health endpoint
* Successful query request
* Invalid query validation

Run the tests from the `backend` directory:

```bash
pytest
```

Expected result:

```text
3 passed
```

## End-to-End Usage

The complete application follows this flow:

```text
User Question
      ↓
Streamlit Frontend
      ↓
POST /query
      ↓
FastAPI Backend
      ↓
Chroma Similarity Search
      ↓
Top 2 Relevant Chunks
      ↓
Groq LLM
      ↓
Grounded Answer
      ↓
Answer + Sources
      ↓
Streamlit Frontend
```

Example question:

```text
What was the importance of the Nile River to Ancient Egypt?
```

The system retrieves relevant chunks from the document and generates a grounded answer with source references.

## Persisted Vector Store

The vector store is generated by the RAG notebook and persisted using Chroma.

The backend uses the persisted store located at:

```text
backend/data/vector_store/
```

The vector store is loaded when the FastAPI application starts rather than being recreated for every query.

## Security and GitHub

Sensitive and unnecessary files are excluded from the public repository.

The following files and directories should not be committed:

```text
.venv/
.env
__pycache__/
*.log
```

The real Groq API key must never be uploaded to GitHub.

Environment variable templates are provided using:

```text
.env.example
```

The raw document/corpus should also not be uploaded as an unnecessary raw corpus dump if excluded by the project requirements.

## Limitations

* The assistant can only answer questions supported by the provided document.
* Retrieval currently uses the top two chunks.
* The project uses a text-only RAG pipeline.

## Future Improvements

Possible future improvements include:

* Better retrieval and reranking
* Larger evaluation dataset
* More detailed citation handling
* Conversation memory
* Support for multiple documents
* Improved answer evaluation
* Optional image/document vision capabilities

## Author

Ancient Egypt RAG Assistant

Built as part of a RAG-powered Document Assistant project.
