try:
    import Tkinter as tk # this is for python2
except:
    import tkinter as tk # this is for python3
from PIL import ImageDraw, Image, ImageTk
import sys

window = tk.Tk(className="bla")

image = Image.open(sys.argv[1] if len(sys.argv) >=2 else "img/armado/elementos-fbhorizontal.png")
image = image.resize((1000, 800), Image.ANTIALIAS)
canvas = tk.Canvas(window, width=image.size[0], height=image.size[1])
canvas.pack()
image_tk = ImageTk.PhotoImage(image)

canvas.create_image(image.size[0]//2, image.size[1]//2, image=image_tk)

def callback(event):
    print("clicked at: ", event.x, event.y)

canvas.bind("<Button-1>", callback)
tk.mainloop()