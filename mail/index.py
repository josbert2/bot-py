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
from openpyxl import Workbook
import xlrd
from selenium.common.exceptions import NoSuchElementException



workbook = xlrd.open_workbook("link.xlsx","rb")
sheets = workbook.sheet_names()
productos_link = []

for sheet_name in sheets:
    sh = workbook.sheet_by_name(sheet_name)
    for rownum in range(sh.nrows):
        row_valaues = sh.row_values(rownum)
        productos_link.append(row_valaues[0])
     


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


for i in range(len(productos_link)):
    print("Scan:" + str(i))

    
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(productos_link[i])

    nombre = driver.find_element_by_css_selector('.h1-alert').text
    imagen = driver.find_element_by_css_selector('.zoomImg')
    imagen = imagen.get_attribute('src')

    response = requests.get(imagen)
    Image.open(BytesIO(response.content)).convert('RGBA').save('static/image-' + str(i) + '.png')




    precioNormal = 0
    precioOferta = 0

    try:
        element = driver.find_element_by_class_name('price-big').find_element_by_class_name('price-none')
        precioNormal = driver.find_element_by_css_selector('.price-big .price-none').text
    except NoSuchElementException:
        precioNormal = 0
        print("No element found")


    try:
        element = driver.find_element_by_css_selector('.precio-oferta-div')
        precioOferta = driver.find_element_by_css_selector('.precio-oferta-div').text 
        precioOferta = precioOferta.replace("(oferta)","")
    except NoSuchElementException:
        precioOferta = 0
        print("No element found")



    try:
        element = driver.find_element_by_css_selector('.porcentaje-email')
        descuento = driver.find_element_by_css_selector('.porcentaje-email').text 
    except NoSuchElementException:
        descuento = 0
        print("No element found")
  
    
    background = Image.new('RGB', ((300, 465)), (255, 255, 255))
    backgroundButton = Image.open('btn.png')


    font = ImageFont.truetype('Pangram-Bold.otf', 17)
    font2 = ImageFont.truetype('Pangram-Light.otf', 14)
    userinput = nombre


    producto = Image.open('static/image-' + str(i) + '.png').convert('RGBA')
    producto = producto.resize((276, 276))

    print(background.size[1])


    background.paste(producto, (0, 0), producto)
    background.paste(backgroundButton, (0, background.size[1] - backgroundButton.size[1]), backgroundButton)

    diff = textwrap.wrap(userinput, width=28)



    draw_multiple_line_text(background, userinput, font, '#41494f', producto.size[1])
    #draw_multiple_line_text(background, "$90.000 | 35%", font, 'rgba(245,106,128, 1)', producto.size[1] + 53)


    if precioOferta[i] != 0:
        descuento = descuento.replace("DCTO", "")
        draw_multiple_line_text(background, precioOferta + ' | ' + descuento, font, '#f06980', producto.size[1] + 53)
    else:
        draw_multiple_line_text(background, " ", font, '#f06980', producto.size[1] + 53)

    
    draw_multiple_line_text(background, "precio normal:" + precioNormal, font2, '#41494f', producto.size[1] + 83)


    background.show()



