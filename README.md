# GenAI-Powered Assessment Recommender System

A modular Retrieval-Augmented Generation (RAG) pipeline designed to map recruiter hiring queries and long job descriptions (JDs) to relevant individual SHL assessments.

## Overview

The system leverages a modular architecture to handle natural language queries, balancing technical, behavioral, and competency-based assessments while respecting practical constraints like duration and adaptivity.

### Key Features

* **Intelligent Query Understanding**: Uses structured LLM prompts via the Groq API to extract intent, seniority, and skills reliably, replacing lossy regex normalization.
* **High-Performance Vector Retrieval**: Utilizes Pinecone for efficient indexing, achieving a significant retrieval accuracy improvement over initial FAISS implementations.
* **Rule-Aware Re-ranking**: Applies a weighted re-ranking layer based on lexical title matching, URL keywords, and duration constraints to ensure practical relevance.
* **Comprehensive Data Ingestion**: Includes a custom crawler to scrape and structure metadata (URL, Remote Testing, Adaptive/IRT, Type, Duration) from the SHL Product Catalogue.
<img width="763" height="405" alt="image" src="https://github.com/user-attachments/assets/6888070f-5c68-44ac-9602-6321a340f0c1" />

## Tech Stack

* **Framework**: FastAPI
* **Embeddings**: Hugging Face Hub (`sentence-transformers/all-MiniLM-L6-v2`)
* **Vector Database**: Pinecone
* **LLM API**: Groq (for query understanding)
* **Scraping**: BeautifulSoup & Requests

## Installation & Setup

### 1. Prerequisites

* Python 3.9+
* A Pinecone API Key
* A Hugging Face API Token
* A Groq API Key

### 2. Clone the Repository
```bash
git clone https://github.com/rishabh-108272/genai-assessment-recommender-system
cd genai-recommender-system
```

### 3. Setup Virtual Environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Environment Variables

Create a `.env` file in the root directory and add your credentials:
```env
PINECONE_API_KEY=your_pinecone_key
HF_API_KEY=your_huggingface_key
GROQ_API_KEY=your_groq_key
```

## Running the Project

### Local Development

Start the FastAPI server using Uvicorn:
```bash
uvicorn api.backend:app --reload
```

The API will be available at `http://127.0.0.1:8000`. You can access the interactive Swagger documentation at `http://127.0.0.1:8000/docs`.

### API Endpoints

* **Health Check**: `GET /health` — Verifies server status.
* **Recommendation**: `POST /recommend` — Submit a query or JD text to receive top-K assessments.

## Evaluation Results

The system is evaluated using Mean Recall@10.

* **Initial Recall (FAISS)**: ~1.16%
* **Improved Recall (Pinecone)**: ~50% increase
* **Final Recall (Fine-tuned Re-ranking)**: ~60%
