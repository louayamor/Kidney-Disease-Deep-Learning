import streamlit as st
import requests
import base64
from PIL import Image
import io

API_URL = "https://kidney-disease-deep-learning.onrender.com/predict"

def encode_image(file_bytes: bytes) -> str:
    return base64.b64encode(file_bytes).decode('utf-8')

def predict_image(encoded_image: str) -> dict:
    headers = {"Content-Type": "application/json"}
    response = requests.post(API_URL, json={"image": encoded_image}, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"❌ Server Error: {response.status_code}")
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
                except Exception as e:
                    st.error(f"❌ Connection Error: {e}")

    else:
        st.markdown("<br>", unsafe_allow_html=True)
        st.info('⬆️ Upload an image file to start.', icon="ℹ️")

if __name__ == "__main__":
    main()
