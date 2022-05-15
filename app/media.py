import secrets
from PIL import Image
from os import path
from . import app

class Picture:
    def __init__(self, path):
        self.path = path
        self.name = 'default.jpeg'

    def rename_picture(self):
        random_hex = secrets.token_hex(8)
        _, f_ext = path.splitext(self.path.filename)
        self.name = random_hex + f_ext

    def save_picture(self, folder: str):
        picture_for_save = Image.open(self.path)
        self.path = path.join(app.root_path, 'static', folder, self.name)
        picture_for_save.save(self.path)


class ProfilePicture(Picture):

    def resize_picture(self, output_size: tuple[int, int] = (125, 125)):
        picture_for_resize = Image.open(self.path)
        picture_for_resize.thumbnail(output_size)


class PostPicture(Picture):

    def resize_picture(self, output_size: tuple[int, int] = (970, 970)):
        picture_for_resize = Image.open(self.path)
        if picture_for_resize.size < output_size:
            picture_for_resize.resize(output_size)
        else:
            picture_for_resize.thumbnail(output_size)