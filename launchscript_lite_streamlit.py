import streamlit as st
import requests
import re

st.set_page_config(page_title="LaunchScript Lite", layout="centered")

st.title("🚀 LaunchScript Lite")
st.subheader("Turn your ideas into content with AI — no setup needed.")

# Updated to use Falcon-7B Instruct for higher quality content
API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
headers = {"Authorization": f"Bearer {st.secrets['HUGGINGFACE_TOKEN']}"}

def clean_output(text):
    # Remove LLM disclaimers
    text = re.sub(r"(?i)as an ai language model.*?(\.|\n)", "", text)
    # Remove prompt echoes
    text = re.sub(r"(?i)(write|generate).*?:.*", "", text)
    return text.strip()

def format_twitter_thread(raw_text):
    # Attempt to split by tweet number or newline
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
            f"Write a Twitter thread with exactly 5 tweets. Each tweet should be short, punchy, and helpful for solo creators about: {prompt}. Number them clearly, and separate each tweet with line breaks. Use emojis and 1-2 relevant hashtags where it makes sense. Do not restate the prompt."
        ),
        "💼 LinkedIn Post": query_model(
            f"Write a personal and professional LinkedIn post for solo entrepreneurs. It should feel human, reflective, and helpful about this topic: {prompt}. Avoid saying 'as an AI model' and do not repeat the prompt."
        ),
        "🎮 YouTube Script": query_model(
            f"Create a 60-second YouTube script with this structure: [Intro], [Point 1], [Point 2], [Point 3], [Call to Action]. Tone should be natural, energetic, and clear. Topic: {prompt}. Do not restate the prompt or mention AI."
        ),
        "🎯 Hook Ideas": query_model(
            f"Write 3 viral-style headlines that would hook a content creator. Make them short, curiosity-driven, and emotional. Topic: {prompt}."
        )
    }
    # Format the Twitter thread specifically
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
