from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import openai
import numpy as np
import streamlit as st
from medical_data import docs

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]  # Load API key from Streamlit secrets

# Initialize OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY,
                       base_url="https://openrouter.ai/api/v1",)

# 3. Embed documents with SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")
doc_embeddings = model.encode(docs)


def retrieve_context(query, top_k=2):
    query_embedding = model.encode([query])
    similarities = cosine_similarity(query_embedding, doc_embeddings)[0]
    top_indices = np.argsort(similarities)[-top_k:][::-1]
    return [docs[i] for i in top_indices]

# 5. Function to call OpenAI (explanation generation)


def generate_explanation(symptoms, context):
    prompt = f"""
    You are a helpful medical assistant. A user described their symptoms as: {symptoms}

    Here are relevant clinical insights:
    {chr(10).join(context)}

    Based on this, write an easy-to-understand explanation of what might be going on.
    Always include a disclaimer to consult a medical professional.
    """
    response = client.chat.completions.create(
        model="mistralai/mistral-7b-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return response.choices[0].message.content


# 🔍 Test with user input
st.title("💬 Tell Me About Your Symptoms")
user_input = st.text_input("Eg: I have chest pain and it gets worse when I breathe")

if user_input:
    context = retrieve_context(user_input)
    output = generate_explanation(user_input, context)
    st.write("🤖", output)
