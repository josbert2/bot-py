from PIL import Image, ImageDraw, ImageFont
import textwrap
import qrcode
from openpyxl import Workbook
import xlrd
import time
import locale
from currencies import Currency
import locale

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



#

for j in range(len(total_producto)):
   print('valor padre: ' + str(j))
   for i in range(len(platform)):
      print('valor: ' + str(i))
      diffTop = 0
      if i == 2:
         diffTop = 70
      if i == 3:
         diffTop = 220

         


      if i != 10:
         print('Usando plataforma: ' + str(bgPlatform[i]))
         print('Tamaño general: ' + str(loopPlatform[i]))
         
         producto_img = Image.open('image/' + str(j) + '.png').convert('RGBA')
        
      
         if i == 3:
            producto_img = producto_img.resize(loopPlatformProducto[i], Image.ANTIALIAS)
         else:
            producto_img = producto_img.resize(loopPlatformProducto[i])

         #calugin_img = Image.open('soloxhoy-02.png')
         #calugin_sizeW, calugin_imgH = loopPlatform[i]
         #calugin_img = calugin_img.resize((round(calugin_sizeW / 2 - 150), 120))


         armado = Image.open(bgPlatform[i]).convert('RGBA')
         

         
         
         background = Image.new('RGB', (loopPlatform[i]), (255, 255, 255))
         img_w, img_h = producto_img.size
         bg_w, bg_h = armado.size
         if i == 3:
            #diffC = (bg_w - img_w) // 2
            #diffC = diffC + diffC  - diffC  // 2
            #diffC = (bg_w - img_w) // 2 + 200
            ##diffC = (bg_w - diffC // 2) - 100
            center =  bg_w // 3
            center = center // 2
            center = bg_w - center - img_w
            diffC = center
            print(center)
         
            offset = (center, 0)
         elif i == 4:
            center = (bg_w // 2)
            center = center // 2

            vertical = (bg_h // 2)
            vertical = vertical // 2
            print(vertical)


            offset = ( center + (bg_w - img_w) // 2, 0 - vertical // 2 + 50)
         else:
            offset = ((bg_w - img_w) // 2, (bg_h - img_h - 50) // 2 + diffTop)


         canvas = ImageDraw.Draw(armado)   
         if i == 3:             
            font = ImageFont.truetype('Pangram-ExtraBold.otf', size=28)
         elif i == 4:
            font = ImageFont.truetype('Pangram-ExtraBold.otf', size=22)
         else:
            font = ImageFont.truetype('Pangram-ExtraBold.otf', size=48)
         
         if i == 3:             
            font2 = ImageFont.truetype('Pangram-Light.otf', size=20)
         else:
            font2 = ImageFont.truetype('Pangram-Light.otf', size=40)


      
         font3 = ImageFont.truetype('Pangram-ExtraBold.otf', size=70)
         text_width, text_height = canvas.textsize("17-25-2021", font=font)


         titulo = productos_titulo[j].upper()
         marca = marca_titulo[j].upper()
         
         precio = locale.currency(precio_titulo[j], grouping=True)
         precio = precio.replace(',', '.')
         # substring = precio[:-3]
         precio = precio[0:-3]

         cuadradito = Image.open('cuadradito.png').convert('RGBA')
         #cuadradito = cuadradito.resize((round(calugin_sizeW / 2 - 150), 120))
         tw, th = canvas.textsize(precio, font=font3)
         tw1, th1 = canvas.textsize(titulo, font=font)
         cuadradito = cuadradito.resize((tw + 20 , th + 20))

         if i == 3:
            
            lines = textwrap.wrap(titulo, width=50)
         else:
            lines = textwrap.wrap(titulo, width=50)
         current_h, pad = 180, 310

      

         if i == 3:
            alturaTitulo = 0
         else:
            alturaTitulo = (bg_h / 2) + (img_h / 2)


         margin = offset2 = 40
         for line in lines:
            w, h = canvas.textsize(line, font=font)
            if i == 3:
               canvas.text(( diffC,  offset2 + alturaTitulo - 10 + diffTop), line, font = font, fill = "#FFF", align='center')
            elif i == 4:
               canvas.text((center + (bg_w - img_w) // 2,  img_h ), line, font = font, fill = "#FFF", align='center')
            else:
               canvas.text(((bg_w - w) / 2,  alturaTitulo + diffTop), line, font = font, fill = "#FFF")
            offset2 += font.getsize(line)[1]

         lines = textwrap.wrap(marca, width=50)
         current_h, pad = 180, 310

         for line in lines:
            w, h = canvas.textsize(marca, font=font2)
            if i == 3:
               canvas.text((center, alturaTitulo + 70 + diffTop), marca, font = font2, fill = "#FFF")
            elif i == 4:
               tw1, th1 = canvas.textsize(titulo, font=font)
               print(tw1 // 2)
               canvas.text((center + (bg_w - img_w) // 2 + 117,  img_h + 30 ), line, font = font2, fill = "#FFF", align='center')
            else:
               canvas.text(((bg_w - w) / 2, alturaTitulo + 60 + diffTop), marca, font = font2, fill = "#FFF")
            offset2 += font.getsize(marca)[1]


         
            
      
         cuadraditoW = (bg_w - cuadradito.size[0]) // 2
         cuadraditoH = remove_trailing_zeros(floatToString((bg_h // 2) + loopPlatformProducto[i][1] - 130 + diffTop))


         armado.paste(armado, (0,0))
         armado.paste(producto_img, offset, producto_img)
         #armado.paste(calugin_img, (0, 100), calugin_img)

         if i == 3:
            armado.paste(cuadradito,  (diffC, int(alturaTitulo + 140 + diffTop)), cuadradito)
         elif i == 4:
            armado.paste(cuadradito,  (center + (bg_w - img_w) // 2, int(alturaTitulo - 20 + diffTop)), cuadradito)
         else:
            armado.paste(cuadradito,  (int(cuadraditoW), int(alturaTitulo + 140 + diffTop)), cuadradito)
         
         lines = textwrap.wrap(precio, width=50)
         current_h, pad = 180, 310


         
      
         for line in lines:
            w, h = canvas.textsize(precio, font=font3)
            if i == 3:
               canvas.text((diffC, alturaTitulo + 140 + diffTop), precio, font = font3, fill = "#FFF")
            elif i == 4:
               canvas.text((center + (bg_w - img_w) // 2, alturaTitulo - 16), precio, font = font3, fill = "#FFF")
            else:
               canvas.text(((bg_w - w) / 2, alturaTitulo + 140 + diffTop), precio, font = font3, fill = "#FFF")
            offset2 += font.getsize(precio)[1]
         armado.show()
         #(bg_h // 2) + loopPlatformProducto[i][1] - 135 + cuadradito.size[1] / 2 - h / 2
         armado.save('save/' + platform[i] + '_' + str(j) + '_.png')
      else:
         print(i)