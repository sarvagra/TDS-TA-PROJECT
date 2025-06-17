# 🧠 TDS Virtual TA (Teaching Assistant)

A FastAPI backend that answers academic questions using vector search with Jina embeddings and GPT models.

---

## 🔧 Tech Stack

- **FastAPI** – Web API framework
- **ChromaDB** – Vector database
- **Jina AI** – For text embeddings (768-dim)
- **OpenAI GPT** – LLMs for final response
- **Python 3.9+**

---

## 🚀 Features

- 🔍 Vector search with top 5 context-relevant chunks
- 🤖 GPT-based answer generation
- 📎 Optional image field (base64, future use)
- 🔗 Custom link generator

---

## 📁 Project Structure
```
project/
├── app.py # FastAPI app
├── chromadb_store/ # Chroma vector DB
├── .env # API keys
├── requirements.txt # Dependencies
└── README.md # You're here!
```

---

## ⚙️ Setup

### 1. Clone the repo

```bash
git clone https://github.com/your-username/tds-virtual-ta.git
cd tds-virtual-ta
```
### 2. Install the dpendencies
```
pip install -r requirements.txt

```
### 3. Set your API key
```
OPENAI_API_KEY=your_openai_api_key_here
```
### 4. Run the server
```
uvicorn app:app --reload
```
---
## 📮 API Reference
- Request Body:
```
{
  "question": "your query",
  "image": "base 64 image"
}
```

- Response:
```
{
  "answer": "Overfitting occurs when...",
  "links": [
    {
      "url": "https://discourse.onlinedegree.iitm.ac.in/...",
      "text": "Discussion on overfitting"
    }
  ]
}
```

- cURL example:
```
curl -X POST "http://127.0.0.1:8000/api/" \
  -H "Content-Type: application/json" \
  -d '{"question": "Explain entropy in ID3 algorithm", "image": ""}'
```
---
## 🛠 Troubleshooting

- **Chroma errors** → Ensure the database folder `chromadb_store` exists and has the correct embeddings.
- **OpenAI errors** → Check your `.env` file for the correct API key.
- **Embedding mismatch** → Use the same embedding model during indexing and querying (`Jina` = 768-dim).

---

## 📝 To-Do

- [ ] Add OCR support for images
- [ ] Integrate frontend (React/Svelte)
- [ ] Contextual link extraction
- [ ] Add tests and CI/CD

---

## 📜 License

MIT License – free for personal and academic use.

---

## 🤝 Contributing

Feel free to submit a PR or raise issues. Open to feedback and ideas!


