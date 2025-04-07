from random import randint
from PIL import Image


val = randint(1001, 1031)
img = Image.open(f"coverpages/{val}.png")
img.show()
