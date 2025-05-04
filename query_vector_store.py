from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# Embedding modeli
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Veritabanını yükle (pickle güvenliği için flag gerekiyor)
vectorstore = FAISS.load_local(
    "embeddings/faiss_db",
    embedding_model,
    allow_dangerous_deserialization=True
)

# Kullanıcıdan sorgu al
query = input("Sorgunuz: ")

# Benzer dokümanları getir
docs = vectorstore.similarity_search(query, k=3)

print("\n🔍 En alakalı sonuçlar:")
for i, doc in enumerate(docs, 1):
    print(f"\n[{i}] {doc.page_content}")
