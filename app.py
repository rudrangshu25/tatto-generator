import streamlit as st
from PIL import Image
import requests
from io import BytesIO
from dotenv import load_dotenv
import os
from tattoo_generator import extract_tattoo_symbols  


load_dotenv()
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

def generate_image_from_prompt(prompt):
    API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"
    }
    payload = {
        "inputs": prompt,
        "options": {"wait_for_model": True}
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        return None, f"{response.status_code} - {response.text}"

    if "image" not in response.headers.get("Content-Type", ""):
        return None, "Response was not an image."

    try:
        image = Image.open(BytesIO(response.content))
        return image, None
    except Exception as e:
        return None, f"Image decode error: {str(e)}"


st.set_page_config(page_title="AI Tattoo Designer", layout="centered")
st.title(" AI Tattoo Designer")
st.markdown("Describe your life story or experiences.")


user_input = st.text_area("Tell your story:", height=200, placeholder="E.g., I overcame childhood struggles and found strength in solitude...")

generate = st.button("Generate Tattoo Design")

if generate and user_input.strip():
    with st.spinner("Generating tattoo design... "):
        
        result = extract_tattoo_symbols(user_input)
        symbols = result["Matched Symbols"]

        if symbols:
            prompt = f"Minimal black ink tattoo of {', '.join(symbols)}, line art, white background"
            st.success("Tattoo Prompt Generated!")
            st.markdown(f"**Prompt:** `{prompt}`")

            
            image, error = generate_image_from_prompt(prompt)

            if error:
                st.error(f"Failed to generate image: {error}")
            else:
                st.image(image, caption="AI-generated Tattoo", use_container_width=True)
        else:
            st.warning("No matching symbols found. Try a longer or more descriptive story.")
elif generate:
    st.warning("Please write something about your story first.")

st.markdown("---")
st.markdown("Powered by NLP + Stable Diffusion + Hugging Face Inference API")
