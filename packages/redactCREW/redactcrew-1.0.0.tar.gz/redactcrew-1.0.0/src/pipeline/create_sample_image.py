# src/pipeline/create_sample_image.py

from PIL import Image, ImageDraw, ImageFont
import os

def create_sample_image():
    # Create a white background image
    img = Image.new('RGB', (800, 400), color = (255, 255, 255))
    d = ImageDraw.Draw(img)

    # Load a font
    try:
        # Ensure you have a font that supports both English and Hindi
        font = ImageFont.truetype("arial.ttf", 40)
    except IOError:
        # Default to a basic font if arial is not found
        font = ImageFont.load_default()

    # Add English text
    d.text((50,50), "John Doe", fill=(0,0,0), font=font)
    d.text((50,150), "Aadhar: 1234-5678-9012", fill=(0,0,0), font=font)
    d.text((50,250), "PAN: ABCDE1234F", fill=(0,0,0), font=font)

    # Add Hindi text
    d.text((50,350), "नाम: यशू", fill=(0,0,0), font=font)
    d.text((400,350), "पता: 123 एमजी रोड, बेंगलुरु", fill=(0,0,0), font=font)

    # Save the image
    img_path = os.path.join('input', 'sample_image.png')
    img.save(img_path)
    print(f"Sample image created at {img_path}")

if __name__ == "__main__":
    os.makedirs('input', exist_ok=True)
    create_sample_image()