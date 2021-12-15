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


dev = False
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
  


def grid(img):
   step_count = 10

   if len(sys.argv) == 2:
      step_count = int(sys.argv[1])

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
def crwalUrl():


   workbook = xlrd.open_workbook("link.xlsx","rb")
   sheets = workbook.sheet_names()
   productos_link = []

   for sheet_name in sheets:
      sh = workbook.sheet_by_name(sheet_name)
      for rownum in range(9, sh.nrows):
         row_valaues = sh.row_values(rownum)
         productos_link.append(row_valaues[0])

   

   taskStatus(task='Extract Info from Excel', limit=len(productos_link))


   
   for i in range(len(productos_link)):
      options = Options()
      options.add_argument('--headless')
      options.add_argument('--disable-gpu')
      driver = webdriver.Chrome(executable_path='./chromedriver')
      driver.set_window_position(0, 0)
      driver.get(productos_link[i])

      print('[bold blue] Index: [/bold blue]' + str(i) )
      print()
      nombre.append(driver.find_element_by_class_name('h1-alert').text)

      imagen = driver.find_element_by_class_name('lazy-image-cloud')
      imagen = imagen.get_attribute('src')
   
      imagenes.append(imagen)
      print('[bold red] Crawl URL: [/bold red]' + productos_link[i] )

      response = requests.get(imagen)
      Image.open(BytesIO(response.content)).convert('RGBA').save('image/' + str(i) + '.png')

      print('[bold blue] Quitando fondo de la imagen... [/bold blue]')
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


      
  

def igPost(total_producto, bgPlatform, loopPlatform, loopPlatformProducto):
   
   mainPlatform = 'img/armado/post-ig.png'
   
   for j in range(len(total_producto)):
      
     
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

      font = ImageFont.truetype('Pangram-Bold.otf', 44)
      font2 = ImageFont.truetype('Pangram-Light.otf', 38)
      font3 = ImageFont.truetype('Pangram-Light.otf', 38)
      titulo = nombre[j] 
      marca = marcas[j]
      categoria = "Esta es una categoria"
      precio = "$ 90.000"
      

      cuadradito = Image.open('cuadradito.png').convert('RGBA')
      tw, th = canvas.textsize(precio, font=font3)
      cuadradito = cuadradito.resize((tw + 100 , th + 20))
      cuadraditoW = (bg_w - cuadradito.size[0]) // 2

      diffTitulo = textwrap.wrap(titulo, width=28)
      
      if len(diffTitulo) == 1:
         diff = 5
         diffCuadrito = 75
         diffCategoria = 75
      else:
         diff = 135
         diffCuadrito = 110
         diffCategoria = 75



      x.draw_multiple_line_text(armado, titulo, font, '#191919', offsetVertical + img_h - 70, push="center")
      x.draw_multiple_line_text(armado, marca, font2, '#191919', offsetVertical + img_h + diff, push="center")
      x.draw_multiple_line_text(armado, categoria, font2, '#191919', offsetVertical + img_h + diff + 50, push="center" )

      armado.paste(armado, (0,0))
      armado.paste(producto_img, offset, producto_img)
      armado.paste(cuadradito, (int(cuadraditoW), offsetVertical + img_h + diff + diffCuadrito  + 35), cuadradito)


      x.draw_multiple_line_text(armado, precio, font3, '#FFF', offsetVertical + img_h + diff + diffCuadrito + 41, push="center")

     

      armado.show()
      if dev:
         grid(armado)
   taskStatus('Making image for Instagram Post', len(total_producto))
      

     
def postFB(total_producto, bgPlatform, loopPlatform, loopPlatformProducto):
   mainPlatform = 'img/armado/post-fb.png'
   index = 1
   ramdonN = randrange(10)
   for j in range(9, len(total_producto)):

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

      font = ImageFont.truetype('Pangram-Bold.otf', 36)
      font2 = ImageFont.truetype('Pangram-Light.otf', 25)
      font3 = ImageFont.truetype('Pangram-Light.otf', 34)
      titulo = "CASTILLO DE HOGWARTS Y " 
      marca = "Cubic Fun"
      categoria = "Puzzles y rompecabezas"
      precio = "$ 190.000"
      

      cuadradito = Image.open('cuadradito.png').convert('RGBA')
      tw, th = canvas.textsize(precio, font=font3)
      cuadradito = cuadradito.resize((tw + 100 , th + 40))
      #cuadraditoW = (bg_w - cuadradito.size[0]) // 2
      cuadraditoW = bg_w // 2 
      cuadraditoW = cuadraditoW + (cuadradito.size[0] // 2)
      diffTitulo = textwrap.wrap(titulo, width=28)

      if len(diffTitulo) == 1:
         
         diff = 280
         diffCuadrito = 135
         diffCategoria = 15
         diffTituloH = 92
         categoriaHDIFF = 0
         
      elif len(diffTitulo) == 2:
         diff = 180
         diffCuadrito = 235
         diffCategoria = - 86
         diffTituloH = 22
         categoriaHDIFF = 100
      elif len(diffTitulo) == 3:
         diff = 130
         diffCuadrito = 285
         diffCategoria = - 175
         diffTituloH = 22
         categoriaHDIFF = 170
      elif len(diffTitulo) == 4:
      
         diff = 130
         diffCuadrito = 110
         diffCategoria = 75
         diffTituloH = 92
         categoriaHDIFF = 0
     
         

 

      x.draw_multiple_line_text(armado, titulo, font, '#191919', offsetVertical + 90 + diffTituloH, push="fbpush", width=img_w, positionCenter=600)
      x.draw_multiple_line_text(armado, marca, font2, '#191919', offsetVertical + diff - diffCategoria,push="fbpush", width=img_w, positionCenter=600)
      x.draw_multiple_line_text(armado, categoria, font2, '#191919', offsetVertical + diff + 40 + categoriaHDIFF, push="fbpush", width=img_w, positionCenter=600)

      armado.paste(armado, (0,0))
      armado.paste(producto_img, (30 ,(bg_h - img_h) // 2 + 80), producto_img)
      armado.paste(cuadradito, (int(cuadraditoW - 22), offsetVertical + diff + diffCuadrito  + 10), cuadradito)


      x.draw_multiple_line_text(armado, precio, font3, '#FFF', offsetVertical + diff + diffCuadrito  + 26, push="fbpush", width=img_w, positionCenter=600)

     

      armado.show()
   taskStatus(task='Making image for Facebook Post', limit=len(total_producto))
     
def story(total_producto, bgPlatform, loopPlatform, loopPlatformProducto):
   mainPlatform = 'img/armado/story.png'
   index = 2
   ramdonN = 9
   for j in range(ramdonN, len(total_producto)):

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

      font = ImageFont.truetype('Pangram-Bold.otf', 56)
      font2 = ImageFont.truetype('Pangram-Light.otf', 50)
      font3 = ImageFont.truetype('Pangram-Light.otf', 90)
      titulo = "Esta es la descripci" 
      marca = "Esto es una marca"
      categoria = "Esta es una categoria"
      precio = "$ 90.000"
      

      cuadradito = Image.open('cuadradito.png').convert('RGBA')
      tw, th = canvas.textsize(precio, font=font3)
      cuadradito = cuadradito.resize((tw + 80 , th + 30))
      cuadraditoW = (bg_w - cuadradito.size[0]) // 2

      diffTitulo = textwrap.wrap(titulo, width=28)
      
      if len(diffTitulo) == 1:
         diff = 65
         diffCuadrito = 290
         diffCategoria = - 130
         diffTituloH = - 140
         diffMarca = - 120
      else:
         diff = 120
         diffCuadrito = 290
         diffCategoria =  - 165
         diffMarca = -5
         diffTituloH = - 100

      x.draw_multiple_line_text(armado, titulo, font, '#191919', offsetVertical + img_h - 20 + diffTituloH, push="center")
      x.draw_multiple_line_text(armado, marca, font2, '#191919', offsetVertical + img_h + diff + diffMarca , push="center")
      x.draw_multiple_line_text(armado, categoria, font2, '#191919', offsetVertical + img_h + diff + 90 + diffCategoria, push="center" )

      armado.paste(armado, (0,0))
      armado.paste(producto_img, ((bg_w - img_w) // 2 , (bg_h - img_h) // 2 - 140), producto_img)
      armado.paste(cuadradito, (int(cuadraditoW), offsetVertical + img_h + diff + diffCuadrito  - 200), cuadradito) 


      x.draw_multiple_line_text(armado, precio, font3, '#FFF', offsetVertical + img_h + diff + diffCuadrito - 190 , push="center")

     

      armado.show()
   taskStatus(task='Making image for Story', limit=len(total_producto))

def push(total_producto, bgPlatform, loopPlatform, loopPlatformProducto):
   mainPlatform = 'img/armado/push_.png'

   index = 3
   ramdonN = 7
   for j in range(9, len(total_producto)):
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

      font = ImageFont.truetype('Pangram-Bold.otf', 22)
      font2 = ImageFont.truetype('Pangram-Light.otf', 20)
      font3 = ImageFont.truetype('Pangram-Light.otf', 38)
      titulo = "APPLE MACBOOK PRO 13.3 I5 2.50GHZ 8GB RAM" 
      marca = "Apple"
      categoria = "Notebooks"
      precio = "$ 490.009"
      

      cuadradito = Image.open('cuadradito.png').convert('RGBA')
      tw, th = canvas.textsize(precio, font=font3)
      cuadradito = cuadradito.resize((tw + 40, th + 50))
      cuadraditoW = (bg_w - cuadradito.size[0]) // 2

      diffTitulo = textwrap.wrap(titulo, width=28)
      
      
      if len(diffTitulo) == 1:
         diff = 65
         diffCuadrito = 260
         diffCategoria = 75
         diffTituloH =  - 420
         diffMarca = 0
      else:
         diff = 35
         diffCuadrito = 20
         diffCategoria = - 180
         diffMarca = - 120
         diffTituloH =  - 160

      centeer = (bg_w // 2) - cuadradito.size[0] // 2
      centeer = bg_w  - bg_w // 2 //  2 - cuadradito.size[0] // 2

      newCenterText = bg_w  - bg_w // 2 //  2
      tw3, th3 = canvas.textsize(categoria, font=font2)
   

      x.draw_multiple_line_text(armado, titulo, font, '#191919', offsetVertical + img_h - 90 +  diffTituloH, push="pushreal", width=img_w)
      x.draw_multiple_line_text(armado, marca, font2, '#191919', offsetVertical + img_h - diff + diffMarca, push="pushreal", width=img_w)
      x.draw_multiple_line_text(armado, categoria, font2, '#191919', offsetVertical + img_h + diff - 45 + diffCategoria, push="pushreal", width=img_w, positionCenter=newCenterText )

      armado.paste(armado, (0,0))
     
      armado.paste(producto_img, (diffArmado2 + img_w // 2 , offsetVertical), producto_img)
      centerR = bg_w - (800 // 2) + (tw // 2) - tw
      centerR = diffArmado2 + diffArmado // 2 

      s = 0
      for i in precio:
         s += 1
      if s == 9:
         centerR = centerR + img_w  - cuadradito.size[0] + 45
      else:
         centerR = centerR + img_w  - cuadradito.size[0] + 35


      #armado.paste(cuadradito, ((center + bg_w  //  2) - img_w  + 185, offsetVertical + img_h + diff + diffCuadrito  - 20), cuadradito)
      armado.paste(cuadradito, (centerR  , offsetVertical + img_h + diff + diffCuadrito  - 122), cuadradito)

      x.draw_multiple_line_text(armado, precio, font3, '#FFF', offsetVertical + img_h + diff + diffCuadrito  - 100, push="right5", width=img_w, positionCenter=centerR + cuadradito.size[0] // 2 - tw // 2) 

     

      armado.show()
   taskStatus(task='Making image for Push', limit=len(total_producto))
          
def fbHorizontal(total_producto, bgPlatform, loopPlatform, loopPlatformProducto):
   mainPlatform = 'img/armado/fb-horizontal.png'
   index = 4
   ramdonN = 7
   for j in range(9, len(total_producto)):
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

      font = ImageFont.truetype('Pangram-Bold.otf', 22)
      font2 = ImageFont.truetype('Pangram-Light.otf', 20)
      font3 = ImageFont.truetype('Pangram-Light.otf', 38)
      titulo = "APPLE MACBOOK PRO 13.3 I5 2.50GHZ 8GB RAM" 
      marca = "Apple"
      categoria = "Notebooks"
      precio = "$ 490.009"
      

      cuadradito = Image.open('cuadradito.png').convert('RGBA')
      tw, th = canvas.textsize(precio, font=font3)
      cuadradito = cuadradito.resize((tw + 40, th + 50))
      cuadraditoW = (bg_w - cuadradito.size[0]) // 2 

      diffTitulo = textwrap.wrap(titulo, width=28)
      
    
      if len(diffTitulo) == 1:
         diff = 65
         diffCuadrito = 260
         diffCategoria = 75
         diffTituloH =  - 420
         diffMarca = 0
      else:
         diff = 35
         diffCuadrito = 20
         diffCategoria = - 180
         diffMarca = - 120
         diffTituloH =  - 160

      centeer = (bg_w // 2) - cuadradito.size[0] // 2
      centeer = bg_w  - bg_w // 2 //  2 - cuadradito.size[0] // 2

      newCenterText = bg_w  - bg_w // 2 //  2
      tw3, th3 = canvas.textsize(categoria, font=font2)
   
      
      x.draw_multiple_line_text(armado, titulo, font, '#191919', offsetVertical + img_h - 90 +  diffTituloH, push="pushfb", width=img_w)
      x.draw_multiple_line_text(armado, marca, font2, '#191919', offsetVertical + img_h - diff + diffMarca, push="pushfb", width=img_w)
      x.draw_multiple_line_text(armado, categoria, font2, '#191919', offsetVertical + img_h + diff - 45 + diffCategoria, push="pushfb", width=img_w, positionCenter=newCenterText )

      armado.paste(armado, (0,0))
      centrito = bg_w - 782 + 84
      armado.paste(producto_img, (centrito, offsetVertical), producto_img)
      centerR = bg_w - (782 // 2) + (tw // 2) - tw
      

      s = 0
      for i in precio:
         s += 1
      if s == 9:
         centerR = centerR + img_w  - cuadradito.size[0] + 45
      else:
         centerR = centerR + img_w  - cuadradito.size[0] + 35



      centerR =   bg_w - 417  
      centerR = bg_w - centerR 
      centerR = (bg_w - cuadradito.size[0]) // 2 + 743 // 2 + 40
   
     
      #armado.paste(cuadradito, ((center + bg_w  //  2) - img_w  + 185, offsetVertical + img_h + diff + diffCuadrito  - 20), cuadradito)
      #armado.paste(cuadradito, (centerR, offsetVertical + img_h + diff + diffCuadrito  - 122), cuadradito)
      armado.paste(cuadradito, (centerR, offsetVertical + img_h + diff + diffCuadrito  - 122), cuadradito)

      x.draw_multiple_line_text(armado, precio, font3, '#FFF', offsetVertical + img_h + diff + diffCuadrito  - 100, push="right5", width=img_w, positionCenter=centerR + cuadradito.size[0] // 2 - tw // 2) 

     

      armado.show()
   taskStatus(task='Making image for Facebook Horizontal', limit=len(total_producto))
    
