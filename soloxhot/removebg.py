from rembg.bg import remove
import numpy as np
import io
from PIL import Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

input_path = '5fc06120f1032985858809.jpeg'
output_path = 'out.png'

f = np.fromfile(input_path)
result = remove(f)
img = Image.open(io.BytesIO(result)).convert("RGBA")
img.save(output_path)