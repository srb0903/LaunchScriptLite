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
    tweets = [tweet.strip() for tweet in tweets if tweet.strip() and len(tweet) > 30]
    return "\n\n".join(tweets[:5]) if tweets else raw_text

def format_hooks(raw_text):
    hooks = re.findall(r"\d\.\s(.+?)(?=\n\d\.|\Z)", raw_text.strip(), re.DOTALL)
    cleaned = [h.strip(" .'\n") for h in hooks if len(h.strip()) > 20 and 'ask' not in h.lower() and 'repurpose' not in h.lower() and 'engage' not in h.lower()]
    return "\n".join(cleaned[:3]) if cleaned else raw_text

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
            f"You're a solo creator writing for Twitter. Write a compelling 5-part thread on this topic: {prompt}. The first tweet should grab attention. The next three should build insight or value. The fifth should be a takeaway or CTA. Each tweet must be numbered and formatted as if you're tweeting."
        ),
        "💼 LinkedIn Post": query_model(
            f"Write a personal and professional LinkedIn post for solo entrepreneurs. It should feel human, reflective, and helpful about this topic: {prompt}. Avoid saying 'as an AI model' and do not repeat the prompt."
        ),
        "🎮 YouTube Shorts Script": query_model(
            f"Write a fast-paced, conversational script for a YouTube Short (under 60 seconds) on the topic: {prompt}. Start with a hook, give 2-3 punchy value points, and end with a clear call to action. Do not mention AI."
        ),
        "🎯 Hook Ideas": query_model(
            f"You're a social media copywriter. Write 3 short, curiosity-driven headline hooks for: {prompt}. Make them emotional or intriguing. No explanations or tips, just the hook. Each under 80 characters. Format as: 1. ... 2. ... 3. ..."
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
