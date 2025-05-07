import streamlit as st
from PIL import Image
import math
import os

# Function to convert GIF to spritesheet
def gif_to_spritesheet(gif_path, sprite_width, sprite_height, total_frames, margin):
    # Open the GIF
    gif = Image.open(gif_path)
    frames = []

    # Save all frames of the GIF into a list
    while True:
        frames.append(gif.copy())
        try:
            gif.seek(gif.tell() + 1)
        except EOFError:
            break

    # Calculate the number of rows and columns for the spritesheet
    columns = math.ceil(math.sqrt(total_frames))  # Using square root to make it more square-like
    rows = math.ceil(total_frames / columns)

    # Calculate the size of the spritesheet with margin
    spritesheet_width = (sprite_width + margin) * columns - margin
    spritesheet_height = (sprite_height + margin) * rows - margin

    # Create a blank canvas for the spritesheet
    spritesheet = Image.new("RGBA", (spritesheet_width, spritesheet_height))

    # Add each frame to the spritesheet
    for idx, frame in enumerate(frames):
        if idx >= total_frames:
            break
        row = idx // columns
        col = idx % columns

        # Position x and y in the spritesheet
        x_pos = col * (sprite_width + margin)
        y_pos = row * (sprite_height + margin)

        # Resize the frame and paste it into the spritesheet
        frame_resized = frame.resize((sprite_width, sprite_height))
        spritesheet.paste(frame_resized, (x_pos, y_pos))

    # Save the spritesheet as a file
    output_path = "spritesheet.png"
    spritesheet.save(output_path)

    return output_path

# Streamlit app layout
st.set_page_config(page_title="GIF to Spritesheet Converter", layout="wide")
st.title("GIF to Spritesheet Converter")

# Add some styling to make it more professional
st.markdown("""
    <style>
        .main {
            padding: 20px;
        }
        .header {
            font-size: 2em;
            font-weight: bold;
            color: #2F4F4F;
        }
        .container {
            display: flex;
            flex-wrap: wrap;
            gap: 30px;
        }
        .container > div {
            width: 45%;
        }
        .button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            cursor: pointer;
            border-radius: 5px;
        }
        .button:hover {
            background-color: #45a049;
        }
    </style>
""", unsafe_allow_html=True)

# File uploader for the GIF
uploaded_file = st.file_uploader("Upload your GIF", type="gif")

if uploaded_file is not None:
    # Load the uploaded GIF and display it (no resizing)
    img = Image.open(uploaded_file)

    # Display the GIF with specific dimensions for layout (without resizing it)
    st.markdown('<div class="container">', unsafe_allow_html=True)
    st.markdown('<div class="header">Uploaded GIF:</div>', unsafe_allow_html=True)
    st.image(uploaded_file, caption="Uploaded GIF", use_column_width=True)  # Display original size, with small width for layout
    st.markdown('</div>', unsafe_allow_html=True)

    # Parameters for spritesheet
    st.markdown('<div class="container">', unsafe_allow_html=True)
    sprite_width = st.number_input("Sprite Width", min_value=1, value=64, step=1, label_visibility="collapsed")
    sprite_height = st.number_input("Sprite Height", min_value=1, value=64, step=1, label_visibility="collapsed")
    total_frames = st.number_input("Total Frames", min_value=1, value=20, label_visibility="collapsed")
    margin = st.number_input("Margin Between Frames", min_value=0, value=5, label_visibility="collapsed")

    if st.button("Convert to Spritesheet", key="convert_spritesheet"):
        # Save the uploaded GIF temporarily
        with open("uploaded.gif", "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Convert GIF to spritesheet
        spritesheet_path = gif_to_spritesheet("uploaded.gif", sprite_width, sprite_height, total_frames, margin)

        # Display the generated spritesheet
        st.markdown('<div class="container">', unsafe_allow_html=True)
        st.markdown('<div class="header">Generated Spritesheet:</div>', unsafe_allow_html=True)
        st.image(spritesheet_path, caption="Generated Spritesheet", use_column_width=True)  # Display spritesheet
        st.markdown('</div>', unsafe_allow_html=True)

        # Provide a download button for the spritesheet
        st.download_button(
            label="Download Spritesheet",
            data=open(spritesheet_path, "rb").read(),
            file_name="spritesheet.png",
            mime="image/png",
            help="Click to download the generated spritesheet"
        )

    st.markdown('</div>', unsafe_allow_html=True)
