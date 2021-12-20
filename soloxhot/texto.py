from PIL import Image, ImageDraw, ImageFont
import textwrap
import qrcode
from openpyxl import Workbook
import xlrd
import master as x
import requests
from io import BytesIO
from random import randrange
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from time import sleep
import time
from alive_progress import alive_bar, config_handler
from rich import print
from rich.console import Console
import sys
from selenium.webdriver.chrome.options import Options

from selenium.common.exceptions import NoSuchElementException
from sys import platform

def getHeightText(text, width=18):
    lines = textwrap.wrap(header_text, width=width, break_long_words = True, replace_whitespace=True, drop_whitespace = False)
    y_text = 0
    for letter in lines:
        line_width, line_height = font.getsize(letter)
        letter_width, letter_height = draw.textsize(letter, font=font)
        y_text += line_height
    return y_text


y_text = 0
image = Image.new('RGB', (1000, 1000), color = 'white')
draw = ImageDraw.Draw(image)
font = ImageFont.truetype('Pangram-ExtraBold.otf', 44)
image_width, image_height = image.size
header_text = 'RADADA SMART START FISHER PRICE'
lines = textwrap.wrap(header_text, width=18, break_long_words = True, replace_whitespace=True, drop_whitespace = False)





x = 0
xpos = 0
checkIndex = 0
for idx, letter in enumerate(lines):
  line_width, line_height = font.getsize(letter)
  letter_width, letter_height = draw.textsize(letter, font=font)
  checkIndex = idx
  if checkIndex == 0:
    xpos = 0
    xpoy = 7
  elif checkIndex == 1:
    xpos = 0
    xpoy = -3
  elif checkIndex == 2:
    xpos = 0
    xpoy = -3
  elif checkIndex == 3:
    xpos = 0
    xpoy = 3

  for i in range(0, len(letter)):
    letter_width, letter_height = draw.textsize(letter[i], font=font)
    print(letter_width)
    if letter_width == 36:
        xpos += - 1 
    draw.text((((image_width -  line_width) / 2) + xpos , y_text), letter[i], (0,0,0), font=font, spacing=10)
    xpos += letter_width - 3
    
  
  y_text += line_height + xpoy
    


#print(getHeightText(header_text))



image.show()










"""
desired_width_of_text = 300
left_side_padding = 10



total_text_width, total_text_height = draw.textsize(header_text, font=font )
width_difference = desired_width_of_text - total_text_width
gap_width = - 3
xpos = left_side_padding

# Si mayor a 10 ultimas unidades disponible

for letter in lines:
    line_width, line_height = font.getsize(letter)
    letter_width, letter_height = draw.textsize(letter, font=font)
    if letter == ' ':
        xpos += 10
    else:
        xpos += 0
    draw.text(((image_width - line_width) / 2, y_text),letter, (0,0,0), font=font)
    y_text += line_height
    xpos += letter_width + gap_width
   




image.show()"""