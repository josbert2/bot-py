from PIL import Image, ImageDraw, ImageFont
import textwrap
import qrcode
from openpyxl import Workbook
import xlrd
import master as x
from random import randrange
    
from time import sleep
import time
from alive_progress import alive_bar, config_handler
from rich import print
from rich.console import Console

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
  



#Incluir categoria

def crwalUrl():


   workbook = xlrd.open_workbook("link.xlsx","rb")
   sheets = workbook.sheet_names()
   productos_link = []

   for sheet_name in sheets:
      sh = workbook.sheet_by_name(sheet_name)
      for rownum in range(sh.nrows):
         row_valaues = sh.row_values(rownum)
         productos_link.append(row_valaues[0])

   

  

def igPost(total_producto, bgPlatform, loopPlatform, loopPlatformProducto):
   
   mainPlatform = 'img/armado/elementos-postig.png'
   
   for j in range(9, len(total_producto)):
     
      producto_img = Image.open('image/' + str(j) + '.png').convert('RGBA')
      producto_img = producto_img.resize(loopPlatformProducto[0])

      armado = Image.open(mainPlatform).convert('RGBA')
      background = Image.new('RGB', (loopPlatform[0]), (255, 255, 255))
      img_w, img_h = producto_img.size
      bg_w, bg_h = armado.size

      offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
      offsetVertical = ((bg_h - img_h) // 2)
      offsetHorizontal = ((bg_w - img_w) // 2)

      canvas = ImageDraw.Draw(armado)   

      font = ImageFont.truetype('Pangram-Bold.otf', 48)
      font2 = ImageFont.truetype('Pangram-Light.otf', 38)
      font3 = ImageFont.truetype('Pangram-Light.otf', 38)
      titulo = "Esta es la descripci werwe wtwt wetwe wewe wewewe" 
      marca = "Esto es una marca"
      categoria = "Esta es una categoria"
      precio = "$ 90.000"
      

      cuadradito = Image.open('cuadradito.png').convert('RGBA')
      tw, th = canvas.textsize(precio, font=font3)
      cuadradito = cuadradito.resize((tw + 100 , th + 20))
      cuadraditoW = (bg_w - cuadradito.size[0]) // 2

      diffTitulo = textwrap.wrap(titulo, width=28)
      
      if len(diffTitulo) == 1:
         diff = 65
         diffCuadrito = 75
         diffCategoria = 75
      else:
         diff = 135
         diffCuadrito = 110
         diffCategoria = 75

      x.draw_multiple_line_text(armado, titulo, font, '#FFF', offsetVertical + img_h, push="center")
      x.draw_multiple_line_text(armado, marca, font2, '#FFF', offsetVertical + img_h + diff, push="center")
      x.draw_multiple_line_text(armado, categoria, font2, '#FFF', offsetVertical + img_h + diff + 50, push="center" )

      armado.paste(armado, (0,0))
      armado.paste(producto_img, offset, producto_img)
      armado.paste(cuadradito, (int(cuadraditoW), offsetVertical + img_h + diff + diffCuadrito  + 35), cuadradito)


      x.draw_multiple_line_text(armado, precio, font3, '#FFF', offsetVertical + img_h + diff + diffCuadrito + 41, push="center")

     

      armado.show()
   taskStatus('Making image for Instagram Post', len(total_producto))
      

     
def postFB(total_producto, bgPlatform, loopPlatform, loopPlatformProducto):
   mainPlatform = 'img/armado/post-fb.png'
   index = 1
   ramdonN = randrange(10)
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

      font = ImageFont.truetype('Pangram-Bold.otf', 36)
      font2 = ImageFont.truetype('Pangram-Light.otf', 31)
      font3 = ImageFont.truetype('Pangram-Light.otf', 34)
      titulo = "Esta es la descripci werwe wtwt wetwe wewe wewewe" 
      marca = "Esto es una marca"
      categoria = "Esta es una categoria"
      precio = "$ 90.000"
      

      cuadradito = Image.open('cuadradito.png').convert('RGBA')
      tw, th = canvas.textsize(precio, font=font3)
      cuadradito = cuadradito.resize((tw + 100 , th + 20))
      cuadraditoW = (bg_w - cuadradito.size[0]) // 2

      diffTitulo = textwrap.wrap(titulo, width=28)
      
      if len(diffTitulo) == 1:
         diff = 65
         diffCuadrito = 75
         diffCategoria = 75
      else:
         diff = 90
         diffCuadrito = 110
         diffCategoria = 75

      x.draw_multiple_line_text(armado, titulo, font, '#FFF', offsetVertical + img_h - 20, push="center")
      x.draw_multiple_line_text(armado, marca, font2, '#FFF', offsetVertical + img_h + diff, push="center")
      x.draw_multiple_line_text(armado, categoria, font2, '#FFF', offsetVertical + img_h + diff + 50, push="center" )

      armado.paste(armado, (0,0))
      armado.paste(producto_img, offset, producto_img)
      armado.paste(cuadradito, (int(cuadraditoW), offsetVertical + img_h + diff + diffCuadrito  + 10), cuadradito)


      x.draw_multiple_line_text(armado, precio, font3, '#FFF', offsetVertical + img_h + diff + diffCuadrito + 18, push="center")

     

      armado.show()
     
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
      titulo = "Esta es la descripci " 
      marca = "Esto es una marca"
      categoria = "Esta es una categoria"
      precio = "$ 90.000"
      

      cuadradito = Image.open('cuadradito.png').convert('RGBA')
      tw, th = canvas.textsize(precio, font=font3)
      cuadradito = cuadradito.resize((tw + 220 , th + 70))
      cuadraditoW = (bg_w - cuadradito.size[0]) // 2

      diffTitulo = textwrap.wrap(titulo, width=28)
      
      if len(diffTitulo) == 1:
         diff = 65
         diffCuadrito = 260
         diffCategoria = 75
      else:
         diff = 140
         diffCuadrito = 260
         diffCategoria = 75

      x.draw_multiple_line_text(armado, titulo, font, '#FFF', offsetVertical + img_h - 20, push="center")
      x.draw_multiple_line_text(armado, marca, font2, '#FFF', offsetVertical + img_h + diff, push="center")
      x.draw_multiple_line_text(armado, categoria, font2, '#FFF', offsetVertical + img_h + diff + 90, push="center" )

      armado.paste(armado, (0,0))
      armado.paste(producto_img, offset, producto_img)
      armado.paste(cuadradito, (int(cuadraditoW), offsetVertical + img_h + diff + diffCuadrito  + 10), cuadradito , push="center") 


      x.draw_multiple_line_text(armado, precio, font3, '#FFF', offsetVertical + img_h + diff + diffCuadrito + 33 , push="center")

     

      armado.show()

def push(total_producto, bgPlatform, loopPlatform, loopPlatformProducto):
   mainPlatform = 'img/armado/push_.png'
   index = 3
   ramdonN = 7
   for j in range(9, len(total_producto)):
      producto_img = Image.open('image/' + str(j) + '.png').convert('RGBA')
      producto_img = producto_img.resize(loopPlatformProducto[index])


      armado = Image.open(mainPlatform).convert('RGBA')
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
      font3 = ImageFont.truetype('Pangram-Light.otf', 25)
      titulo = "APPLE MACBOOK PRO 13.3 I5 2.50GHZ 8GB RAM" 
      marca = "Apple"
      categoria = "Notebooks"
      precio = "$ 499.990"
      

      cuadradito = Image.open('cuadradito.png').convert('RGBA')
      tw, th = canvas.textsize(precio, font=font3)
      cuadradito = cuadradito.resize((tw + 30, th + 10))
      cuadraditoW = (bg_w - cuadradito.size[0]) // 2

      diffTitulo = textwrap.wrap(titulo, width=28)
      
      print(diffTitulo)
      if len(diffTitulo) == 1:
         diff = 65
         diffCuadrito = 260
         diffCategoria = 75
      else:
         diff = 35
         diffCuadrito = 20
         diffCategoria = 5

      centeer = (bg_w // 2) - cuadradito.size[0] // 2
      centeer = bg_w  - bg_w // 2 //  2 - cuadradito.size[0] // 2

      newCenterText = bg_w  - bg_w // 2 //  2
      tw3, th3 = canvas.textsize(categoria, font=font2)
   
      print(newCenterText)

      x.draw_multiple_line_text(armado, titulo, font, '#FFF', offsetVertical + img_h - 90, push="right", width=img_w)
      x.draw_multiple_line_text(armado, marca, font2, '#FFF', offsetVertical + img_h - diff, push="right", width=img_w)
      x.draw_multiple_line_text(armado, categoria, font2, '#FFF', offsetVertical + img_h + diff - 45, push="right", width=img_w, positionCenter=newCenterText )

      armado.paste(armado, (0,0))
      armado.paste(producto_img, offset, producto_img)
      
      #armado.paste(cuadradito, ((center + bg_w  //  2) - img_w  + 185, offsetVertical + img_h + diff + diffCuadrito  - 20), cuadradito)
      armado.paste(cuadradito, (centeer + 10, offsetVertical + img_h + diff + diffCuadrito  - 22), cuadradito)

      x.draw_multiple_line_text(armado, precio, font3, '#FFF', offsetVertical + img_h + diff + diffCuadrito  - 20, push="right2", width=img_w, positionCenter=centeer + 10 )

     

      armado.show()
          
def fbHorizontal(total_producto, bgPlatform, loopPlatform, loopPlatformProducto):
   mainPlatform = 'img/armado/fb-horizontal.png'
   index = 4
   ramdonN = 7
   for j in range(9, len(total_producto)):
      producto_img = Image.open('image/' + str(j) + '.png').convert('RGBA')
      producto_img = producto_img.resize(loopPlatformProducto[index])


      armado = Image.open(mainPlatform).convert('RGBA')
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
      font3 = ImageFont.truetype('Pangram-Light.otf', 25)
      titulo = "APPLE MACBOOK PRO 13.3 I5 2.50GHZ 8GB RAM" 
      marca = "Apple"
      categoria = "Notebooks"
      precio = "$ 499.990"
      

      cuadradito = Image.open('cuadradito.png').convert('RGBA')
      tw, th = canvas.textsize(precio, font=font3)
      cuadradito = cuadradito.resize((tw + 30, th + 10))
      cuadraditoW = (bg_w - cuadradito.size[0]) // 2

      diffTitulo = textwrap.wrap(titulo, width=28)
      
      print(diffTitulo)
      if len(diffTitulo) == 1:
         diff = 65
         diffCuadrito = 260
         diffCategoria = 75
      else:
         diff = 35
         diffCuadrito = 20
         diffCategoria = 5

      centeer = (bg_w // 2) - cuadradito.size[0] // 2
      centeer = bg_w  - bg_w // 2 //  2 - cuadradito.size[0] // 2

      newCenterText = bg_w  - bg_w // 2 //  2
      tw3, th3 = canvas.textsize(categoria, font=font2)
   
      print(newCenterText)

      x.draw_multiple_line_text(armado, titulo, font, '#FFF', offsetVertical + img_h - 90, push="right", width=img_w)
      x.draw_multiple_line_text(armado, marca, font2, '#FFF', offsetVertical + img_h - diff, push="right", width=img_w)
      x.draw_multiple_line_text(armado, categoria, font2, '#FFF', offsetVertical + img_h + diff - 45, push="right", width=img_w, positionCenter=newCenterText )

      armado.paste(armado, (0,0))
      armado.paste(producto_img, offset, producto_img)
      
      #armado.paste(cuadradito, ((center + bg_w  //  2) - img_w  + 185, offsetVertical + img_h + diff + diffCuadrito  - 20), cuadradito)
      armado.paste(cuadradito, (centeer + 47 , offsetVertical + img_h + diff + diffCuadrito  - 22), cuadradito)

      x.draw_multiple_line_text(armado, precio, font3, '#FFF', offsetVertical + img_h + diff + diffCuadrito  - 20, push="right2", width=img_w, positionCenter=centeer + 47 )

     

      armado.show()
    
