from PIL import Image, ImageDraw, ImageFont

WIDTH_TO_FONT_SIZE = {
    24: 24,  # Actually 3.5mm, not sure how this is reported if its 3 or 4
    32: 32,
    50: 50,
    70: 70,
    112: 112,
    128: 128
}

def calculate_font_size(text, font_path, image_height, desired_height_ratio):
    def calculate_height(font_size):
        font = ImageFont.truetype(font_path, font_size)
        width, height = ImageDraw.Draw(Image.new("RGBA", (0, 0), (255, 255, 255, 0))).textsize(text, font=font)
        return height

    low, high = 0, image_height
    while low < high:
        mid = (low + high) // 2
        height = calculate_height(mid)
        if height / image_height < desired_height_ratio:
            low = mid + 1
        else:
            high = mid

    return low

def text_to_image(text, font_size, image_width, image_height):
    image_size = (image_width, image_height)
    font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
    # Create a transparent image
    image = Image.new("RGBA", image_size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    
    # Load the font and set the font size
    font = ImageFont.truetype(font_path, font_size)
    
    # Draw the text on the image
    draw.text((0, 0), text, font=font, fill=(0, 0, 0, 255))
    
    return image

def calculate_width(text, font_path, font_size):
    # Load the font and set the font size
    font = ImageFont.truetype(font_path, font_size)
    
    # Get the size of the text
    width, height = ImageDraw.Draw(Image.new("RGBA", (0, 0), (255, 255, 255, 0))).textsize(text, font=font)
    
    return width