from PIL import Image, ImageDraw, ImageFont
import textwrap
import qrcode
from openpyxl import Workbook
import xlrd
def draw_multiple_line_text(image, text, font, text_color, text_start_height, push, width=None):
    '''
    From unutbu on [python PIL draw multiline text on image](https://stackoverflow.com/a/7698300/395857)
    '''
    draw = ImageDraw.Draw(image)
    image_width, image_height = image.size
    y_text = text_start_height
    if push == 'right':
        lines = textwrap.wrap(text, width=28)
    else:
        lines = textwrap.wrap(text, width=28)
    for line in lines:
        line_width, line_height = font.getsize(line)
        ##draw.text(((image_width - line_width) / 2, y_text), 
        #          line, font=font, fill=text_color)
        #  image_width // 2 + width // 2 
        if push == 'right':
            print(width)
            draw.text(((image_width - line_width + image_width // 2 + width // 2 - 100 ) / 2 , y_text), line, font=font, fill=text_color)
        else:
            draw.text(((image_width - line_width) / 2, y_text), line, font=font, fill=text_color)
        y_text += line_height
