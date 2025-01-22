# assistant/utils.py
import openai
from django.conf import settings
from docx import Document as DocxDocument
import os
import pdfplumber
from .models import Document, Embedding
import faiss
import numpy as np
from transformers import AutoTokenizer,AutoModel,AutoModelForCausalLM

# openai.api_key = settings.OPENAI_API_KEY
# dimension = 1536  # Embedding size for OpenAI
dimension = 768  # Embedding size for OpenAI
index = faiss.IndexFlatL2(dimension)  # FAISS index for similarity search

tokenizer_chat = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf")
model_chat = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-chat-hf")
tokenizer_embed = AutoTokenizer.from_pretrained("nvidia/NV-Embed-v2", trust_remote_code=True)
model_embed = AutoModel.from_pretrained("nvidia/NV-Embed-v2", trust_remote_code=True)

# def generate_answer_from_openai(query, context):
#     response = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt=f"Given the context: {context}\nAnswer the following query: {query}",
#         max_tokens=150
#     )
#     return response.choices[0].text.strip()

def generate_answer_from_llama(query, context):
    
    # Combine the context and query
    input_text = f"Given the context: {context}\nAnswer the following query: {query}"
    
    # Tokenize the input text
    inputs = tokenizer_chat(input_text, return_tensors="pt")
    
    # Generate the response
    outputs = model_chat.generate(**inputs, max_length=150)
    
    # Decode the response
    response = tokenizer_chat.decode(outputs[0], skip_special_tokens=True)
    
    return response.strip()


def retrieve_context(query):
    query_vector = embed_text_hg(query)
    
    k = 5  
    distances, indices = index.search(np.array([query_vector]), k)

    context_chunks = []
    for idx in indices[0]:
        if idx != -1:  
            embedding = Embedding.objects.get(id=idx)
            context_chunks.append(embedding.chunk)
    
    context = " ".join(context_chunks)
    return context



# def embed_text(text):
#     response = openai.embeddings.create(
#         model="text-embedding-ada-002",
#         input=text
#     )
#     return np.array(response['data'][0]['embedding'], dtype=np.float32)

def embed_text_hg(text):
    # Tokenize the input text
    inputs = tokenizer_embed(text, return_tensors="pt")
    # Get the embeddings from the model
    outputs = model_embed(**inputs)
    # Return the embeddings
    return outputs.last_hidden_state

def process_file(file):
    """Extract text from files (PDF, DOCX, TXT)."""
    ext = file.name.split('.')[-1].lower()
    text = ""

    if ext == "pdf":
        with pdfplumber.open(file) as pdf:
            text = "\n".join([page.extract_text() for page in pdf.pages])
    elif ext == "docx":
        doc = DocxDocument(file)
        text = "\n".join([para.text for para in doc.paragraphs])
    elif ext == "txt":
        text = file.read().decode('utf-8')
    
    print(text)
    return text
    
def save_file(file):
    upload_dir = settings.MEDIA_ROOT / 'uploads'
    os.makedirs(upload_dir, exist_ok=True)
    
    file_path = os.path.join(upload_dir, file.name)
    with open(file_path, 'wb') as f:
        for chunk in file.chunks():
            f.write(chunk)

    text = process_file(file)
    
    doc = Document.objects.create(name=file.name, file=file)
    
    chunks = [text[i:i + 200] for i in range(0, len(text), 200)] # created chunks of 500 characters
    
    for chunk in chunks:
        vector = embed_text_hg(chunk)
        # vector = embed_text(chunk)
        Embedding.objects.create(document=doc, chunk=chunk, vector=vector.tobytes())
        index.add(np.array([vector]))

    return f"uploaded_files/{file.name}"
