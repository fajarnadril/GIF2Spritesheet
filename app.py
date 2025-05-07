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
            justify-content: center;
        }
        .container > div {
            width: 100%;
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
        .column {
            width: 100%;
        }
        .image-display {
            width: 100px;
            height: 100px;
            object-fit: contain;
            margin-top: 20px;
        }
        .upload-section {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 15px;
        }
        .upload-label {
            font-weight: bold;
            font-size: 1.2em;
        }
        .upload-button {
            padding: 10px;
            background-color: #2D89FF;
            color: white;
            border-radius: 5px;
        }
    </style>
""", unsafe_allow_html=True)

# Single column layout
st.header("Customize Spritesheet")
    
# Text boxes for customizable settings (input fields)
sprite_width = st.text_input("Sprite Width", value="64")  # Default value is 64px
sprite_height = st.text_input("Sprite Height", value="64")  # Default value is 64px
total_frames = st.text_input("Total Frames", value="20")  # Default value is 20
margin = st.text_input("Margin Between Frames", value="5")  # Default value is 5px

# Validate input (ensure they are integers and convert them)
try:
    sprite_width = int(sprite_width)
    sprite_height = int(sprite_height)
    total_frames = int(total_frames)
    margin = int(margin)
except ValueError:
    st.error("Please enter valid integer values for Sprite Width, Sprite Height, Total Frames, and Margin.")
    sprite_width = sprite_height = total_frames = margin = 64  # Reset to default values

# File uploader for the GIF
st.markdown('<div class="upload-section">', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload your GIF", type="gif")
st.markdown('</div>', unsafe_allow_html=True)

if st.button("Generate Spritesheet"):
    st.session_state['sprite_params'] = (sprite_width, sprite_height, total_frames, margin)

# Display the uploaded GIF and generate spritesheet preview
if uploaded_file is not None:
    # Display the uploaded GIF with a fixed width of 100px for consistent preview size
    st.image(uploaded_file, caption="Uploaded GIF", width=100)  # Fixed width for GIF preview (100px)

    # Save the uploaded GIF temporarily
    with open("uploaded.gif", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Generate spritesheet when button is clicked
    if 'sprite_params' in st.session_state:
        sprite_width, sprite_height, total_frames, margin = st.session_state['sprite_params']
        spritesheet_path = gif_to_spritesheet("uploaded.gif", sprite_width, sprite_height, total_frames, margin)

        # Display the generated spritesheet (same size as the uploaded GIF)
        st.image(spritesheet_path, caption="Generated Spritesheet", width=100)  # Fixed width for preview (100px)

        # Provide a download button for the spritesheet
        st.download_button(
            label="Download Spritesheet",
            data=open(spritesheet_path, "rb").read(),
            file_name="spritesheet.png",
            mime="image/png",
            help="Click to download the generated spritesheet"
        )
