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
st.title("GIF to Spritesheet Converter")

# File uploader for GIF
uploaded_file = st.file_uploader("Upload your GIF", type="gif")

if uploaded_file is not None:
    # Load the uploaded GIF and display it
    img = Image.open(uploaded_file)

    # Resize the GIF (actual resizing, not just display size)
    width = st.number_input("Resize width for display:", min_value=1, value=400)
    height = int((width / float(img.size[0])) * float(img.size[1]))  # Maintain aspect ratio
    img_resized = img.resize((width, height))

    # Display the resized image
    st.image(img_resized, caption="Resized GIF", use_column_width=True)

    # Parameters for spritesheet
    sprite_width = st.number_input("Sprite Width", min_value=1, value=64)
    sprite_height = st.number_input("Sprite Height", min_value=1, value=64)
    total_frames = st.number_input("Total Frames", min_value=1, value=20)
    margin = st.number_input("Margin Between Frames", min_value=0, value=5)

    if st.button("Convert to Spritesheet"):
        # Save the uploaded GIF temporarily
        with open("uploaded.gif", "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Convert GIF to spritesheet
        spritesheet_path = gif_to_spritesheet("uploaded.gif", sprite_width, sprite_height, total_frames, margin)

        # Display the generated spritesheet
        st.image(spritesheet_path, caption="Generated Spritesheet", use_column_width=True)

        # Provide a download button for the spritesheet
        st.download_button(
            label="Download Spritesheet",
            data=open(spritesheet_path, "rb").read(),
            file_name="spritesheet.png",
            mime="image/png"
        )
