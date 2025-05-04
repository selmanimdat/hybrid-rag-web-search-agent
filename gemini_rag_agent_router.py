import os
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from duckduckgo_search import DDGS

# 1. Gemini'yi yapılandır
genai.configure(api_key="AIzaSyBIDWAjdXbX0uBmhdUpkjNL18LW0N_aVi0")
model = genai.GenerativeModel("gemini-2.0-flash")

# 2. FAISS vektör veritabanı + RAG
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = FAISS.load_local(
    "embeddings/faiss_db", embedding_model, allow_dangerous_deserialization=True
)
retriever = vectorstore.as_retriever()

def query_rag(question):
    docs = retriever.get_relevant_documents(question)
    if docs:
        context = "\n".join([d.page_content for d in docs])
        prompt = f"Aşağıdaki bağlama göre soruyu cevapla:\n\n{context}\n\nSoru: {question}"
        return model.generate_content(prompt).text
    return "Vektör veritabanında uygun bilgi bulunamadı."

# 3. Tavily Web Search Tool
def ddg_search(question):
    with DDGS() as ddgs:
        results = ddgs.text(question, max_results=3)
        context = "\n".join([r["body"] for r in results])
        prompt = f"Aşağıdaki arama sonuçlarına göre soruyu yanıtla:\n\n{context}\n\nSoru: {question}"
        return model.generate_content(prompt).text
    
def query_web(question):
    return ddg_search(question)


# 4. Agent Router (karar verir)
def route_query(question):
    decision_prompt = f"""Soru: "{question}"\nBu soruda güncel bilgi mi aranıyor yoksa daha çok belge tabanlı bir bilgi mi?
    
Eğer belge tabanlı ise "RAG", güncel veya internetten araştırılması gereken bir şeyse "WEB" yaz."""
    decision = model.generate_content(decision_prompt).text.strip().upper()
    
    if "WEB" in decision:
        return query_web(question)
    else:
        return query_rag(question)

# 5. Terminal uygulaması
if __name__ == "__main__":
    while True:
        question = input("\n🔍 Soru (çıkmak için q): ")
        if question.lower() == "q":
            break
        answer = route_query(question)
        print("\n📌 Cevap:\n", answer)
