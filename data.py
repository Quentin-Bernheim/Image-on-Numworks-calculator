import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image
from sklearn.cluster import KMeans

def open_file():
    """Opens file explorer to choose an image."""
    root = tk.Tk()
    root.withdraw()  # Hide main window
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    return file_path

def resize_image(image_path, size=(320, 240)):
    """Resizes image to 320x240."""
    img = Image.open(image_path).convert("RGB")
    img = img.resize(size)
    return img

def get_palette(img, n_colors=20):
    """Finds the 20 most dominant colors in the image."""
    img_data = np.array(img)
    pixels = img_data.reshape(-1, 3)

    kmeans = KMeans(n_clusters=n_colors, n_init=10)
    kmeans.fit(pixels)

    palette = kmeans.cluster_centers_.astype(int).tolist()
    return palette, kmeans.labels_.reshape(img.size[::-1])

def compress_image(data, palette):
    """Converts image data to a compressed string representation."""
    flat_data = data.flatten()
    compressed = []
    
    i = 0
    while i < len(flat_data):
        color_index = flat_data[i]
        count = 1
        
        while i + 1 < len(flat_data) and flat_data[i + 1] == color_index and count < 99:
            count += 1
            i += 1
        
        compressed.append(f"{chr(65 + color_index)}{count if count > 1 else ''}")
        i += 1
    
    return "".join(compressed)

def split_string(s, chunk_size=500):
    """Splits the compressed string into chunks of approximately `chunk_size` characters, ensuring breaks occur after a letter."""
    parts = []
    buffer = ""
    
    for char in s:
        if char.isalpha() and len(buffer) >= chunk_size:
            parts.append(buffer)
            buffer = ""
        buffer += char
    
    if buffer:
        parts.append(buffer)
    
    return parts

def main():
    """Main function to run the full pipeline."""
    image_path = open_file()
    if image_path:
        img = resize_image(image_path)
        palette, img_data = get_palette(img)
        compressed = compress_image(img_data, palette)
        parts = split_string(compressed)

        print("\nPalette (20 colors):")
        print(palette)

        print("\nCompressed Image Data:")
        for part in parts:
            print(f'"{part}"')
    else:
        print("No image selected.")

if __name__ == "__main__":
    main()

