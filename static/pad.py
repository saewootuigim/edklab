from PIL import Image, ImageOps
import os

def add_padding(input_image_path, output_image_path, padding, color):
    # Open the original image
    image = Image.open(input_image_path)

    # Calculate new dimensions with padding
    new_width = image.width + 2 * padding
    new_height = image.height# + 2 * padding

    # Create a new image with a transparent background
    if color=='black':
        new_image = Image.new("RGBA", (new_width, new_height), (0, 0, 0, 255))
    else:
        new_image = Image.new("RGBA", (new_width, new_height), (255, 255, 255, 255))

    # Paste the original image onto the new image, centered
    new_image.paste(image, (padding, 0))

    # Save the new image
    new_image.save(output_image_path)

# Example usage
padding = 120

input = os.path.abspath("static/carousel/7.png")
output = os.path.abspath("static/carousel/72.png")
add_padding(input, output, padding, 'black')

input = os.path.abspath("static/carousel/8.png")
output = os.path.abspath("static/carousel/82.png")
add_padding(input, output, padding, 'black')

input = os.path.abspath("static/carousel/9.png")
output = os.path.abspath("static/carousel/92.png")
add_padding(input, output, padding, 'white')