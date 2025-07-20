# 🧠 Chat with PDF (Streamlit)

A lightweight AI-powered app to **chat with PDF documents** using local embeddings and semantic search. Built with **Streamlit** and **LangChain**, optimized for privacy and offline use.

---
## 🚀 Features

- 📄 Upload and parse PDF documents
- 🔍 Local semantic search with FAISS + Sentence Transformers
- 💬 Ask questions and receive accurate answers
- 🧠 Optional LLM-based summarization
- 🎈 Clean and responsive Streamlit UI

---
## 📁 Project Structure
chat-with-pdf/
## 📁 Project Structure

- `app.py` – Backend logic using LangChain
- `ui.py` – Streamlit UI logic
- `model/` – SentenceTransformer model files
- `requirements.txt` – Project dependencies


---
## 🛠️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/chat-with-pdf.git
cd chat-with-pdf
```
### 2. Create and Activate a Virtual Environment
# For Windows
```bash
python -m venv venv
venv\Scripts\activate
```
# For macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Run the App
```bash
streamlit run ui.py
```
## 💡 How It Works

1. **Upload a PDF** via the UI.
2. The document is **parsed and chunked** using *LangChain's* text splitter.
3. **Embeddings are generated** using *SentenceTransformers*.
4. **FAISS indexes** the chunks for fast similarity search.
5. **Ask any question** — relevant chunks are retrieved and shown with answers.

## 🔐 Privacy First

This app runs **locally** — no documents or data leave your system. Ideal for **confidential** or **offline** use cases.
