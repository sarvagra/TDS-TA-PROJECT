from pydantic import BaseModel
import requests
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import base64
import pytesseract
import weaviate
from weaviate.classes.init import Auth

OPENAI_API_KEY="eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjI0ZjIwMDQ5MjJAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.CfwJHvL6a0adtb7_Xu9in2i4Kg7BLXJTP6h3Qr_96D4"
WEAVIATE_URL = "zu1ijfg3rlyvlghm1kmzca.c0.asia-southeast1.gcp.weaviate.cloud"
WEAVIATE_API_KEY = "TVVoZjVjc0NranZVeEV2VV9UOC9ieTlUbEsxZmhOQiszd0xHczJrVW4xdkYzR28xdllRWmpaN3VRVEt3PV92MjAw"

# Connect to Weaviate
client = weaviate.connect_to_weaviate_cloud(
    cluster_url=WEAVIATE_URL,
    auth_credentials=Auth.api_key(WEAVIATE_API_KEY),
)
collection = client.collections.get("TextEmbedding")

# Setup FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

# Input schema
class Question(BaseModel):
    question: str
    image: str = None

# OCR function
def extract_text_from_base64(base64_image: str) -> str:
    image_data = base64.b64decode(base64_image)
    image = Image.open(io.BytesIO(image_data))
    text = pytesseract.image_to_string(image)
    return text

# Get embedding
def get_embedding(text: str):
    url = "https://aiproxy.sanand.workers.dev/openai/v1/embeddings"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {"model": "text-embedding-3-small", "input": [text]}
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["data"][0]["embedding"]

# Main endpoint
@app.post("/virtual-ta")
def virtual_ta(question: Question):
    # Combine question + OCR text if available
    if question.question and question.image:
        image_text = extract_text_from_base64(question.image)
        query_text = question.question + " " + image_text
    elif question.question:
        query_text = question.question
    elif question.image:
        query_text = extract_text_from_base64(question.image)
    else:
        raise ValueError("No question or image provided")

    # Get vector embedding
    embedding = get_embedding(query_text)

    # Search Weaviate
    results = collection.query.near_vector(
        near_vector=embedding,
        limit=5,
        return_metadata=["distance"]
    )

    docs = results.objects
    top_docs = [obj.properties.get("text", "") for obj in docs]
    top_metas = [obj.metadata for obj in docs]

    # Clean response
    lines = "\n".join(top_docs).split("\n")
    clean_lines = [
        line.strip()
        for line in lines
        if line.strip() and not line.strip().startswith(("###", "##", "#", "-", "*", "`", "```")) and len(line.strip()) > 15
    ]
    answer = " ".join(clean_lines[:3]) if clean_lines else "No clear answer found."

    # Extract source URLs
    links = []
    for doc, meta in zip(top_docs, top_metas):
        source = getattr(meta, "source", None)
        if source:
            text_line = doc.strip().split("\n")[0]
            links.append({
                "url": source,
                "text": text_line
            })

    return JSONResponse(content={
        "answer": answer,
        "links": links
    })
