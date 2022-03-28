#! /usr/bin/python

from PIL import Image
import sys

Image.MAX_IMAGE_PIXELS = None


# Provide file name as first arg.
img    = Image.open(sys.argv[1]) 
pixels = img.load()
width  = img.size[0]
height = img.size[1]
print ( f"size: w {width} h {height}" )

# Find max and min pixel values.
max_val = 0
min_val = 100000
max_val_x = 0
max_val_y = 0
min_val_x = 0
min_val_y = 0

for y in range ( height ) :
  if 0 == (y % 100) :
    print ( f"Finding min and max: row {y}" )
  for x in range ( width ) :
    val = pixels [ x, y ]
    if val > max_val :
      max_val = val
      max_val_x = x
      max_val_y = y
    if val < min_val :
      min_val = val
      min_val_x = x
      min_val_y = y

print ( f"max_val == {max_val} at {max_val_x} {max_val_y}" )
print ( f"min_val == {min_val} at {min_val_x} {min_val_y}" )

altitude_range = max_val - min_val
meters_per_gray_value = altitude_range / 255

print ( f"altitude_range {altitude_range}  meters_per_gray_value {meters_per_gray_value} " )


# Make the new image, with max pixel translated to white.
new_img = Image.new ( mode = "RGB",
                      size = (width, height),
                      color = ( 0, 0, 0 ) )
new_pixels = new_img.load()

for y in range ( height ) :
  if 0 == (y % 100) :
    print ( f"Making new image: row {y}" )
  for x in range ( width ) :
    val = pixels [ x, y ]
    # print ( f" val {val} minus min {val-min_val} dbgvpm {(val - min_val) / meters_per_gray_value}" )
    new_val = int ( (val - min_val) / meters_per_gray_value)
    if new_val > 255 :
      print ( f"new_val {new_val}" )
      new_val = 255
    new_pixels [ x, y ] = ( new_val, new_val, new_val )

# And there you go.
new_img.save ( "new_img.tif" )


