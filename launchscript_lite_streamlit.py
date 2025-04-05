import streamlit as st
import requests

st.set_page_config(page_title="LaunchScript Lite", layout="centered")

st.title("🚀 LaunchScript Lite")
st.subheader("Turn your ideas into content with AI — no setup needed.")

# New open model that supports anonymous usage reliably
API_URL = "https://api-inference.huggingface.co/models/mrm8488/t5-base-finetuned-common_gen"

def query_model(prompt):
    try:
        response = requests.post(API_URL, json={"inputs": prompt})
        result = response.json()
        if response.status_code == 200 and isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"]
        else:
            return f"⚠️ Error: {result.get('error', 'Unknown error')}"
    except Exception as e:
        return f"⚠️ Exception: {str(e)}"

def generate_all(prompt):
    return {
        "🧵 Twitter Thread": query_model(f"Generate a short Twitter thread about: {prompt}"),
        "💼 LinkedIn Post": query_model(f"Write a professional LinkedIn post about: {prompt}"),
        "🎮 YouTube Script": query_model(f"Write a YouTube script introduction for: {prompt}"),
        "🎯 Hook Ideas": query_model(f"List 3 catchy content titles for: {prompt}")
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
