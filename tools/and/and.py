#! /usr/bin/python

import sys
from PIL import Image


# Turn an image into a list of numbers stored in a file.
# The first two numbers are width and height.
# Then each pixel is stored, 
# one pixel per line in scanline order,
# R G B.

file_1 = sys.argv[1]
file_2 = sys.argv[2]

img_1 = Image.open ( file_1, 'r')
img_2 = Image.open ( file_2, 'r')

if img_1.size[0] != img_2.size[0] :
  print ( f"Image widths are different: {img_1.size[0]} vs {img_2.size[0]}" )
  sys.exit(1)
print ( f"Image widths: {img_1.size[0]}" )

if img_1.size[1] != img_2.size[1] :
  print ( f"Image heights are different: {img_1.size[1]} vs {img_2.size[1]}" )
  sys.exit(1)
print ( f"Image heights: {img_1.size[1]}" )


pixels_1 = list ( img_1.getdata() )
pixels_2 = list ( img_2.getdata() )

result = Image.new ( 'RGB', ( img_1.size[0], img_1.size[1] ) )

for i in range(len(pixels_1)) :
  if pixels_1[i][0] != 0 and pixels_2[i][0] != 0 :
    pixels_1[i] = (255, 255, 255)
  else :
    pixels_1[i] = (0, 0, 0)
    
result_name = "./result.tif"
result.putdata ( pixels_1 )
result.save ( result_name )
print ( f"Result written to {result_name}." )





