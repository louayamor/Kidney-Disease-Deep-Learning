import streamlit as st
import requests
import base64
from PIL import Image
import io

API_URL = "http://localhost:8089/predict"

def encode_image(file_bytes: bytes) -> str:
    return base64.b64encode(file_bytes).decode('utf-8')

def predict_image(encoded_image: str) -> dict:
    response = requests.post(API_URL, json={"image": encoded_image})
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"❌ Server Error: {response.status_code}")
        return None

def main():
    st.set_page_config(page_title="Kidney Disease Predictor", page_icon="🩺", layout="centered")
    st.title("🩺 Kidney Disease Prediction App")
    st.markdown("Upload a medical image and get an instant prediction!")

    uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        file_bytes = uploaded_file.read()
        image = Image.open(io.BytesIO(file_bytes))
        st.image(image, caption='Uploaded Image', use_column_width=True)
        encoded_image = encode_image(file_bytes)

        if st.button('Predict'):
            with st.spinner('🔄 Sending image to model and predicting...'):
                try:
                    result = predict_image(encoded_image)
                    if result:
                        st.success(f"✅ Prediction Result: **{result}**")
                except Exception as e:
                    st.error(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    main()
