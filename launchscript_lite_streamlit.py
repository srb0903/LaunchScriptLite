import streamlit as st
import requests
import re

st.set_page_config(page_title="LaunchScript Lite", layout="centered")

st.title("🚀 LaunchScript Lite")
st.subheader("Turn your ideas into content with AI — no setup needed.")

# Using Falcon-7B Instruct for high-quality generation
API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
headers = {"Authorization": f"Bearer {st.secrets['HUGGINGFACE_TOKEN']}"}

def clean_output(text):
    # Remove LLM disclaimers
    text = re.sub(r"(?i)as an ai language model.*?(\.|\n)", "", text)
    # Remove echoed prompts or brackets
    text = re.sub(r"(?i)(write|create|generate).*?:.*", "", text)
    return text.strip()

def format_twitter_thread(raw_text):
    tweets = re.split(r"\n|(?<=\d\.)\s", raw_text.strip())
    tweets = [tweet.strip(" -:\n") for tweet in tweets if tweet.strip()]
    return "\n\n".join([f"{i+1}. {t}" for i, t in enumerate(tweets[:5])])

def query_model(prompt):
    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
        if response.status_code != 200:
            return f"⚠️ Error: {response.status_code}"
        result = response.json()
        if isinstance(result, list) and "generated_text" in result[0]:
            return clean_output(result[0]["generated_text"])
        elif isinstance(result, dict) and "generated_text" in result:
            return clean_output(result["generated_text"])
        else:
            return "⚠️ The model responded but no text was returned. Try again."
    except Exception as e:
        return f"⚠️ Exception: {str(e)}"

def generate_all(prompt):
    outputs = {
        "🧵 Twitter Thread": query_model(
            f"Write a Twitter thread with exactly 5 tweets. Each tweet should be short, punchy, and helpful for solo creators about: {prompt}. Number them clearly, and separate each tweet with line breaks. Use emojis and 1-2 relevant hashtags. Do NOT restate the prompt."
        ),
        "💼 LinkedIn Post": query_model(
            f"Write a personal and professional LinkedIn post for solo entrepreneurs. It should feel human, reflective, and helpful about this topic: {prompt}. Avoid saying 'as an AI model' and do not repeat the prompt."
        ),
        "🎮 YouTube Script": query_model(
            f"Write a 60-second YouTube video script for solo creators. Structure it like this: Intro (hook the viewer), Point 1 (personal example), Point 2 (practical tip), Point 3 (creative twist), and a clear Call to Action. Keep it conversational and natural. Topic: {prompt}. Do NOT restate the prompt or mention AI."
        ),
        "🎯 Hook Ideas": query_model(
            f"Write 3 short, catchy headlines that could go viral with content creators. Use curiosity, emotional words, or strong benefits. Topic: {prompt}."
        )
    }
    if "🧵 Twitter Thread" in outputs:
        outputs["🧵 Twitter Thread"] = format_twitter_thread(outputs["🧵 Twitter Thread"])
    return outputs

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
