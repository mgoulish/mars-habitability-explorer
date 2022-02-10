#! /usr/bin/python

from PIL import Image

width  = 3600
height = 1800

img = Image.new ( mode = "RGB",
                  size = (width, height),
                  color = ( 0, 0, 0 ) )

pixels = img.load ( )

# Get the data!
fp = open ( 'data.csv', 'r' )
lines = fp.readlines()

for line in lines :
  words = line.split ( ',' ) 
  long  = (1800 + int(float(words[1]) * 10.0)) % 3600
  lat   = 180 - int((float(words[2])+90.0) * 10)
  pixels [ long, lat ] = ( 255, 255, 255 )

img.save ( "caves.tif" )

