from PIL import Image, ImageDraw, ImageFont, ImageFile
import textwrap
import qrcode
from openpyxl import Workbook
import xlrd

import numpy as np
import cv2

import io
from rembg.bg import remove






def center_with_letter_spacing(text, lines, draw, image_width, line_width, font, y_text, difference):
    desired_width_of_text = 1
    left_side_padding = difference

    header_text = text

    lines = lines
    total_text_width, total_text_height = draw.textsize( "Sample Text asdsdads", font=font )
    width_difference = desired_width_of_text - total_text_width
    gap_width = - 3
    xpos = left_side_padding

    for letter in header_text:
        draw.text( (xpos + (image_width - line_width) / 2, y_text),letter, '#3b369f', font=font)
        letter_width, letter_height = draw.textsize(letter, font=font)
        xpos += letter_width + gap_width





def draw_multiple_line_text(image, text, font, text_color, text_start_height, push, width=None, positionCenter=None):
    '''
    From unutbu on [python PIL draw multiline text on image](https://stackoverflow.com/a/7698300/395857)
    '''
    draw = ImageDraw.Draw(image)
    image_width, image_height = image.size
    y_text = text_start_height
    if push == 'right':
        lines = textwrap.wrap(text, width=28)
    elif push == 'fbpush':
        lines = textwrap.wrap(text, width=20)
    elif push == 'pushreal':
        lines = textwrap.wrap(text, width=20)
    elif push == 'preciofbhorizontal':
        lines = textwrap.wrap(text, width=16)
    else:
        lines = textwrap.wrap(text, width=28)


    for line in lines:
        line_width, line_height = font.getsize(line)
        ##draw.text(((image_width - line_width) / 2, y_text), 
        #          line, font=font, fill=text_color)
        #  image_width // 2 + width // 2 
        if push == 'right':

        
            draw.text(((image_width - line_width + image_width // 2 + width // 2 - 100 ) / 2 , y_text), line, font=font, fill=text_color)
        elif push == 'right2':
            draw.text((12 + positionCenter, y_text), line, font=font, fill=text_color)
        elif push == 'right5':
            draw.text((positionCenter, y_text), line, font=font, fill=text_color)
        elif push == 'right3':
            draw.text((positionCenter, y_text), line, font=font, fill=text_color)
        elif push == 'fbpush':
           center = (image_width - line_width) // 2
           draw.text((center + 270, y_text), line, font=font, fill=text_color)
        elif push == 'pushreal':
            draw.text(((image_width - line_width + image_width // 2 + width // 2 - 0 ) / 2 , y_text), line, font=font, fill=text_color)
        elif push == 'pushfb':
            draw.text(((image_width - line_width + image_width // 2 + width // 2 + 80 ) / 2 , y_text), line, font=font, fill=text_color)
        
        elif push == 'precio-fb':
            draw.text((positionCenter, y_text), line, font=font, fill=text_color)
        elif push == 'preciofbhorizontal':
            draw.text(((2000 - line_width) / 2 , y_text), line, font=font, fill=text_color)
        elif push == 'centerc':
            
            center_with_letter_spacing(text, lines, draw, image_width, line_width, font, y_text, difference=20)
        else:
            draw.text(((image_width - line_width) / 2, y_text), line, font=font, fill=text_color)
        y_text += line_height
def remobeBG(image, i=0):
    #from rembg.bg import remove
    ImageFile.LOAD_TRUNCATED_IMAGES = True

    input_path = image
    output_path = './image_with_bg/image_' + str(i) + '.png'

    f = np.fromfile(input_path)
    result = remove(f)
    img = Image.open(io.BytesIO(result)).convert("RGBA")
    img.save(output_path)

def removeBG2(image, i=0):
    # load image
    input_path = image
    img = cv2.imread(image)
    output_path = './image_with_bg/image_' + str(i) + '.png'

    # convert to graky
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # threshold input image as mask
    mask = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)[1]

    # negate mask
    mask = 255 - mask

    # apply morphology to remove isolated extraneous noise
    # use borderconstant of black since foreground touches the edges
    kernel = np.ones((3,3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # anti-alias the mask -- blur then stretch
    # blur alpha channel
    mask = cv2.GaussianBlur(mask, (0,0), sigmaX=2, sigmaY=2, borderType = cv2.BORDER_DEFAULT)

    # linear stretch so that 127.5 goes to 0, but 255 stays 255
    mask = (2*(mask.astype(np.float32))-255.0).clip(0,255).astype(np.uint8)

    # put mask into alpha channel
    result = img.copy()
    result = cv2.cvtColor(result, cv2.COLOR_BGR2BGRA)
    result[:, :, 3] = mask

    # save resulting masked image
    cv2.imwrite(output_path, result)

    # display result, though it won't show transparency
    #cv2.imshow("INPUT", img)
    #cv2.imshow("GRAY", gray)
    #cv2.imshow("MASK", mask)
    #cv2.imshow("RESULT", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()







def draw_multiple_line_text2(image, text, font, text_color, text_start_height, push, width=None, positionCenter=None, category=28):
   
    
    draw = ImageDraw.Draw(image)
    image_width, image_height = image.size
    y_text = text_start_height
    lines = textwrap.wrap(text, width=category)


    for line in lines:
        line_width, line_height = font.getsize(line)
        draw.text(((image_width - line_width) / 2, y_text), line, font=font, fill=text_color)
        y_text += line_height

def draw_multiple_line_text3(image,  diffTitulo, text, fontFamily, fontWidth, text_color, text_start_height, WIDTHLOG=None, widthFontText=None, diffHeight=None):

   
    font = ImageFont.truetype(fontFamily, fontWidth)
    draw = ImageDraw.Draw(image)
    y_text = text_start_height
    image_width, image_height = image.size
    header_text = text
    lines = textwrap.wrap(header_text, width=widthFontText)
    if diffTitulo == 0:
        diffTitulo = 0
    else:
        diffTitulo = diffTitulo 
    x = 0
    xpos = 0
    checkIndex = 0
  
    if diffHeight != None:
        diffHeight = diffHeight
    else:
        diffHeight = 0
    
    for idx, letter in enumerate(lines):
        line_width, line_height = font.getsize(letter)
        letter_width, letter_height = draw.textsize(letter, font=font)
        checkIndex = idx
        diffHorizontal = WIDTHLOG
        if checkIndex == 0:
            xpos = 0
            xpoy = -1  + diffHeight
        elif checkIndex == 1:
            xpos = 0
            xpoy = - 3 + diffHeight
        elif checkIndex == 2:
            xpos = 0
            xpoy = -3 + diffHeight
        elif checkIndex == 3:
            xpos = 0
            xpoy = 3 + diffHeight

        for i in range(0, len(letter)):
            letter_width, letter_height = draw.textsize(letter[i], font=font)
          
            if letter_width == 36:
                xpos += - 1 
            draw.text((( ( diffHorizontal  // 2) + int(diffTitulo) + (image_width -  line_width) / 2) + xpos , y_text), letter[i], text_color, font=font, spacing=10)
            xpos += letter_width - 3
            
        
        y_text += line_height + xpoy




import wx
app = wx.App()
 
def width_and_height_calculator_in_pixel(txt, fontname, fontsize):
    dc   = wx.ScreenDC()
   #dc.SetFont(...) # todo: https://wxpython.org/Phoenix/docs/html/wx.DC.html#wx.DC.SetFont
    size = dc.GetTextExtent(txt)
    return size
 




def draw_multiple_line_text4(image,  diffTitulo, text, fontFamily, fontWidth, text_color, text_start_height, WIDTHLOG=None, widthFontText=None, diffHeight=None):

   
    font = ImageFont.truetype(fontFamily, fontWidth)
    draw = ImageDraw.Draw(image)
    y_text = text_start_height
    image_width, image_height = image.size
    header_text = text
    lines = textwrap.wrap(header_text, width=widthFontText)
    text_size = width_and_height_calculator_in_pixel(header_text, "Calibri", 11)        
    if diffTitulo == 0:
        diffTitulo = 0
    else:
        diffTitulo = diffTitulo 
    x = 0
    xpos = 0
    checkIndex = 0
  
    if diffHeight != None:
        diffHeight = diffHeight
    else:
        diffHeight = 0
    
    for idx, letter in enumerate(lines):
        line_width, line_height = font.getsize(letter)
        letter_width, letter_height = draw.textsize(letter, font=font)
        letter_width2, letter_height2 = draw.textsize(letter, font=font)
        checkIndex = idx
        diffHorizontal = WIDTHLOG
        #remove space 

        line_width, line_height = font.getsize(letter)

  
        for i in range(0, len(letter)):
           
            letter_width, letter_height = draw.textsize(letter[i], font=font)
          
            if letter_width == 36:
                xpos += - 1 
       
            #draw.text((( ( diffHorizontal  // 2) + int(diffTitulo) + (image_width -  line_width) / 2) + xpos , y_text), letter[i], text_color, font=font, spacing=10)
            draw.text(((image_width - line_width) // 2 + 35  +  xpos, y_text), letter[i], text_color, font=font, spacing=10)
            xpos += letter_width - 3
            
        
        y_text += line_height








def draw_text_center_letter_spacing(image, text, fontFamily, fontWidth, fontColor, y_text):
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(fontFamily, fontWidth)
    image_width, image_height = image.size
    text_size = width_and_height_calculator_in_pixel(text, "Calibri", 11)
   
    text_width, text_height = draw.textsize(text, font=font)
    draw.text(((image_width - text_width) // 2, y_text), text, font=font, fill=fontColor, spacing=10)
    




def draw_left(image, text, fontFamily, fontWidth, fontSize, fontColor, y_text, x_text, diffHeight=None):
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(fontFamily, fontSize)
    if diffHeight != None:
        diffHeight = diffHeight
    else:
        diffHeight = 0
    image_width, image_height = image.size
    text_size = width_and_height_calculator_in_pixel(text, "Calibri", 11)
   
    text_width, text_height = draw.textsize(text, font=font)
    lines = textwrap.wrap(text, width=fontWidth)
  
    for line in lines:
        line_width, line_height = font.getsize(line)
        draw.text((x_text, y_text), line, font=font, fill=fontColor)
        y_text += line_height + diffHeight




def draw_multiple_line_text_one_line(image,  diffTitulo, text, fontFamily, fontWidth, text_color, text_start_height, WIDTHLOG=None, widthFontText=None, diffHeight=None, diffLineal=None):

   
    font = ImageFont.truetype(fontFamily, fontWidth)
    draw = ImageDraw.Draw(image)
    y_text = text_start_height
    image_width, image_height = image.size
    header_text = text
    lines = textwrap.wrap(header_text, width=widthFontText)
    if diffTitulo == 0:
        diffTitulo = 0
    else:
        diffTitulo = diffTitulo 
    x = 0
    xpos = 0
    checkIndex = 0
  
    if diffHeight != None:
        diffHeight = diffHeight
    else:
        diffHeight = 0
    
    if diffLineal != None:
        diffLineal = diffLineal
    else:
        diffLineal = 0

    for idx, letter in enumerate(lines):
        line_width, line_height = font.getsize(letter)
        letter_width, letter_height = draw.textsize(letter, font=font)
        checkIndex = idx
   
        diffHorizontal = WIDTHLOG
        if checkIndex == 0:
            if checkIndex == 0:
                xpos = 0
                xpoy = -1  + diffHeight
            elif checkIndex == 1:
                xpos = 0
                xpoy = - 3 + diffHeight
            elif checkIndex == 2:
                xpos = 0
                xpoy = -3 + diffHeight
            elif checkIndex == 3:
                xpos = 0
                xpoy = 3 + diffHeight

            for i in range(0, len(letter)):
                letter_width, letter_height = draw.textsize(letter[i], font=font)
            
                if letter_width == 36:
                    xpos += - 1 
                if letter_width == 10:
                    xpos += 8
                draw.text((( diffLineal - ( diffHorizontal  // 2) + int(diffTitulo) + (image_width -  line_width) / 2) + xpos , y_text), letter[i], text_color, font=font, spacing=10)
                xpos += letter_width - 4.5
                
            
            y_text += line_height + xpoy


def draw_multiple_line_text_one_line_marca(image,  diffTitulo, text, fontFamily, fontWidth, text_color, text_start_height, WIDTHLOG=None, widthFontText=None, diffHeight=None, diffLineal=None):

   
    font = ImageFont.truetype(fontFamily, fontWidth)
    draw = ImageDraw.Draw(image)
    y_text = text_start_height
    image_width, image_height = image.size
    header_text = text
    lines = textwrap.wrap(header_text, width=widthFontText)
    if diffTitulo == 0:
        diffTitulo = 0
    else:
        diffTitulo = diffTitulo 
    x = 0
    xpos = 0
    checkIndex = 0
  
    if diffHeight != None:
        diffHeight = diffHeight
    else:
        diffHeight = 0
    
    if diffLineal != None:
        diffLineal = diffLineal
    else:
        diffLineal = 0

    for idx, letter in enumerate(lines):
        line_width, line_height = font.getsize(letter)
        letter_width, letter_height = draw.textsize(letter, font=font)
        checkIndex = idx

        diffHorizontal = WIDTHLOG
        if checkIndex == 0:
            if checkIndex == 0:
                xpos = 0
                xpoy = -1  + diffHeight
            elif checkIndex == 1:
                xpos = 0
                xpoy = - 3 + diffHeight
            elif checkIndex == 2:
                xpos = 0
                xpoy = -3 + diffHeight
            elif checkIndex == 3:
                xpos = 0
                xpoy = 3 + diffHeight

            for i in range(0, len(letter)):
                letter_width, letter_height = draw.textsize(letter[i], font=font)
            
                if letter_width == 27:
                    xpos += 2
                    print(letter[i])
                if letter_width == 26:
                    xpos += 2
                if letter_width == 10:
                    xpos += 8

                draw.text((( 16 + ( diffHorizontal  // 2)  + (image_width -  line_width) / 2) + xpos , y_text), letter[i], text_color, font=font, spacing=10)
                xpos += letter_width - 4.5
                
            
            y_text += line_height + xpoy



def draw_multiple_line_text_one_line_category(image,  diffTitulo, text, fontFamily, fontWidth, text_color, text_start_height, WIDTHLOG=None, widthFontText=None, diffHeight=None, diffLineal=None):

   
    font = ImageFont.truetype(fontFamily, fontWidth)
    draw = ImageDraw.Draw(image)
    y_text = text_start_height
    image_width, image_height = image.size
    header_text = text
    lines = textwrap.wrap(header_text, width=widthFontText)
    if diffTitulo == 0:
        diffTitulo = 0
    else:
        diffTitulo = diffTitulo 
    x = 0
    xpos = 0
    checkIndex = 0
  
    if diffHeight != None:
        diffHeight = diffHeight
    else:
        diffHeight = 0
    
    if diffLineal != None:
        diffLineal = diffLineal
    else:
        diffLineal = 0

    for idx, letter in enumerate(lines):
        line_width, line_height = font.getsize(letter)
        letter_width, letter_height = draw.textsize(letter, font=font)
        checkIndex = idx

        diffHorizontal = WIDTHLOG
        if checkIndex == 0:
            if checkIndex == 0:
                xpos = 0
                xpoy = -1  + diffHeight
            elif checkIndex == 1:
                xpos = 0
                xpoy = - 3 + diffHeight
            elif checkIndex == 2:
                xpos = 0
                xpoy = -3 + diffHeight
            elif checkIndex == 3:
                xpos = 0
                xpoy = 3 + diffHeight

            for i in range(0, len(letter)):
                letter_width, letter_height = draw.textsize(letter[i], font=font)
            
                if letter_width == 28 and letter[i] != "b":
                    xpos += 2
                if letter_width == 28 and letter[i] == "b":
                    xpos += 2
                if letter_width == 10:
                    xpos += 8
                print(letter_width)

                draw.text((( 16 + ( diffHorizontal  // 2)  + (image_width -  line_width) / 2) + xpos , y_text), letter[i], text_color, font=font, spacing=10)
                xpos += letter_width - 4.5
                
            
            y_text += line_height + xpoy







def draw_left_titulo_pushfb(image, text, fontFamily, fontWidth, fontSize, fontColor, y_text, x_text, diffHeight=None):
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(fontFamily, fontSize)
    if diffHeight != None:
        diffHeight = diffHeight
    else:
        diffHeight = 0
    image_width, image_height = image.size
    text_size = width_and_height_calculator_in_pixel(text, "Calibri", 11)
   
    text_width, text_height = draw.textsize(text, font=font)
    lines = textwrap.wrap(text, width=fontWidth)
 
    for idx, line in enumerate(lines):
        if idx == 0:
            line_width, line_height = font.getsize(line)
            draw.text((x_text, y_text), line, font=font, fill=fontColor)
            y_text += line_height + diffHeight
