
# 🤖 Hybrid RAG + Web Search Agent for Humanoid Robot

## 🧠 Project Overview

**Hybrid RAG + Web Search Agent for Humanoid Robot** is an advanced AI-powered agent system designed to be the software brain of a humanoid robot. It enables users to interact via voice through a web interface, combining real-time internet search and local document retrieval for intelligent, natural conversations.

The system dynamically decides whether to use a **Retrieval-Augmented Generation (RAG)** pipeline or **real-time web search** based on the question's context. It leverages **Gemini LLM (Google Generative AI)** for natural language understanding and response generation, and uses **gTTS** to convert answers into spoken audio.

---

## ✨ Key Features

- **Context-Aware Routing**: Automatically switches between RAG and Web Search using a prompt-based decision engine powered by Gemini.
- **FAISS Vector Database**: Stores 800+ embedded documents for fast, semantic retrieval.
- **Real-Time Web Search**: Uses DuckDuckGo API for up-to-date answers.
- **Voice Interaction**: Converts user speech to text using SpeechRecognition and speaks responses using gTTS.
- **User-Friendly Web Interface**: Built with Flask, accessible via browser for seamless interaction.

---

## 📁 Project Structure

```text
├── app.py                      # Main Flask app
├── gemini_rag_agent_router.py  # Core agent decision logic
├── build_vector_store.py       # Script to build FAISS vector store
├── query_vector_store.py       # Query engine for vector store
├── rag_utils.py                # Helper functions for RAG
├── speak.py                    # Handles speech synthesis
├── embeddings/                 # Sentence embeddings
├── documnets/                  # Source documents
├── templates/                  # HTML templates
├── static/                     # JS, CSS, and assets
├── pyproject.toml              # Python project metadata
├── requirements_ai_rag.txt     # Required Python packages
└── README.md
