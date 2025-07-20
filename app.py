from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama.llms import OllamaLLM
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.embeddings import HuggingFaceEmbeddings

model_path = r"D:\Project\ChatPDF\models\bge-base-en-v1.5"
embeddings = HuggingFaceEmbeddings(model_name=model_path)

pdfs_directory = 'pdfs/'

llm = OllamaLLM(model="mistral")

template = """ 
You are an assistant that answers questions. Using the following retrieved information, answer the user question. If you don't know answer, just say that you don't know. Use up to 3 sentences , keep it concise and to the point.

Question: {question}
Context: {context}
Answer:
"""
prompt = ChatPromptTemplate.from_template(template)

def upload_pdf(file_path):
    with open(pdfs_directory + file_path, "wb") as f:
        f.write(file_path.getbuffer())

def create_vector_store(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000, 
        chunk_overlap=200,
        add_start_index=True
    )

    chunked_docs = text_splitter.split_documents(documents)
    db = FAISS.from_documents(chunked_docs, embeddings)
    return db

def retrieve_docs(query, db, k=5):
    return db.similarity_search(query, k)

def question_pdf(question, db):
    # Retrieve relevant documents using similarity search
    documents = db.similarity_search(question, k=5)

    # Join content for context
    context = "\n".join([doc.page_content for doc in documents])
    
    chain = prompt | llm
    return chain.invoke({"question": question, "context": context})

def summarize_pdf(vector_store: FAISS):
    # Retrieve relevant chunks from the vector store
    docs = vector_store.similarity_search("Summarize this document", k=5)
    content = "\n".join([doc.page_content for doc in docs])

    # Build prompt
    summarize_template = """
    You are a helpful assistant. Provide a concise summary (4-6 bullet points) of the following document content:

    {content}

    Summary:
    """
    summarize_prompt = ChatPromptTemplate.from_template(summarize_template)

    # Chain prompt with LLM
    summarize_chain = summarize_prompt | llm

    # Invoke with content
    return summarize_chain.invoke({"content": content})