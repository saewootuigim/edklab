import os
from PIL import Image

def convert_all_tifs_to_pngs(directory):
    # List all files in the given directory
    for filename in os.listdir(directory):
        # Check if the file is a TIFF file
        if filename.lower().endswith('.tif') or filename.lower().endswith('.tiff'):
            # Construct full file path
            input_path = os.path.join(directory, filename)
            # Create output path by changing the file extension to .png
            output_path = os.path.splitext(input_path)[0] + '.png'
            
            # Open the TIFF file and convert it to PNG
            with Image.open(input_path) as img:
                img.save(output_path, format='PNG')
            print(f"Converted: {filename} to {os.path.basename(output_path)}")

# Example usage
current_directory = os.getcwd()  # Use the current working directory
convert_all_tifs_to_pngs(current_directory)