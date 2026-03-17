from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_classic.chains import RetrievalQA
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate

from rag.safety import detect_risk, emergency_message, safety_filter
from rag.prompts import ELDER_SAFE_PROMPT

DB_DIR = "embeddings/faiss_index"

# Embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Load vector DB
vectorstore = FAISS.load_local(
    DB_DIR,
    embeddings,
    allow_dangerous_deserialization=True
)

# OFFLINE LLM (Laptop-safe)
llm = OllamaLLM(
    model="phi3",
    temperature=0
)

# Elder-safe prompt
prompt = PromptTemplate(
    template=ELDER_SAFE_PROMPT +
    "\n\nContext:\n{context}\n\nQuestion:\n{question}\n\nAnswer:",
    input_variables=["context", "question"]
)

qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
    chain_type_kwargs={"prompt": prompt},
    return_source_documents=False
)

print("🧓 JivanMitra AI (OFFLINE & ELDER-SAFE) ready.\n")

while True:
    query = input("👤 You: ")

    if query.lower() in ["exit", "quit"]:
        break

    # 🚨 Risk detection
    if detect_risk(query):
        print("\n🤖 JivanMitra:\n", emergency_message(), "\n")
        continue

    result = qa.invoke({"query": query})
    safe_answer = safety_filter(result["result"])

    print("\n🤖 JivanMitra:", safe_answer, "\n")
