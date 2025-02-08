import streamlit as st
from io import BytesIO
from PIL import Image

def convert_image_to_bytes(image):
    buf = BytesIO()
    image.save(buf, format="PNG")
    return buf.getvalue()

def download_image_button(processed_image):
    # Convert the processed image to bytes
    image_bytes = convert_image_to_bytes(processed_image)

    # Initialize session state to store the image bytes
    if "image_bytes" not in st.session_state:
        st.session_state.image_bytes = image_bytes

    # Download button
    if st.download_button(
        label="Download Processed Image",
        data=st.session_state.image_bytes,
        file_name="processed_image.png",
        mime="image/png",
    ):
        st.success("Image is ready for download!")