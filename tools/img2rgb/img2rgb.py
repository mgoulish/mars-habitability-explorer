#! /usr/bin/python

from PIL import Image


# Turn an image into a list of numbers stored in a file.
# The first two numbers are width and height.
# Then each pixel is stored, 
# one pixel per line in scanline order,
# R G B.

img = Image.open ( '../../data/mola/data.jpg', 'r')
f = open ( './rgb.txt', "w" )
f.write ( f"{img.size[0]} {img.size[1]}\n" )
for pixel in list ( img.getdata() ) :
  f.write ( f"{pixel[0]} {pixel[1]} {pixel[2]}\n" )
f.close()
