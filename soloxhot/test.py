from PIL import Image, ImageDraw, ImageFont

color = (255, 244, 41)
text = 'S'

N = 500
size_image = width_image, height_image = N, N

img = Image.new('RGB', size_image, color='white')
font_path = 'Pangram-Bold.otf'
font = ImageFont.truetype(font_path, size=600)
draw = ImageDraw.Draw(img)
width_text, height_text = draw.textsize(text, font)
print(width_text)
offset_x, offset_y = font.getoffset(text)
width_text += offset_x
height_text += offset_y

top_left_x = width_image / 2 - width_text / 2
top_left_y = height_image / 2 - height_text / 2
xy = top_left_x, top_left_y

draw.text(xy, text, font=font, fill=color)

img.show()