from PIL import Image, ImageDraw, ImageFont

WIDTH_TO_FONT_SIZE = {
    24: 10,  
    32: 14,
    50: 22,
    70: 31,
    112: 50,
    128: 57
}

#If you would use a different font or different label sizes, this can be used to calculate the appropriate font size.
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

def text_to_image(text, image_height):
    font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

    #for value in WIDTH_TO_FONT_SIZE.keys():
    #    pointsize = calculate_font_size(text, font_path, image_height, 0.5)
    #    print(f"value: {value}")
    #    print(f"pointsize: {pointsize}")
    image_width = calculate_width(text, font_path, image_height)
    font_size = WIDTH_TO_FONT_SIZE[image_height]
    image_size = (image_width, image_height)
    
    # Create a transparent image
    image = Image.new("RGBA", image_size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    
    # Load the font and set the font size
    font = ImageFont.truetype(font_path, font_size)
    
    # Draw the text on the image
    _, _, w, h = draw.textbbox((0, 0), text, font=font)
    draw.text(((image_width-w)/2, (image_height-h)/2), text, font=font, fill=(0, 0, 0, 255))
    
    return image

def calculate_width(text, font_path, font_size):
    # Load the font and set the font size
    font = ImageFont.truetype(font_path, font_size)
    
    # Get the size of the text
    width, height = ImageDraw.Draw(Image.new("RGBA", (0, 0), (255, 255, 255, 0))).textlength(text, font=font)
    
    return width

def main():
    image = text_to_image("Hello World!", 70)
    image.save("hello_world.png")

if __name__ == "__main__":
    main()