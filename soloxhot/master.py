from PIL import Image, ImageDraw, ImageFont, ImageFile
import textwrap
import qrcode
from openpyxl import Workbook
import xlrd
from rembg.bg import remove
import numpy as np
import io
def draw_multiple_line_text(image, text, font, text_color, text_start_height, push, width=None, positionCenter=None):
    '''
    From unutbu on [python PIL draw multiline text on image](https://stackoverflow.com/a/7698300/395857)
    '''
    draw = ImageDraw.Draw(image)
    image_width, image_height = image.size
    y_text = text_start_height
    if push == 'right':
        lines = textwrap.wrap(text, width=28)
    elif push == 'fbpush':
        lines = textwrap.wrap(text, width=22)
    else:
        lines = textwrap.wrap(text, width=28)
    for line in lines:
        line_width, line_height = font.getsize(line)
        ##draw.text(((image_width - line_width) / 2, y_text), 
        #          line, font=font, fill=text_color)
        #  image_width // 2 + width // 2 
        if push == 'right':

        
            draw.text(((image_width - line_width + image_width // 2 + width // 2 - 100 ) / 2 , y_text), line, font=font, fill=text_color)
        elif push == 'right2':
            draw.text((12 + positionCenter, y_text), line, font=font, fill=text_color)
        elif push == 'right5':
            draw.text((positionCenter, y_text), line, font=font, fill=text_color)
        elif push == 'right3':
            draw.text((positionCenter, y_text), line, font=font, fill=text_color)
        elif push == 'fbpush':
           center = (image_width - line_width) // 2
           draw.text((center + 250, y_text), line, font=font, fill=text_color)
        elif push == 'pushreal':
            draw.text(((image_width - line_width + image_width // 2 + width // 2 - 0 ) / 2 , y_text), line, font=font, fill=text_color)
        elif push == 'pushfb':
            draw.text(((image_width - line_width + image_width // 2 + width // 2 + 80 ) / 2 , y_text), line, font=font, fill=text_color)
        else:
            draw.text(((image_width - line_width) / 2, y_text), line, font=font, fill=text_color)
        y_text += line_height
def remobeBG(image, i=0):
    ImageFile.LOAD_TRUNCATED_IMAGES = True

    input_path = image
    output_path = './image_with_bg/image_' + str(i) + '.png'

    f = np.fromfile(input_path)
    result = remove(f)
    img = Image.open(io.BytesIO(result)).convert("RGBA")
    img.save(output_path)