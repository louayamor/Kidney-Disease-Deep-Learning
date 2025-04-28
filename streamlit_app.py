import streamlit as st
import requests
import base64
import json
from PIL import Image
import io

# ========== App Constants ==========
APP_TITLE = "🩺 Kidney Disease Predictor"
APP_DESCRIPTION = "Upload a medical scan and get a fast prediction!"
PAGE_ICON = "🩺"
API_URL = "http://localhost:8089/predict"
SCORES_FILE = "scores.json"

LINKS = {
    "GitHub": {
        "url": "https://github.com/your-github-repo",
        "icon": "https://img.icons8.com/ios-glyphs/30/000000/github.png"
    },
    "DAGsHub": {
        "url": "https://dagshub.com/your-dagshub-repo",
        "icon": "https://img.icons8.com/external-tal-revivo-filled-tal-revivo/30/000000/external-dagshub-a-git-based-data-and-model-management-platform-logo-filled-tal-revivo.png"
    },
    "Render": {
        "url": "https://your-render-link.onrender.com",
        "icon": "https://img.icons8.com/ios-filled/30/000000/deployment.png"
    },
    "MLflow": {
        "url": "https://cdn-icons-png.flaticon.com/512/685/685887.png",
        "icon": "https://cdn-icons-png.flaticon.com/512/685/685887.png"  # update with your real MLflow link
    }
}

# ========== Helper Functions ==========
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

def load_scores(filepath=SCORES_FILE):
    try:
        with open(filepath, "r") as f:
            scores = json.load(f)
        return scores
    except FileNotFoundError:
        st.warning("⚠️ Scores file not found.", icon="⚠️")
        return None

def display_links():
    st.markdown(
        "<div style='text-align: center;'>"
        + "".join([
            f"<a href='{info['url']}' target='_blank' title='{name}'>"
            f"<img src='{info['icon']}' style='margin: 0px 15px;'/>"
            f"</a>"
            for name, info in LINKS.items()
        ])
        + "</div><br>",
        unsafe_allow_html=True
    )

# ========== Main App ==========
def main():
    # Set page config as the first Streamlit command
    st.set_page_config(page_title=APP_TITLE, page_icon=PAGE_ICON, layout="centered")

    # Set custom CSS styles for a fresh design
    st.markdown(
        """
        <style>
            body {
                background-color: #f3f4f6; /* Light gray background */
            }
            .title {
                color: #1e3a8a; /* Dark blue color for title */
                font-size: 36px;
                font-weight: bold;
            }
            .description {
                color: #1e3a8a;
                font-size: 18px;
                text-align: center;
            }
            .button {
                background-color: #fbbf24; /* Bright yellow */
                color: white;
                border-radius: 5px;
                padding: 12px 30px;
                font-size: 18px;
                font-weight: bold;
                margin-top: 10px;
                border: none;
            }
            .button:hover {
                background-color: #eab308; /* Hover effect */
            }
            .metric {
                font-size: 18px;
                color: #1e3a8a;
            }
            .metric-value {
                font-weight: bold;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    display_links()

    # Title and description in styled container
    with st.container():
        st.markdown(
            f"<h1 class='title'>{APP_TITLE}</h1>",
            unsafe_allow_html=True
        )

        st.markdown(
            f"<p class='description'>{APP_DESCRIPTION}</p>",
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

        if st.button('🚀 Predict Now', use_container_width=True, key="predict_button", help="Click to make a prediction"):
            with st.spinner('🔄 Predicting... Please wait...'):
                try:
                    result = predict_image(encoded_image)
                    if result:
                        st.success(f"✅ **Prediction Result:** {result}")

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
