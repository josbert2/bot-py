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

dev = False
devInfo = False
def taskStatus(task='Default task', limit=20):
   console = Console()
   tasks = [f"Run: {task}" for n in range(0, 1)]
   print()
   with console.status("[bold green]Working on tasks...") as status:
      while tasks:
         task = tasks.pop(0)
         sleep(3)
         console.log(f"{task} complete")
   
   # break line

   progressBar(limit)
   print(f'[bold green] ✔ [/bold green] {task} [bold green]SUCCESS [/bold green]')


def progressBar(limit ):
   with alive_bar(limit, length=40) as bar:
      for i in range(limit):
         time.sleep(0.15)
         bar()
  
campama = ''

def grid(img):
   step_count = 6
   #height = 600
   #width = 600
   image = img
   # Draw some lines
   draw = ImageDraw.Draw(image)
   y_start = 0
   y_end = image.height
   step_size = int(image.width / step_count)

   for x in range(0, image.width, step_size):
      line = ((x, y_start), (x, y_end))
      draw.line(line, fill=128)

   x_start = 0
   x_end = image.width

   for y in range(0, image.height, step_size):
      line = ((x_start, y), (x_end, y))
      draw.line(line, fill=128)

   del draw

   image.show()
#Incluir categoria


nombre = []
imagenes = []
marcas = []
categorias = []
precioNormals = []
precioOfertas = []
descuentos = []
productos_link = []
def crwalUrl():
   global productos_link

   workbook = xlrd.open_workbook("link.xlsx","rb")
   sheets = workbook.sheet_names()
   

   for sheet_name in sheets:
      sh = workbook.sheet_by_name(sheet_name)
      for rownum in range(9, sh.nrows):
         row_valaues = sh.row_values(rownum)
         productos_link.append(row_valaues[0])

   

   taskStatus(task='Extract Info from Excel', limit=len(productos_link))


   
   for i in range(len(productos_link)):
   
      options = Options()
      #options.add_argument('--headless')
      #options.add_argument('--disable-gpu')
      print(platform)
      if platform == "win32":
         driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(), options=options)
      else:
         driver = webdriver.Chrome(executable_path='./chromedriver')
        
      #driver.set_window_position(0, 0)
      driver.get(productos_link[i])

      print('[bold blue] Index: [/bold blue]' + str(i) )
      print(driver.find_element_by_tag_name('h1').text)
      nombre.append(driver.find_element_by_tag_name('h1').text)

      imagen = driver.find_element_by_class_name('lazy-image-cloud')
      imagen = imagen.get_attribute('src')
   
      imagenes.append(imagen)
      print('[bold red] Crawl URL: [/bold red]' + productos_link[i] )

      response = requests.get(imagen)
      Image.open(BytesIO(response.content)).convert('RGBA').save('image/' + str(i) + '.png')

      print('[bold blue] Quitando fondo de la imagen... [/bold blue]')
      if platform == "win32":
         x.removeBG2('image/' + str(i) + '.png', i)
      else:
         x.remobeBG('image/' + str(i) + '.png', i)
     

      



      try:
         element = driver.find_element_by_class_name('price-big').find_element_by_class_name('price-none')
         precioNormals.append(driver.find_element_by_css_selector('.price-big .price-none').text)
         print(f'[bold green] ✔ [/bold green] Precio normal encontrado [bold green]SUCCESS [/bold green]')
      except NoSuchElementException:
         precioNormals.append(0)
         print(f'[bold red] x [/bold red] Precio normal NO encontrado [bold red] Failed [/bold red]')


      try:
         element = driver.find_element_by_css_selector('.precio-oferta-div')
         precioOferta = driver.find_element_by_css_selector('.precio-oferta-div').text 
         precioOferta = precioOferta.replace("(oferta)","")
         precioOfertas.append(precioOferta)
         print(f'[bold green] ✔ [/bold green] Precio oferta encontrado [bold green]SUCCESS [/bold green]')
      except NoSuchElementException:
         precioOfertas.append(0)
         print(f'[bold red] ✔ [/bold red] Precio oferta NO encontrado [bold red] Failed [/bold red]')




      try:
         element = driver.find_element_by_css_selector('.porcentaje-email')
         descuentos.append(driver.find_element_by_css_selector('.porcentaje-email').text )
         print(f'[bold green] ✔ [/bold green] Descuento encontrado [bold green]SUCCESS [/bold green]')
      except NoSuchElementException:
         descuentos.append(0)
         print(f'[bold red] ✔ [/bold red] Descuento NO encontrado [bold red] Failed [/bold red]')

      try:
         element = driver.find_element_by_css_selector('.marca-producto')
         marcas.append(driver.find_element_by_css_selector('.marca-producto').text )
         print(f'[bold green] ✔ [/bold green] Marca encontrada [bold green]SUCCESS [/bold green]')
      except NoSuchElementException:
         marcas.append(0)
         print(f'[bold red] ✔ [/bold red]  Marca no encontrada [bold red] Failed [/bold red]')

      try:
         element = driver.find_element_by_css_selector('.breadcrumb-items')
         categorias.append(driver.find_element_by_css_selector('.breadcrumb-items a:last-child').text )
         print(f'[bold green] ✔ [/bold green] Marca encontrada [bold green]SUCCESS [/bold green]')
      except NoSuchElementException:
         categorias.append(0)
         print(f'[bold red] ✔ [/bold red]  Marca no encontrada [bold red] Failed [/bold red]')

      
  

def igPost( bgPlatform, loopPlatform, loopPlatformProducto):
   
   
   global productos_link
   mainPlatform = 'img/armado/' + campama + 'post-ig.png'
   if devInfo:
      productos_link = []
      productos_link.append(0)
   for j in range(len(productos_link)):
      
     
      producto_img = Image.open('image_with_bg/image_' + str(j) + '.png').convert('RGBA')
      producto_img = producto_img.resize(loopPlatformProducto[0])

      armado = Image.open(mainPlatform).convert('RGBA')
      
      background = Image.new('RGB', (loopPlatform[0]), (255, 255, 255))
      img_w, img_h = producto_img.size
      bg_w, bg_h = armado.size

      offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2 - 90)
      offsetVertical = ((bg_h - img_h) // 2)
      offsetHorizontal = ((bg_w - img_w) // 2)

      canvas = ImageDraw.Draw(armado)   

      font = ImageFont.truetype('Pangram-ExtraBold.otf', 40)
      font2 = ImageFont.truetype('Pangram-Light.otf', 38)
      font3 = ImageFont.truetype('Pangram-ExtraBold.otf', 58)

      fontMarca = ImageFont.truetype('Pangram-Light.otf', 27)
      fontCategoria = ImageFont.truetype('Pangram-Regular.otf', 30)
      # if one line


      titulo = 'Baloncesto Resbalín' if devInfo else nombre[j]
      marca = 'Fisher Price' if devInfo else  marcas[j]
      categoria =  'jueguetes de exterior' if devInfo else categorias[j]
      categoria = categoria.lower()
      if devInfo:
         precio = '13.000'
      else:
         if precioOfertas[j] == 0:
            precio = ''
         else:
            precio = precioOfertas[j].replace('$', '').replace('$', '')
      

      cuadradito = Image.open('cuadradito.png').convert('RGBA')
      tw, th = canvas.textsize(precio, font=font3)
      cuadradito = cuadradito.resize((tw + 100 , th + 30))
      cuadraditoW = (bg_w - cuadradito.size[0]) // 2

      diffTitulo = textwrap.wrap(titulo, width=28)
      
      if len(diffTitulo) == 1:
         diff = 0
         diffCuadrito = offsetVertical  + img_h + 130
         diffCategoria = offsetVertical  + img_h + 40
         diffMarca = offsetVertical  + img_h
         diffPrecio =  diffCuadrito + 7
      elif len(diffTitulo) == 2:
         diff = 0
         diffCuadrito = offsetVertical  + img_h + 130
         diffCategoria = offsetVertical  + img_h + 59
         diffMarca = offsetVertical  + img_h + 20
         diffPrecio =  diffCuadrito + 7
      else:
         diff = 135
         diffCuadrito = 110
         diffCategoria = 75
         diffPrecio = 0




      x.draw_multiple_line_text3(armado, 29, titulo, 'Pangram-ExtraBold.otf', 45, '#3B369F', offsetVertical + img_h - 100, 0, 28, 0)
      x.draw_multiple_line_text3(armado, 29, marca, 'Pangram-Regular.otf', 34, '#3B369F', diffMarca, 0, 20, 0)
      x.draw_multiple_line_text3(armado, 29, categoria, 'Pangram-Regular.otf', 38, '#3B369F', diffCategoria, 0, 28, 0)
      armado.paste(armado, (0,0))
      armado.paste(producto_img, offset, producto_img)
      armado.paste(cuadradito, (int(cuadraditoW),  diffCuadrito), cuadradito)


      x.draw_multiple_line_text(armado, '$' + precio, font3, '#FFF', diffPrecio, push="center")

     
      if dev:
         grid(armado)
      else:
         if devInfo:
            armado.show()
      armado.show()
      armado.save('save/postig_' + str(j) + '.png')
      
   taskStatus('Making image for Instagram Post', len(productos_link))
      

     
def postFB( bgPlatform, loopPlatform, loopPlatformProducto):
   global productos_link
   mainPlatform = 'img/armado/' + campama + 'post-fb.png'
   index = 1
   ramdonN = randrange(10)
   if devInfo:
      productos_link = []
      productos_link.append(0)
   for j in range(len(productos_link)):

      random = str(index)
      producto_img = Image.open('image/' + str(j) + '.png').convert('RGBA')
      producto_img = producto_img.resize(loopPlatformProducto[index])

      armado = Image.open(mainPlatform).convert('RGBA')
      background = Image.new('RGB', (loopPlatform[index]), (255, 255, 255))
      img_w, img_h = producto_img.size
      bg_w, bg_h = armado.size

      offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
      offsetVertical = ((bg_h - img_h) // 2)
      offsetHorizontal = ((bg_w - img_w) // 2)

      canvas = ImageDraw.Draw(armado)   

      font = ImageFont.truetype('Pangram-ExtraBold.otf', 40)
      font2 = ImageFont.truetype('Pangram-Light.otf', 38)
      font3 = ImageFont.truetype('Pangram-ExtraBold.otf', 58)

      fontMarca = ImageFont.truetype('Pangram-Light.otf', 27)
      fontCategoria = ImageFont.truetype('Pangram-Regular.otf', 30)
      
      titulo = 'Baloncesto Resbalín' if devInfo else nombre[j]
      marca = 'Fisher Price' if devInfo else  marcas[j]
      categoria =  'Juguetes de exterior' if devInfo else categorias[j]
      categoria = categoria.lower()
      if devInfo:
         precio = '130.000'
      else:
         if precioOfertas[j] == 0:
            precio = ''
         else:
            precio = precioOfertas[j].replace('$', '')
      

      cuadradito = Image.open('cuadradito.png').convert('RGBA')
      tw, th = canvas.textsize(precio, font=font3)
      cuadradito = cuadradito.resize((tw + 100 , th + 40))
      #cuadraditoW = (bg_w - cuadradito.size[0]) // 2
      cuadraditoW = bg_w // 2 
      cuadraditoW = cuadraditoW + (cuadradito.size[0] // 2)
      diffTitulo = textwrap.wrap(titulo, width=20)

      if len(diffTitulo) == 1:
         
         diff = 280
         diffCuadrito = 135
         diffCategoria = 45
         diffTituloH = 92
         categoriaHDIFF = 0
         diffMarquita = 0
         
      elif len(diffTitulo) == 2:
         diff = 180
         diffCuadrito = 235
         diffCategoria = 60
         diffTituloH = 22
         categoriaHDIFF = 100
         diffMarquita = 20
      elif len(diffTitulo) == 3:
         diff = 130
         diffCuadrito = 285
         diffCategoria = 90
         diffTituloH = 22
         categoriaHDIFF = 170
         diffMarquita = 50
      elif len(diffTitulo) == 4:
      
         diff = 130
         diffCuadrito = 110
         diffCategoria = 75
         diffTituloH = 92
         categoriaHDIFF = 0
         diffMarquita = 0

     
         
      mitadFondo1 = bg_w // 2
      mitadFondo2 = mitadFondo1 // 2
      total = bg_w // 2
   
 

      x.draw_multiple_line_text3(armado, 29, titulo, 'Pangram-ExtraBold.otf', 45, '#3B369F', offsetVertical + 90, total, 20, 9)
      x.draw_multiple_line_text3(armado, 36, marca, 'Pangram-Regular.otf', 35, '#3B369F', offsetVertical + 220 + diffMarquita, total, 20)
      x.draw_multiple_line_text3(armado, 45, categoria, 'Pangram-Regular.otf', 35, '#3B369F', offsetVertical + 220 + diffCategoria, total, 20)

      armado.paste(armado, (0,0))
      armado.paste(producto_img, (30 ,(bg_h - img_h) // 2 + 80), producto_img)
      
         
      centerR = (bg_w // 2) 
      centerR = centerR + centerR // 2
      centerR = centerR - cuadradito.size[0] // 2
      s = 0
      for i in precio:
         s += 1
      if s == 7:
         centerR2 =   30
      else:
         centerR2 =   35

      
      armado.paste(cuadradito, ( centerR + 15, offsetVertical + diff + diffCuadrito  + 10), cuadradito)

     
      x.draw_multiple_line_text(armado, '$' + precio, font3, '#FFF', offsetVertical + diff + diffCuadrito  + 23, push="precio-fb", width=img_w, positionCenter=centerR2 + centerR + 15)

      if dev:
         armado.show()
      else:
         if devInfo:
            armado.show()
      armado.show()
      armado.save('save/postigFB_' + str(j) + '.png')
   taskStatus(task='Making image for Facebook Post', limit=len(productos_link))
     
def story( bgPlatform, loopPlatform, loopPlatformProducto):
   global productos_link
   mainPlatform = 'img/armado/' + campama + 'story.png'
   index = 2
   ramdonN = 9
   if devInfo:
      productos_link = []
      productos_link.append(0)
  
   for j in range(len(productos_link)):
      
     
      random = str(index)
      producto_img = Image.open('image/' + str(j) + '.png').convert('RGBA')
      producto_img = producto_img.resize(loopPlatformProducto[index])

      armado = Image.open(mainPlatform).convert('RGBA')
      background = Image.new('RGB', (loopPlatform[index]), (255, 255, 255))
      img_w, img_h = producto_img.size
      bg_w, bg_h = armado.size

      offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
      offsetVertical = ((bg_h - img_h) // 2)
      offsetHorizontal = ((bg_w - img_w) // 2)

      canvas = ImageDraw.Draw(armado)   

      font = ImageFont.truetype('Pangram-ExtraBold.otf', 60)
      font2 = ImageFont.truetype('Pangram-Light.otf', 38)
      font3 = ImageFont.truetype('Pangram-ExtraBold.otf', 78)

      fontMarca = ImageFont.truetype('Pangram-Light.otf', 37)
      fontCategoria = ImageFont.truetype('Pangram-Bold.otf', 40)


      titulo = 'Baloncesto Resbalín Baloncesto Resbalín' if devInfo else nombre[j]
      marca = 'Fisher Price' if devInfo else  marcas[j]
      categoria =  'Juguetes de exterior' if devInfo else categorias[j]
      categoria = categoria.lower()
      if devInfo:
         precio = '13.000'
      else:
         if precioOfertas[j] == 0:
            precio = ''
         else:
            precio = precioOfertas[j].replace('$', '')
      
      

      cuadradito = Image.open('cuadradito.png').convert('RGBA')
      tw, th = canvas.textsize(precio, font=font3)
      cuadradito = cuadradito.resize((tw + 120 , th + 75))
      cuadraditoW = (bg_w - cuadradito.size[0]) // 2

      diffTitulo = textwrap.wrap(titulo, width=28)
      
      if len(diffTitulo) == 1:
         diff = 65
         diffCuadrito = 290
         diffCategoria = - 160
         diffTituloH = - 130
         diffMarca = - 120
      elif len(diffTitulo) == 2:
         diff = 65
         diffCuadrito = 290
         diffCategoria = - 80
         diffTituloH = - 110
         diffMarca = - 40
      else:
         diff = 120
         diffCuadrito = 290
         diffCategoria =  - 165
         diffMarca = -5
         diffTituloH = - 100

      x.draw_multiple_line_text3(armado, 29, titulo, 'Pangram-ExtraBold.otf', 65, '#3B369F', offsetVertical + img_h - 20 + diffTituloH, 0, 28, 0)
      x.draw_multiple_line_text3(armado, 29, marca, 'Pangram-Regular.otf', 45, '#3B369F', offsetVertical + img_h + diff + diffMarca , 0, 28, 0)
      x.draw_multiple_line_text3(armado, 29, categoria, 'Pangram-Regular.otf', 45, '#3B369F', offsetVertical + img_h + diff + 90 + diffCategoria , 0, 28, 0)


      armado.paste(armado, (0,0))
      armado.paste(producto_img, ((bg_w - img_w) // 2 , (bg_h - img_h) // 2 - 140), producto_img)
      armado.paste(cuadradito, (int(cuadraditoW), offsetVertical + img_h + diff + diffCuadrito  - 200), cuadradito) 


      x.draw_multiple_line_text(armado, '$' + precio, font3, '#FFF', offsetVertical + img_h + diff + diffCuadrito - 175 , push="center")

      if dev:
         armado.show()
      else:
         if devInfo:
            armado.show()
      armado.show()
      armado.save('save/story_' + str(j) + '.png')
   taskStatus(task='Making image for Story', limit=len(productos_link))

def push( bgPlatform, loopPlatform, loopPlatformProducto):
   global productos_link
   mainPlatform = 'img/armado/' + campama + 'push_.png'

   index = 3
   ramdonN = 7
   if devInfo:
      productos_link = []
      productos_link.append(0)
   for j in range( len(productos_link)):
      producto_img = Image.open('image/' + str(j) + '.png').convert('RGBA')
      producto_img = producto_img.resize(loopPlatformProducto[index])


      armado = Image.open(mainPlatform).convert('RGBA')


      diffArmado = 800
      diffArmado2 = armado.size[0]
      diffArmado2 = (diffArmado2 - diffArmado)
    

      background = Image.new('RGB', (loopPlatform[index]), (255, 255, 255))
      img_w, img_h = producto_img.size
      bg_w, bg_h = armado.size

      
      center = bg_w  // 2  // 2


      offset = ((center + bg_w  //  2) - img_w  + 70, 50)
      offsetVertical = ((bg_h - img_h) // 2)
      offsetHorizontal = ((bg_w - img_w) // 2)

      canvas = ImageDraw.Draw(armado)   

      
      font = ImageFont.truetype('Pangram-ExtraBold.otf', 30)
      font2 = ImageFont.truetype('Pangram-Light.otf', 25)
      font3 = ImageFont.truetype('Pangram-ExtraBold.otf', 58)

      fontMarca = ImageFont.truetype('Pangram-Light.otf', 20)
      fontCategoria = ImageFont.truetype('Pangram-Bold.otf', 30)


      titulo = 'Muñeca de fronzen' if devInfo else nombre[j]
      marca = 'Marca' if devInfo else  marcas[j]
      categoria =  'Categoria' if devInfo else categorias[j]
      if devInfo:
         precio = '13.000'
      else:
         if precioOfertas[j] == 0:
            precio = ''
         else:
            precio = precioOfertas[j].replace('$', '')
      

      cuadradito = Image.open('cuadradito.png').convert('RGBA')
      tw, th = canvas.textsize(precio, font=font3)
      cuadradito = cuadradito.resize((tw + 100, th + 40))
      cuadraditoW = (bg_w - cuadradito.size[0]) // 2

      diffTitulo = textwrap.wrap(titulo, width=28)
      
      
      if len(diffTitulo) == 1:
         diff = 35
         diffCuadrito = 20
         diffCategoria = - 120
         diffMarca = - 120
         diffTituloH =  bg_h // 2 - 160
      else:
         diff = 35
         diffCuadrito = 20
         diffCategoria = - 120
         diffMarca = - 120
         diffTituloH =  bg_h // 2 - 160

      centeer = (bg_w // 2) - cuadradito.size[0] // 2
      centeer = bg_w  - bg_w // 2 //  2 - cuadradito.size[0] // 2

      newCenterText = bg_w  - bg_w // 2 //  2
      tw3, th3 = canvas.textsize(categoria, font=font2)

      total = diffArmado2
   

      x.draw_multiple_line_text3(armado, 29, titulo, 'Pangram-ExtraBold.otf', 37, '#3B369F', offsetVertical + 0, 680, 20, 9)
      x.draw_multiple_line_text(armado, marca, fontMarca, '#3b369f', offsetVertical + img_h - diff + diffMarca, push="pushreal", width=img_w)
      x.draw_multiple_line_text(armado, categoria, fontCategoria, '#3b369f', offsetVertical + img_h + diff - 45 + diffCategoria, push="pushreal", width=img_w, positionCenter=newCenterText )

      armado.paste(armado, (0,0))
     
      armado.paste(producto_img, (diffArmado2 + img_w // 2 , offsetVertical), producto_img)
      centerR = bg_w - (800 // 2) + (tw // 2) - tw
      centerR = diffArmado2 + diffArmado // 2 

      s = 0
      for i in precio:
         s += 1
      if s == 7:
         tt =  67
      else:
         tt =  70
      print(s)


      diffArmado = 800
      diffArmado2 = armado.size[0]
      diffArmado2 = (diffArmado2 - diffArmado)
      #centerR = bg_w - (782 // 2) + (tw // 2) - tw
      centerR = diffArmado2 + diffArmado // 2 
      centerR2 = centerR + ( bg_w - centerR) // 2
      centerR = centerR + ( bg_w - centerR) // 2
      centerR = centerR - cuadradito.size[0] // 2


      #armado.paste(cuadradito, ((center + bg_w  //  2) - img_w  + 185, offsetVertical + img_h + diff + diffCuadrito  - 20), cuadradito)
      armado.paste(cuadradito, (centerR - 20  , offsetVertical + img_h + diff + diffCuadrito  - 122), cuadradito)

      x.draw_multiple_line_text(armado, '$' + precio, font3, '#FFF', offsetVertical + img_h + diff + diffCuadrito  - 109, push="right5", width=img_w, positionCenter=centerR + (tw // 2) - 20 - tt ) 

     

      if dev:
         armado.show()
      else:
         if devInfo:
            armado.show()
      armado.show()
      armado.save('save/push_' + str(j) + '.png')
   taskStatus(task='Making image for Push', limit=len(productos_link))
          
def fbHorizontal( bgPlatform, loopPlatform, loopPlatformProducto):
   global productos_link
   mainPlatform = 'img/armado/' + campama + 'fb-horizontal.png'
   index = 4
   ramdonN = 7
   if devInfo:
      productos_link = []
      productos_link.append(0)
   for j in range(len(productos_link)):
      producto_img = Image.open('image/' + str(j) + '.png').convert('RGBA')
      ww, hh = loopPlatformProducto[index]
      producto_img = producto_img.resize((ww - 80, hh - 80))


      armado = Image.open(mainPlatform).convert('RGBA')


      diffArmado = 782
      diffArmado2 = armado.size[0]
      diffArmado2 = diffArmado2 - diffArmado
    
      
      background = Image.new('RGB', (loopPlatform[index]), (255, 255, 255))
      img_w, img_h = producto_img.size
      bg_w, bg_h = armado.size

      
      center = bg_w  // 2  // 2


      offset = ((center + bg_w  //  2) - img_w  + 70, 50)
      offsetVertical = ((bg_h - img_h) // 2)
      offsetHorizontal = ((bg_w - img_w) // 2)

      canvas = ImageDraw.Draw(armado)   

      font = ImageFont.truetype('Pangram-ExtraBold.otf', 30)
      font2 = ImageFont.truetype('Pangram-Light.otf', 25)
      font3 = ImageFont.truetype('Pangram-ExtraBold.otf', 58)

      fontMarca = ImageFont.truetype('Pangram-Light.otf', 20)
      fontCategoria = ImageFont.truetype('Pangram-Bold.otf', 30)
      titulo = 'Muñeca de fronze' if devInfo else nombre[j]
      marca = 'Marca' if devInfo else  marcas[j]
      categoria =  'categoria' if devInfo else categorias[j]
      if devInfo:
         precio = '13.000'
      else:
         if precioOfertas[j] == 0:
            precio = ''
         else:
            precio = precioOfertas[j].replace('$', '')
    
      

      cuadradito = Image.open('cuadradito.png').convert('RGBA')
      tw, th = canvas.textsize(precio, font=font3)
      cuadradito = cuadradito.resize((tw + 80, th + 50))
      cuadraditoW = (bg_w - cuadradito.size[0]) // 2 

      diffTitulo = textwrap.wrap(titulo, width=16)
      
    
      if len(diffTitulo) == 1:
         diff = 35
         diffCuadrito = 20
         diffCategoria = - 140
         diffMarca = - 160
         diffTituloH =  150
      elif len(diffTitulo) == 3:
         diff = 35
         diffCuadrito = 20
         diffCategoria = - 140
         diffMarca = - 160
         diffTituloH =  150
      else:
         diff = 35
         diffCuadrito = 20
         diffCategoria = - 140
         diffMarca = - 160
         diffTituloH =  150
      
      print(len(diffTitulo))

      centeer = (bg_w // 2) - cuadradito.size[0] // 2
      centeer = bg_w  - bg_w // 2 //  2 - cuadradito.size[0] // 2

      newCenterText = bg_w  - bg_w // 2 //  2
      tw3, th3 = canvas.textsize(categoria, font=font2)

      
      diffArmado = 782
      diffArmado2 = armado.size[0]
      diffArmado2 = (diffArmado2 - diffArmado)
      #centerR = bg_w - (782 // 2) + (tw // 2) - tw
      centerR = diffArmado2 + diffArmado // 2 
      centerR2 = centerR + ( bg_w - centerR) // 2
      centerR = centerR + ( bg_w - centerR) // 2
      centerR = centerR - cuadradito.size[0] // 2
     
   
      
      x.draw_multiple_line_text(armado, titulo, font, '#3b369f', diffTituloH, push="preciofbhorizontal", width=img_w, positionCenter=centerR2 )
      x.draw_multiple_line_text(armado, marca, font2, '#3b369f', offsetVertical + img_h - diff + diffMarca, push="pushfb", width=img_w - 80)
      x.draw_multiple_line_text(armado, categoria, fontCategoria, '#3b369f', offsetVertical + img_h + diff - 45 + diffCategoria, push="pushfb", width=img_w - 80, positionCenter=newCenterText )

      armado.paste(armado, (0,0))
      centrito = bg_w - 782 + 84
      armado.paste(producto_img, (centrito, offsetVertical), producto_img)
     
      

      s = 0
      for i in precio:
         s += 1
      if s == 7:
         tt = 87
        
      else:
          tt = 85
      
      



     
      #armado.paste(cuadradito, ((center + bg_w  //  2) - img_w  + 185, offsetVertical + img_h + diff + diffCuadrito  - 20), cuadradito)
      #armado.paste(cuadradito, (centerR, offsetVertical + img_h + diff + diffCuadrito  - 122), cuadradito)
      armado.paste(cuadradito, (centerR, offsetVertical + img_h + diff + diffCuadrito  - 120), cuadradito)

      x.draw_multiple_line_text(armado,  "$" + precio, font3, '#FFF', offsetVertical + img_h + diff + diffCuadrito  - 100, push="right5", width=img_w, positionCenter=centerR + tw // 2 - tt) 

     
      if dev:
         armado.show()
      else:
         if devInfo:
            armado.show()
         armado.save('save/fbHorizontal_' + str(j) + '.png')
         armado.show()
   taskStatus(task='Making image for Facebook Horizontal', limit=len(productos_link))
    
