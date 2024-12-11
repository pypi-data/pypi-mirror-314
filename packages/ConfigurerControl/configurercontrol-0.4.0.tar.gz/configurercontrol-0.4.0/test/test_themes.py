import unittest
from ConfigurerControl import images
from PIL import Image, ImageFont, ImageDraw


class TestType(unittest.TestCase):
    def test_CidPar_sort(self):
        print(images.stop)

    def test_create_default(self):
        new_img = Image.new('RGB', (100, 100), 'white')
        font = ImageFont.load_default(size=50)
        pencil = ImageDraw.Draw(new_img)
        pencil.text((50, 50), '?', anchor="ms", font=font, fill='red')
        new_img.show()
