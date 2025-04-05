import streamlit as st
import requests

st.set_page_config(page_title="LaunchScript Lite", layout="centered")

st.title("🚀 LaunchScript Lite")
st.subheader("Turn your ideas into content with AI — no setup needed.")

# Using Falcon-7B Instruct for high-quality generation
API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
headers = {"Authorization": f"Bearer {st.secrets['HUGGINGFACE_TOKEN']}"}

def query_model(prompt):
    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
        if response.status_code != 200:
            return f"⚠️ Error: {response.status_code}"
        result = response.json()
        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"]
        elif isinstance(result, dict) and "generated_text" in result:
            return result["generated_text"]
        else:
            return "⚠️ The model responded but no text was returned. Try again."
    except Exception as e:
        return f"⚠️ Exception: {str(e)}"

def generate_all(prompt):
    return {
        "🧵 Twitter Thread": query_model(
            f"Write a Twitter thread of exactly 5 tweets. Each tweet should be numbered, clear, engaging, and offer value to solo creators about: {prompt}. Use emojis and hashtags naturally to increase reach."
        ),
        "💼 LinkedIn Post": query_model(
            f"Write a professional and personal LinkedIn post for solo entrepreneurs. The tone should be insightful, reflective, and inspiring. Base it on this topic: {prompt}."
        ),
        "🎮 YouTube Script": query_model(
            f"Write a short YouTube video script for a solo creator. The tone should be friendly, fast-paced, and authentic. Include an intro, 3 clear points with transitions, and a call to action. Topic: {prompt}."
        ),
        "🎯 Hook Ideas": query_model(
            f"Write 3 viral headline ideas optimized for content marketing. Make them catchy, emotional, and curiosity-driven. Topic: {prompt}."
        )
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
