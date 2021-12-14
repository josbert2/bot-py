import re
from flask import Flask,render_template
from PIL import Image, ImageDraw, ImageFont
from bs4 import BeautifulSoup
import textwrap
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
import time
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import requests
import ssl
import certifi
from urllib import request as rq
from io import BytesIO

import time


from rich import print


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
        draw.text((10, y_text), 
                  line, font=font, fill=text_color)
        y_text += line_height

url = 'https://www.entrekids.cl/producto/organo-electrico-nup03-61-teclas-color-negro'

"""
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)

nombre = driver.find_element_by_css_selector('.h1-alert')
imagen = driver.find_element_by_css_selector('.zoomImg')


precioNormal = []
precioOferta = []

if len(driver.find_element_by_css_selector('#price-none')[0]) > 0:
    precioNormal.append(driver.find_element_by_css_selector('#price-none')[0].text) 
if len(driver.find_element_by_css_selector('.precio-oferta-div')[0]) > 0:
    precioOferta.append(driver.find_element_by_css_selector('.precio-oferta-div')[0].text)
"""
background = Image.new('RGB', ((300, 465)), (255, 255, 255))
backgroundButton = Image.open('btn.png')


font = ImageFont.truetype('Pangram-Bold.otf', 17)
font2 = ImageFont.truetype('Pangram-Light.otf', 14)
userinput = "Lorem ipsum dolor sit amet asdad"


producto = Image.open('unnamed.jpg').convert('RGBA')
producto = producto.resize((276, 276))

print(background.size[1])


background.paste(producto, (0, 0), producto)
background.paste(backgroundButton, (0, background.size[1] - backgroundButton.size[1]), backgroundButton)

print(len(textwrap.wrap(userinput, width=28)))



draw_multiple_line_text(background, userinput, font, '#41494f', producto.size[1])
draw_multiple_line_text(background, "$90.000 | 35%", font, 'rgba(245,106,128, 1)', producto.size[1] + 53)
draw_multiple_line_text(background, "precio normal: $25.245", font2, '#41494f', producto.size[1] + 83)


background.show()



