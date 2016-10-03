from .box import box
from espelhos_sonoros.service import app

class Box(object):

    def __init__(self):
        self.address = 'localhost'
        self.name = ''

    def update(self, address, other):
        self.address = address
        self.name = other['name']

box(Box(), app)
