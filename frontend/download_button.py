import streamlit as st
from io import BytesIO

def convert_image_to_bytes(image):
    buf = BytesIO()
    image.save(buf, format="PNG")
    return buf.getvalue()

def download_image_button(processed_image):
    image_bytes = convert_image_to_bytes(processed_image)               # Convert the processed image to bytes
    if st.download_button(                                              # Download button
        label       ="Download Processed Image",
        data        =image_bytes,
        file_name   ="processed_image.png",
        mime        ="image/png",
    ):
        st.success("Image is ready for download!")