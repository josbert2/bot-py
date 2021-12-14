from PIL import Image, ImageDraw, ImageFont
import textwrap
import qrcode

from openpyxl import Workbook
import xlrd
import time
import locale
from currencies import Currency
import locale
from rich import print

import soloxhoy


locale.setlocale(locale.LC_MONETARY, 'en_US.UTF-8')

def format_float_with_trailing_zeros(num):
   return locale.currency(num, grouping=True)

def floatToString(inputValue):
    result = ('%.15f' % int(inputValue)).rstrip('0').rstrip('.')
    return '0' if result == '-0' else result

def format_float(num):
    return ('%i' if num == int(num) else '%s') % num

def remove_trailing_zeros(x):
    return str(x).rstrip('5').rstrip('0').rstrip('.')

def draw_multiple_line_text(image, text, font, text_color, text_start_height):
    '''
    From unutbu on [python PIL draw multiline text on image](https://stackoverflow.com/a/7698300/395857)
    '''
    draw = ImageDraw.Draw(image)
    image_width, image_height = image.size
    y_text = text_start_height
    lines = textwrap.wrap(text, width=28)
    for line in lines:
        line_width, line_height = font.getsize(line)
        ##draw.text(((image_width - line_width) / 2, y_text), 
        #          line, font=font, fill=text_color)
        draw.text(((image_width - line_width) / 2, y_text), 
                  line, font=font, fill=text_color)
        y_text += line_height

workbook = xlrd.open_workbook("P_P.xlsx","rb")
sheets = workbook.sheet_names()
productos_titulo = []
marca_titulo = []
precio_titulo = []
total_producto = []
for sheet_name in sheets:
    sh = workbook.sheet_by_name(sheet_name)
    for rownum in range(sh.nrows):
        row_valaues = sh.row_values(rownum)
        productos_titulo.append(row_valaues[0])
        marca_titulo.append(row_valaues[1])
        precio_titulo.append(row_valaues[3])
        total_producto.append(row_valaues)       

#platform = ['postInsta', 'Facebook', 'Story', 'Push', 'facebookhorizontal']
platform = ['post-ig', 'post-fb', 'story', 'push', 'fb-horizontal']
bgPlatform = [
   'img/armado/post-ig.png',
   'img/armado/post-fb.png', 
   'img/armado/story.png', 
   'img/armado/push_.png', 
   'img/armado/fb-horizontal.png'
]
postInstaW_producto, postInstaH_producto = (500, 500)
FacebookW_producto, FacebookH_producto = (600, 600)
StoryW_producto, StoryH_producto = (600, 600)
pushW_producto, pushH_producto = (150, 150)
facebook_horizontal_productoW, facebook_horizontal_productoH =  (400, 400)

postInstagramTamano = postInstaW, postInstaH = (1080, 1080) 
fbTamano = FacebookW, FacebookH = (1350, 1080) 
storyTamano = StoryW, StoryH = (1080, 1920) 
pushTamano = pushW, pushH = (602, 258) 
fbHorizontalTamano = facebook_horizontalW, facebook_horizontalH =  (1200, 628) # Correcto



loopPlatform = [(postInstagramTamano), (fbTamano), (storyTamano), (pushTamano), (fbHorizontalTamano)]
loopPlatformProducto = [(500, 500), (500, 500), (600, 600), (250, 250), (400, 400)]





soloxhoy.igPost(total_producto, bgPlatform, loopPlatform, loopPlatformProducto)

