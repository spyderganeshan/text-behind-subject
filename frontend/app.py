from PIL         import Image
from loguru      import logger
import sys
import os
from download_button import download_image_button
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from helper.Helper import Helper
import streamlit as st
import requests

import io
import json
API_URL_GENERATE_DEPTH = "http://127.0.0.1:8000/generate-layer/"
API_URL_APPLY_TEXT = "http://127.0.0.1:8000/apply-text/"
my_helper = Helper()
available_fonts = my_helper.get_font_names()
########################################## modela and image selection #################################
st.title("🔍 Text behind image ")
st.write("Upload an image, select the model for processing.")
uploaded_file   = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])       # File uploader
model_selected  = st.selectbox(                                                             # Model selection
    "Select Depth Estimation Model",
    ["Small", "Hybrid", "Large"],
    index=0
)
if 'process_complete' not in st.session_state:                                              # Initialize session state
    st.session_state.process_complete = False
if uploaded_file is not None:
    image       = Image.open(uploaded_file)
    img_width   = image.size[0]  
    img_height  = image.size[1]
    st.image(image, caption="Uploaded Image", use_container_width=True)
    if st.button("Process Image"):
        with st.spinner("Computing Layers... ⏳"):
            img_bytes   = io.BytesIO()
            image.save(img_bytes, format="PNG")
            img_bytes   = img_bytes.getvalue()
            response    = requests.post(
                API_URL_GENERATE_DEPTH,
                files   ={"file": ("image.png", img_bytes, "image/png")},
                data    ={"model_name": model_selected}
            )
            logger.info(f"request sent to {API_URL_GENERATE_DEPTH} ")
            if response.status_code == 200:
                st.success("✅  processing completed")
                st.session_state.process_complete = True
            else:
                st.error("❌ processing failed")

######################################### Text customization ##########################################
if st.session_state.process_complete:
    text        = st.text_input("Enter Text:")
    position_x  = st.slider("X position", 0, img_width, img_width // 2)
    position_y  = st.slider("Y position", 0, img_height, img_height // 2)
    text_size   = st.number_input("Font Size:", min_value=10, max_value=1000, value=800, step=10)
    col1, col2 = st.columns(2)
    with col1:
        text_color  = st.color_picker("Font Color:", "#ff0000")
    with col2:
        text_transparency = st.slider("Select Transparency (%)", min_value=0, max_value=100, value=50)
    col1, col2 = st.columns(2)
    with col1:
        font_name = st.selectbox("Font Name:", available_fonts)

    if st.button("Generate"):
        with st.spinner("Applying Text Overlay... ⏳"):
            # Convert transparency from 0-100 range to 0-255 range
            alpha = int((text_transparency / 100) * 255)
            text_color_rgba = tuple(int(text_color[i:i+2], 16) for i in (1, 3, 5))+(alpha,)
            data = {
                "text"          : text,
                "text_position" : (position_x, position_y),
                "text_size"     : text_size,
                "text_color"    : text_color_rgba,
                "font_name"     : font_name
            }
            response = requests.post(API_URL_APPLY_TEXT,
                                     headers={"Content-Type": "application/json"}, 
                                     data   =json.dumps(data))
            logger.info("request sent to %s", API_URL_APPLY_TEXT)
            if response.status_code == 200:
                processed_image     = Image.open("./utils/image/output.png")
                st.image(processed_image, caption="Processed Image", use_container_width=True)
                download_image_button(processed_image)
            else:
                st.error("❌ Error updating text!")
