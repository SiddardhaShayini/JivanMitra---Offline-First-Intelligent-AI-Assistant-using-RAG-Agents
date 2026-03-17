from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os

PDF_DIR = "data/raw_pdfs"
DB_DIR = "embeddings/faiss_index"

documents = []

for file in os.listdir(PDF_DIR):
    if file.endswith(".pdf"):
        file_path = os.path.join(PDF_DIR, file)
        try:
            loader = PyPDFLoader(file_path)
            docs = loader.load()
            documents.extend(docs)
            print(f"✅ Loaded: {file}")
        except Exception as e:
            print(f"⚠️ Skipped {file} due to error: {e}")

print(f"\nTotal loaded documents: {len(documents)}")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = text_splitter.split_documents(documents)
print(f"Total chunks created: {len(chunks)}")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = FAISS.from_documents(chunks, embeddings)
vectorstore.save_local(DB_DIR)

print("\n🎉 Vector database created successfully")
