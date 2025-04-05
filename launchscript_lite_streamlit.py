
import streamlit as st
import requests

st.set_page_config(page_title="LaunchScript Lite", layout="centered")

st.title("🚀 LaunchScript Lite")
st.subheader("Turn your ideas into content with AI — instantly.")

# This model is open for public use (no token required)
API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"

def query_model(prompt):
    response = requests.post(API_URL, json={"inputs": prompt})
    try:
        return response.json()[0]["generated_text"]
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

def generate_all(prompt):
    return {
        "🧵 Twitter Thread": query_model(f"Write a 5-tweet thread for solo creators about: {prompt}"),
        "💼 LinkedIn Post": query_model(f"Write a short professional LinkedIn post about: {prompt}"),
        "🎬 YouTube Script": query_model(f"Write a 60-second YouTube script for: {prompt}"),
        "🎯 Hook Ideas": query_model(f"Write 3 catchy titles for a post about: {prompt}")
    }

with st.form("content_form"):
    user_prompt = st.text_area("💡 What's your idea or topic?", height=100)
    submitted = st.form_submit_button("Generate Content")

if submitted and user_prompt:
    with st.spinner("Generating content..."):
        outputs = generate_all(user_prompt)
    for label, content in outputs.items():
        st.markdown(f"### {label}")
        st.write(content)
        st.markdown("---")
