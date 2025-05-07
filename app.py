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
