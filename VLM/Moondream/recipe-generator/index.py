import streamlit as st
from openai import OpenAI
import moondream as md
from PIL import Image

# Load API key from Streamlit secrets
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY,
                base_url="https://openrouter.ai/api/v1",)

# Load Moondream model
model = md.vl(api_key=st.secrets["MOONDREAM_API_KEY"])

# Streamlit app
st.title("🥕 AI Recipe Generator from Your Fridge")
st.write("Upload a photo of your fridge, and AI will suggest a recipe!")

# File uploader
uploaded_file = st.file_uploader(
    "Upload a fridge photo", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Save uploaded file
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.read())

    # Step 1: Caption fridge contents with Moondream
    st.image(uploaded_file.name, caption="Uploaded Fridge", use_column_width=True)
    st.write("🔍 Analyzing fridge contents...")

    image = Image.open(uploaded_file)
    caption = model.caption(image)["caption"]
    st.success(f"Fridge contains: {caption}")

    # Step 2: Generate recipe using GPT
    st.write("👩‍🍳 Generating recipe...")

    prompt = f"Suggest a simple, healthy recipe using these items: {caption}. Keep it short and easy to follow."
    response = client.chat.completions.create(
        model="mistralai/mistral-7b-instruct",
        messages=[{"role": "user", "content": prompt}],
    )
    recipe = response.choices[0].message.content

    st.subheader("🍴 Recipe Idea")
    st.write(recipe)
