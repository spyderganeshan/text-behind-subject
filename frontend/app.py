from PIL                    import Image
from loguru                 import logger
from download_button        import download_image_button
from font_preview          import get_available_fonts, display_font_preview
from text_position_preview  import text_position_preview
import sys
import os
import streamlit as st
import requests
import io
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

API_URL_GENERATE_DEPTH  = "http://127.0.0.1:8000/generate-layer/"
API_URL_APPLY_TEXT      = "http://127.0.0.1:8000/apply-text/"
available_fonts         = get_available_fonts()
########################################## model and image selection #################################
st.title("🔍 Test Behind Subject ")
st.write("Upload an image, select the model for processing.")
uploaded_file   = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])       # File uploader
model_selected  = st.selectbox(                                                             # Model selection
    "Select Model",
    ["Small", "Hybrid", "Large"],
    index=0
)
if 'process_complete' not in st.session_state:                                              # Initialize session state
    st.session_state.process_complete = False
      
if uploaded_file is not None:
    image       = Image.open(uploaded_file)
    img_width   = image.size[0]  
    img_height  = image.size[1]
    col1,col2   = st.columns(2)
    with col1:
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
    col1, col2      = st.columns(2)
    with col1:
        text        = st.text_input("Enter Text:")
    with col2:
        text_size   = st.number_input("Text Size:", min_value=10, max_value=2000, value=800, step=10)
    col1, col2      = st.columns(2)
    with col1:
        font_name   = st.selectbox("Select Font:", available_fonts.keys())
    with col2:
        st.write("")
        if font_name:
            st.write("")  # Adds spacing
            display_font_preview(font_name,available_fonts[font_name])
    col1, col2  = st.columns(2)
    with col1:
        text_transparency = st.slider("Select Transparency (%)", min_value=0, max_value=100, value=50)
        alpha   = int((text_transparency / 100) * 255)
    with col2:
        text_color      = st.color_picker("Text Color:", "#ff0000")
        text_color_rgba = tuple(int(text_color[i:i+2], 16) for i in (1, 3, 5))+(alpha,)                     # Convert transparency from 0-100 range to 0-255 range
    # print(font_name+available_fonts[font_name])
    position_x, position_y=text_position_preview(image, text, text_color, text_size,font_name+available_fonts[font_name],text_transparency)
    if st.button("Generate"):
        with st.spinner("Applying Text Overlay... ⏳"):
            data = {
                "text"          : text,
                "text_position" : (position_x, position_y),
                "text_size"     : text_size,
                "text_color"    : text_color_rgba,
                "font_name"     : font_name+available_fonts[font_name]
            }
            response = requests.post(API_URL_APPLY_TEXT,
                                     headers={"Content-Type": "application/json"}, 
                                     data   =json.dumps(data))
            logger.info(f"request sent to{API_URL_APPLY_TEXT}" )
            if response.status_code == 200:
                processed_image     = Image.open("./utils/image/output.png")
                st.image(processed_image, caption="Processed Image", use_container_width=True)
                download_image_button(processed_image)
            else:
                st.error("❌ Error updating text!")
