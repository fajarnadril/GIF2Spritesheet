
import streamlit as st
from PIL import Image
import math
import os

# Fungsi untuk mengubah gif menjadi spritesheet dengan margin dan pengaturan otomatis row/column
def gif_to_spritesheet(gif_path, sprite_width, sprite_height, total_frames, margin):
    # Membuka GIF
    gif = Image.open(gif_path)
    frames = []

    # Menyimpan semua frame GIF ke dalam list
    while True:
        frames.append(gif.copy())
        try:
            gif.seek(gif.tell() + 1)
        except EOFError:
            break

    # Menentukan jumlah kolom dan baris yang seimbang
    columns = math.ceil(math.sqrt(total_frames))  # Menggunakan akar kuadrat untuk membuat bentuk kotak
    rows = math.ceil(total_frames / columns)

    # Menentukan ukuran spritesheet dengan margin
    spritesheet_width = (sprite_width + margin) * columns - margin  # Lebar per kolom + margin
    spritesheet_height = (sprite_height + margin) * rows - margin  # Tinggi per baris + margin

    # Membuat canvas kosong untuk spritesheet
    spritesheet = Image.new("RGBA", (spritesheet_width, spritesheet_height))

    # Menambahkan setiap frame ke dalam spritesheet
    for idx, frame in enumerate(frames):
        if idx >= total_frames:  # Pastikan hanya menggunakan jumlah frame yang diinginkan
            break

        # Hitung posisi kolom dan baris frame
        row = idx // columns
        col = idx % columns

        # Posisi x dan y di dalam spritesheet
        x_pos = col * (sprite_width + margin)
        y_pos = row * (sprite_height + margin)

        # Resize frame sesuai ukuran sprite
        frame_resized = frame.resize((sprite_width, sprite_height))

        # Menempelkan frame ke posisi yang sesuai di spritesheet
        spritesheet.paste(frame_resized, (x_pos, y_pos))

    # Menyimpan spritesheet ke file sementara
    output_path = "spritesheet.png"
    spritesheet.save(output_path)

    return output_path

# Streamlit app layout
st.title("GIF to Spritesheet Converter")

# File uploader
uploaded_file = st.file_uploader("Upload your GIF", type="gif")

if uploaded_file is not None:
    # Read the parameters
    sprite_width = st.number_input("Sprite Width", min_value=1, value=64)
    sprite_height = st.number_input("Sprite Height", min_value=1, value=64)
    total_frames = st.number_input("Total Frames", min_value=1, value=20)
    margin = st.number_input("Margin", min_value=0, value=5)

    # Display the uploaded GIF
    st.image(uploaded_file, caption="Uploaded GIF", use_column_width=True)

    # Process the GIF
    if st.button("Convert to Spritesheet"):
        with open("uploaded.gif", "wb") as f:
            f.write(uploaded_file.getbuffer())

        spritesheet_path = gif_to_spritesheet("uploaded.gif", sprite_width, sprite_height, total_frames, margin)
        st.image(spritesheet_path)

        # Provide download link
        st.download_button(
            label="Download Spritesheet",
            data=open(spritesheet_path, "rb").read(),
            file_name="spritesheet.png",
            mime="image/png"
        )
