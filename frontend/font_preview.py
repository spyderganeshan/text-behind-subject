import os
import base64
import streamlit as st

FONT_FOLDER = "utils/fonts"
FONT_FORMATS = {".ttf": "truetype", ".woff": "woff", ".woff2": "woff2", ".otf": "opentype"}

def get_available_fonts():
    """Fetches available fonts (all formats) from the font folder without extensions."""
    fonts = {}
    for font_file in os.listdir(FONT_FOLDER):
        name, ext = os.path.splitext(font_file)
        if ext in FONT_FORMATS:
            # fonts.setdefault(name, []).append(ext)
            fonts[name]=ext
    return fonts  # Returns a dict {font_name: [".ttf", ".woff", ...]}

def get_font_base64(font_name, font_ext):
    """Reads the font file, converts it to Base64, and returns CSS."""
    font_filename = f"{font_name}{font_ext}"
    font_path = os.path.join(FONT_FOLDER, font_filename)
    
    if not os.path.exists(font_path):
        return None, f"Font file '{font_filename}' not found in '{FONT_FOLDER}'"

    with open(font_path, "rb") as f:
        font_base64 = base64.b64encode(f.read()).decode()

    # Get the correct MIME format
    font_format = FONT_FORMATS.get(font_ext, "truetype")

    # Generate CSS with Base64 font
    custom_css = f"""
    <style>
        @font-face {{
            font-family: '{font_name}';
            src: url(data:font/{font_format};base64,{font_base64}) format('{font_format}');
        }}
        .custom-text {{
            font-family: '{font_name}', sans-serif;
            font-size: 24px;
        }}
    </style>
    """
    return custom_css, None

def display_font_preview(font_name, font_ext):
    """Displays a preview of the selected font in Streamlit."""
    custom_css, error = get_font_base64(font_name, font_ext)
    if error:
        st.error(error)
    else:
        st.markdown(custom_css, unsafe_allow_html=True)
        st.markdown(f'<p class="custom-text">This is a PREVIEW of {font_name}.</p>', unsafe_allow_html=True)

