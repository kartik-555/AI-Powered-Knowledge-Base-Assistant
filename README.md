# AI-Powered Knowledge Base Assistant

AI assistant capable of answering user queries based on a private knowledge base. The assistant uses OpenAI's API for natural language understanding and Retrieval-Augmented Generation (RAG) to fetch context-relevant information from indexed documents.

## Features

- Upload and process documents (PDF, DOCX, TXT)
- Index document content using FAISS for efficient similarity search
- Retrieve relevant context for user queries
- Generate answers using OpenAI's API

## Installation

### Prerequisites

- Python 3.8+
- Django 3.2+
- FAISS
- OpenAI API key

### Steps

1. **Clone the repository:**

   ```sh
   git clone https://github.com/your-username/AI-Powered-Knowledge-Base-Assistant.git
   cd AI-Powered-Knowledge-Base-Assistant
   ```

2. **Create a virtual environment:**

   ```sh
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

3. **Install dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

4. **Run database migrations:**

   ```sh
   python manage.py migrate
   ```

5. **Start the development server:**

   ```sh
   python manage.py runserver
   ```

### Usage

#### Uploading Documents

1. Navigate to the document upload endpoint (`/api/upload/`).
2. Upload a PDF, DOCX, or TXT file.
3. The document will be processed, and its content will be indexed for similarity search.

#### Querying the Knowledge Base

1. Navigate to the query endpoint (`/api/query/`).
2. Enter your query.
3. The assistant will retrieve relevant context from the indexed documents and generate an answer using OpenAI's API.

## Project Structure

- `assistant/`: Contains the main application code.
  - `models.py`: Defines the `Document` and `Embedding` models.
  - `serializers.py`: Defines the serializers for file upload and query handling.
  - `views.py`: Contains the views for handling file uploads and queries.
  - `utils.py`: Contains utility functions for processing files, generating embeddings, and retrieving context.
- `knowledgebase/`: Contains the project settings and URLs.
- `requirements.txt`: Lists the project dependencies.

## How It Works

### Document Upload and Processing

1. **File Upload**: Users can upload PDF, DOCX, or TXT files.
2. **Text Extraction**: The uploaded file is processed to extract text content.
3. **Text Chunking**: The extracted text is split into chunks for indexing.
4. **Embedding Generation**: Each chunk is converted into an embedding using OpenAI's API.
5. **Indexing**: The embeddings are indexed using FAISS for efficient similarity search.

### Query Handling

1. **Query Submission**: Users submit a query to the assistant.
2. **Context Retrieval**: The assistant retrieves relevant context from the indexed documents using FAISS.
3. **Answer Generation**: The retrieved context is used to generate an answer using OpenAI's API.

## Acknowledgements

- [OpenAI](https://openai.com/) for providing the API for natural language understanding.
- [FAISS](https://github.com/facebookresearch/faiss) for efficient similarity search.
- [Django](https://www.djangoproject.com/) for the web framework.
- [drf-yasg](https://github.com/axnsan12/drf-yasg) for generating Swagger documentation.
