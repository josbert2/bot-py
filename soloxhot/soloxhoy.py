from PIL import Image, ImageDraw, ImageFont
import textwrap
import qrcode
from openpyxl import Workbook
import xlrd
import master as x


#Incluir categoria



def igPost(total_producto, bgPlatform, loopPlatform, loopPlatformProducto):
   print('Generando imagenes para Instagram post...')
   mainPlatform = 'img/armado/post-ig.png'
   for j in range(len(total_producto)):
     
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
      titulo = "Esta es la descripci" 
      marca = "Esto es una marca"
      precio = "$ 90.000"
      

      cuadradito = Image.open('cuadradito.png').convert('RGBA')
      tw, th = canvas.textsize(precio, font=font3)
      cuadradito = cuadradito.resize((tw + 20 , th + 20))
      cuadraditoW = (bg_w - cuadradito.size[0]) // 2

      diffTitulo = textwrap.wrap(titulo, width=28)
      
      if len(diffTitulo) == 1:
         diff = 65
         diffCuadrito = 75
      else:
         diff = 135
         diffCuadrito = 115

      x.draw_multiple_line_text(armado, titulo, font, '#FFF', offsetVertical + img_h)
      x.draw_multiple_line_text(armado, marca, font2, '#FFF', offsetVertical + img_h + diff)

      armado.paste(armado, (0,0))
      armado.paste(producto_img, offset, producto_img)
      armado.paste(cuadradito, (int(cuadraditoW), offsetVertical + img_h + diff + diffCuadrito), cuadradito)

      x.draw_multiple_line_text(armado, precio, font3, '#FFF', offsetVertical + img_h + diff + diffCuadrito + 5)
      armado.show()

def postFb():
   print('holaaa')     

def donwloadImageAndRemoveBg():
   print('holaaa')  