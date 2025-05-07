
import streamlit as st
from PIL import Image
import requests
from io import BytesIO

# URL of the GIF hosted on GitHub
gif_url = "https://raw.githubusercontent.com/fajarnadril/GIF2Spritesheet/main/assets/yourgif.gif"

# Fetch the image from GitHub
response = requests.get(gif_url)
img = Image.open(BytesIO(response.content))

# Resize the image (example: resize to width=400px, while keeping aspect ratio)
width = 400
height = int((width / float(img.size[0])) * float(img.size[1]))  # Maintain aspect ratio
img_resized = img.resize((width, height))

# Display the resized image
st.image(img_resized, caption="GIF from GitHub", use_column_width=True)
