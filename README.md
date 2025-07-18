# HolyGrailDev AI MasterClass
This repository contains AI applications developed as part of the HolyGrailDev AI MasterClass

# Retrieval Augmented Generation(RAG)
### Setup Instructions

**Create and activate virtual environment**
- create env: `python -m venv venv`
- activate env: `source venv/bin/activate`

**Install dependencies**
- `pip install -r requirements.txt`

**Save current dependencies (when adding new packages)**
- `pip freeze > requirements.txt`

⚠️ NB: streamlit cloud already comes with most of the packages so just add the packages that are not included in the cloud manually, no need to add the versions. it takes care of that.

**Run the applications**
`streamlit run app.py`


## Projects
1. **Customer Reviews Bot**
- Description: A RAG system for analyzing customer reviews
- Technologies: LangChain, HuggingFace Embeddings, OpenRouter
- Deployment: https://customer-review-bot.streamlit.app/


2. **Symptom Checker**
- Description: Medical assistant that retrieves relevant medical information based on symptoms
- Technologies: SentenceTransformer, OpenAI/OpenRouter
- Deployment: https://symptom-checker-hgd.streamlit.app/