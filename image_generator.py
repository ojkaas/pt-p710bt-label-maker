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

    text_width,text_height = calculate_text_size(text, font_path, image_height)
    print(f"text_width: {text_width}")
    image_width = text_width + 5;
    font_size = WIDTH_TO_FONT_SIZE[image_height]
    image_size = (image_width, image_height)
    
    # Create a transparent image
    image = Image.new("RGBA", image_size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    
    # Load the font and set the font size
    font = ImageFont.truetype(font_path, font_size)
    
    # Draw the text on the image
    draw.text(
        xy=(image_width / 2, image_height / 2),
        text=text,
        fill=(0, 0, 0, 255),
        font=font,
        anchor="mm",
        align="center"
    )
    
    return image

def calculate_text_size(text, font_path, font_size):
    # Load the font and set the font size
    font = ImageFont.truetype(font_path, font_size)
    # Get the size of the text
    return font.getsize(text)

def main():
    image = text_to_image("Hello World!", 70)
    image.save("hello_world.png")

if __name__ == "__main__":
    main()