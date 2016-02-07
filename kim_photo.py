
from bs4 import BeautifulSoup
import requests
import os

PATH = os.getcwd()
FILE = PATH + "/test.jpg"
url = 'http://kimjongunlookingatthings.tumblr.com'

def get_kim():
    '''Get the HTML code from the kimjongunlookingatthings tumblr account'''
    print("[+]\tGetting photo from {}...".format(url))
    get = requests.get(url)
    return get.content


def get_newest_photo():
    '''Get HTML of the newest photo on the kimjongunlookingatthings tumblr account page'''
    soup = BeautifulSoup(get_kim(), "html5lib")
    photo = soup.find(class_="photo")
    return photo

class KimPhoto:
    '''A class of photos of Kim
    
    Arguments
    
    photo: A bs4.BeautifulSoup object containing the data regarding what Kim is looking at'''
    
    def __init__(self, photo):
        try:
            type(photo) == 'bs4.element.Tag'
        except:
            raise TypeError("Argument must be a bs4.BeautifulSoup object")
        self.title = photo['alt']
        self.src = photo['src']
        self.__str__ = "photo of Kim {}".format(self.title)
        self.get_jpg_data()
    
    def get_jpg_data(self):
        image = requests.get(self.src)
        with open(FILE, 'wb') as f:
            f.write(image.content)
            f.close()           
    
