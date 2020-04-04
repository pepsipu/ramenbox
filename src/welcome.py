import time
from PIL import Image, ImageDraw, ImageFont


def welcome_msg(display):
    title = "ramenbox"
    author = "pepsipu"

    loading_menu = Image.new("RGB", (display.width, display.height))
    loading_canvas = ImageDraw.Draw(loading_menu)

    title_font = ImageFont.truetype("fonts/Minecraft.ttf", 40)
    author_font = ImageFont.truetype("fonts/Minecraft.ttf", 25)

    # calculate widths and heights of the text
    author_width, author_height = loading_canvas.textsize(author, font=author_font)
    title_width, title_height = loading_canvas.textsize(title, font=title_font)

    # the title + author should be vertically centered

    # to calculate the vertical center location of the title + author, we first half the display height to get the vertical
    # center of the screen. If we were to write our text here, it would be misaligned as we'd write from the center down.
    # to solve this, we decrease our y coordinate by the height of half the text space, which would make our text space
    # centered. Since the title is at the top of the text space, we can directly write text here.
    text_area_pos = display.height / 2 - (title_height + author_height) / 2

    loading_canvas.text((display.width / 2 - title_width / 2, text_area_pos), title, font=title_font,
                        fill=(255, 179, 3, 255))

    # do the same thing as above, but now we need to write the title under the title so we get the start
    # of the text area once more and offset that by the title's height
    loading_canvas.text((display.width / 2 - author_width / 2, text_area_pos + title_height), author, font=author_font,
                        fill=(86, 135, 9, 255))
    display.ShowImage(loading_menu)
    time.sleep(1.5)

    # fade image to black by multiplying each pixel by .7
    for _ in range(7):
        loading_menu = loading_menu.point(lambda p: p * .55)
        display.ShowImage(loading_menu)
