import os
import base64
import streamlit as st
FONT_FOLDER = "utils/fonts"

def get_available_fonts():
    """Fetches available .ttf fonts from the font folder."""
    return [f.replace(".ttf", "") for f in os.listdir(FONT_FOLDER) if f.endswith(".ttf")]

def get_font_base64(font_name):
    """Reads the font file, converts it to Base64, and returns CSS."""
    font_filename = f"{font_name}.ttf"
    font_path = os.path.join(FONT_FOLDER, font_filename)
    if not os.path.exists(font_path):
        return None, f"Font file '{font_filename}' not found in '{FONT_FOLDER}'"

    with open(font_path, "rb") as f:
        font_base64 = base64.b64encode(f.read()).decode()
    # Generate CSS with Base64 font
    custom_css = f"""
    <style>
        @font-face {{
            font-family: 'CustomFont';
            src: url(data:font/ttf;base64,{font_base64}) format('truetype');
        }}
        .custom-text {{
            font-family: 'CustomFont', sans-serif;
            font-size: 24px;
        }}
    </style>
    """
    return custom_css, None

def display_font_preview(font_name):
    """Displays a preview of the selected font in Streamlit."""
    custom_css, error = get_font_base64(font_name)
    if error:
        st.error(error)
    else:
        st.markdown(custom_css, unsafe_allow_html=True)
        st.markdown('<p class="custom-text">Font Preview: Hello, World!</p>', unsafe_allow_html=True)
