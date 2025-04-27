import streamlit as st
import requests
import base64
import json
from PIL import Image
import io

# API_URL = "https://kidney-disease-deep-learning.onrender.com/predict"
API_URL = "http://localhost:8089/predict"

def encode_image(file_bytes: bytes) -> str:
    return base64.b64encode(file_bytes).decode('utf-8')

def predict_image(encoded_image: str) -> dict:
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(API_URL, json={"image": encoded_image}, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Request Error: {e}")
        return None
    except Exception as e:
        st.error(f"❌ Unexpected Error: {e}")
        return None

def load_scores(filepath="scores.json"):
    try:
        with open(filepath, "r") as f:
            scores = json.load(f)
        return scores
    except FileNotFoundError:
        st.warning("⚠️ Scores file not found.", icon="⚠️")
        return None

def main():
    st.set_page_config(page_title="🩺 Kidney Disease Predictor", page_icon="🩺", layout="centered")

    with st.container():
        st.markdown(
            "<h1 style='text-align: center; color: #e77a40;'>🩺 Kidney Disease Prediction App</h1>",
            unsafe_allow_html=True
        )

        st.markdown(
            "<p style='text-align: center; font-size: 18px;'>"
            "Upload a medical scan and get a fast prediction!"
            "</p>",
            unsafe_allow_html=True
        )

    uploaded_file = st.file_uploader(
        "Choose a medical image",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed"
    )

    if uploaded_file is not None:
        file_bytes = uploaded_file.read()
        image = Image.open(io.BytesIO(file_bytes))
        st.image(image, caption="🖼️ Uploaded Image", use_container_width=True)

        encoded_image = encode_image(file_bytes)

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button('🚀 Predict Now', use_container_width=True):
            with st.spinner('🔄 Predicting... Please wait...'):
                try:
                    result = predict_image(encoded_image)
                    if result:
                        st.success(f"✅ **Prediction Result:** {result}")

                        # --- Load and Display Scores ---
                        scores = load_scores()
                        if scores:
                            st.markdown("---")
                            st.subheader("📈 Model Performance")

                            col1, col2 = st.columns(2)
                            col1.metric(label="Accuracy", value=f"{scores['accuracy']*100:.2f}%")
                            col2.metric(label="Loss", value=f"{scores['loss']:.4f}")

                except Exception as e:
                    st.error(f"❌ Connection Error: {e}")

    else:
        st.markdown("<br>", unsafe_allow_html=True)
        st.info('⬆️ Upload an image file to start.', icon="ℹ️")

if __name__ == "__main__":
    main()
