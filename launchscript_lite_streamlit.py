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
    text = re.sub(r"(?i)as an ai language model.*?(\.|\n)", "", text)
    text = re.sub(r"(?i)(write|create|generate).*?:.*", "", text)
    text = re.sub(r"<.*?>", "", text)  # remove any HTML tags like <strong>
    text = text.replace('"', '').replace("'", '').strip()
    return text

def format_twitter_thread(raw_text):
    tweets = re.findall(r"(?:^|\n)(\d\.\s?.+?)(?=\n\d\.|\Z)", raw_text.strip(), re.DOTALL)
    tweets = [tweet.strip() for tweet in tweets if tweet.strip()]
    return "\n\n".join(tweets[:5])

def format_hooks(raw_text):
    hooks = re.split(r"\n|\d\.\s?", raw_text.strip())
    cleaned = [re.sub(r"<.*?>", "", h).strip(" .'\n") for h in hooks if h.strip()]
    return "\n".join(cleaned[:3])

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
            f"Write a Twitter thread with 5 tweets that explains this topic: '{prompt}'. The first tweet should hook attention using the topic naturally. The rest should add value, build interest, and end with a takeaway or CTA. Number them 1-5 and limit to 280 characters each."
        ),
        "💼 LinkedIn Post": query_model(
            f"Write a personal and professional LinkedIn post for solo entrepreneurs. It should feel human, reflective, and helpful about this topic: {prompt}. Avoid saying 'as an AI model' and do not repeat the prompt."
        ),
        "🎮 YouTube Shorts Script": query_model(
            f"Write a fast-paced, conversational script for a YouTube Short (under 60 seconds) on the topic: {prompt}. Start with a hook, give 2-3 punchy value points, and end with a clear call to action. Do not mention AI."
        ),
        "🎯 Hook Ideas": query_model(
            f"Write 3 viral-style content hooks for a social post about: {prompt}. Keep them curiosity-driven, under 80 characters, and avoid any HTML or formatting tags."
        )
    }
    if "🧵 Twitter Thread" in outputs:
        outputs["🧵 Twitter Thread"] = format_twitter_thread(outputs["🧵 Twitter Thread"])
    if "🎯 Hook Ideas" in outputs:
        outputs["🎯 Hook Ideas"] = format_hooks(outputs["🎯 Hook Ideas"])
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
