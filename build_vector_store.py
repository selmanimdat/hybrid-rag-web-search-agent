import os
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from sentence_transformers import SentenceTransformer
from langchain.embeddings import HuggingFaceEmbeddings

# Belgeleri yükle
loader = TextLoader("/home/selman/Desktop/university/Humanoid_robot/documnets/ornek")
docs = loader.load()

# Metni parçalara ayır
splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)

# Embedding modeli yükle
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# FAISS vektör veritabanı oluştur
vectorstore = FAISS.from_documents(chunks, embedding_model)

# Vektör veritabanını kaydet
vectorstore.save_local("embeddings/faiss_db")
print("FAISS veritabanı oluşturuldu ve kaydedildi.")
