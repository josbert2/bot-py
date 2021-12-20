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
from flask import request
import time
from flask import send_from_directory

from rich import print





app = Flask(__name__,template_folder='template')


@app.route('/')
def index():
    modal = []
    
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get('https://www.entrekids.cl/')
    time.sleep(3)
    driver.find_element_by_class_name('btn-log').click()
    print("Modal Login - [bold green]success  ✓ [/bold green]!")
    modal.append("Modal Login -")
    time.sleep(3)
    driver.find_element_by_id('username').send_keys('fmover@gmail.com')
    driver.find_element_by_id('password').send_keys('12345')
    print("Ejecutando Login - [bold green]success  ✓ [/bold green]!")
    modal.append("Modal Login -")
    time.sleep(3)
    print("Login - [bold green]success  ✓ [/bold green]!")
   
    modal.append("Modal Login -")


    return render_template('index.html', **locals())



if __name__ == '__main__':
    app.run(debug=True)


