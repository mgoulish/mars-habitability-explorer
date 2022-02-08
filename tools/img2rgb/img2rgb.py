#! /usr/bin/python

import sys
from PIL import Image


# Turn an image into a list of numbers stored in a file.
# The first two numbers are width and height.
# Then each pixel is stored, 
# one pixel per line in scanline order,
# R G B.

file_name = sys.argv[1]
img = Image.open ( file_name, 'r')
f = open ( './rgb.txt', "w" )
f.write ( f"{img.size[0]} {img.size[1]}\n" )
for pixel in list ( img.getdata() ) :
  f.write ( f"{pixel[0]} {pixel[1]} {pixel[2]}\n" )
f.close()
