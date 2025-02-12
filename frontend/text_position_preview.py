import streamlit as st
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from loguru import logger
def text_position_preview(image, text, text_color, text_size, font_name, text_transparency):
    img_width, img_height = image.size
    col1, col2 = st.columns(2)
    with col1:
        st.write("")  # Adds spacing                                # Adding space above sliders
        x_percent = st.slider("X Position (%)", 0, 100, 50)                             # X and Y position as percentage (0% to 100%)
        y_percent = st.slider("Y Position (%)", 0, 100, 50)
    alpha = int((text_transparency / 100) * 255)                                        # Convert transparency from 0-100 range to 0-255 range
    text_color_rgba = tuple(int(text_color[i:i+2], 16) for i in (1, 3, 5))+(alpha,)   

    position_x = int((x_percent / 100) * img_width)                                     # Convert percentage to pixel coordinates
    position_y = int((y_percent / 100) * img_height)
    image_with_text = image.convert("RGBA")                                             # Ensure image supports transparency
    overlay = Image.new("RGBA", image_with_text.size, (255, 255, 255, 0))               # Transparent layer
    draw = ImageDraw.Draw(overlay)
    try:
        print(f"utils/fonts/{font_name}")
        font = ImageFont.truetype(f"utils/fonts/{font_name}", text_size)
    except IOError:
        logger.error("could not load font")
        font = ImageFont.load_default()
    draw.text((position_x, position_y), text, fill=text_color_rgba, font=font) 
    final_image = Image.alpha_composite(image_with_text, overlay)
    with col2:
        st.image(final_image, caption="Image with text preview", use_container_width=True)
    return position_x, position_y