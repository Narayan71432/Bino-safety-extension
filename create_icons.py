from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, output_path):
    # Create a red square with a white cross
    img = Image.new('RGB', (size, size), color='red')
    draw = ImageDraw.Draw(img)
    
    # Draw a white cross
    margin = size // 4
    draw.line([(margin, size//2), (size-margin, size//2)], fill='white', width=size//8)
    draw.line([(size//2, margin), (size//2, size-margin)], fill='white', width=size//8)
    
    # Save the image
    img.save(output_path)

# Create icons directory if it doesn't exist
os.makedirs('extension/images', exist_ok=True)

# Create icons in different sizes
sizes = [16, 48, 128]
for size in sizes:
    output_path = f'extension/images/icon{size}.png'
    create_icon(size, output_path)
    print(f'Created {output_path}')
