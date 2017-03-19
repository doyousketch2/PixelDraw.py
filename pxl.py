##=========================================================
##  pxl.py                                      11 Mar 2017
##
##  turn pixels into polygons, from spritesheets to Blender
##
##  Eli Leigh Innis
##  Twitter :  @ Doyousketch2
##  Email :  Doyousketch2 @ yahoo.com
##
##  GNU GPLv3                 gnu.org/licenses/gpl-3.0.html
##=========================================================
##  libs  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from time import time
from math import floor

##=========================================================
##  script  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def draw(W, H, pixeldata, metadata, dimensions):
  looptimer  = time()       ##  initialize timer
  array  = list(pixeldata)  ##  convert raw pixeldata into an array

  newline  = 1
  vert  = 1                 ##  vertex counter
  vertices  = []
  faces  = ['\n\n']
  foundcolors  = []
  colors  = []

  blendergrid  = 16    ##  8 grid divisions in both directions from origin = 16
  blenderunit  = 100   ##  .obj files apprently use centimeters, 100 = blenderunit
  maxwidth  = blendergrid * blenderunit

  if W > H:  scale  = maxwidth / W
  else:      scale  = maxwidth / H

  halfpxl  = scale / 2
  offx  = -scale * W / 2
  offy  = scale * H / 2

  ##  the default grid is +8 & -8, along X and Y.
  ##  find the largest of those two  (W or H)
  ##  then use a scale-factor for the polygons
  ##  to center pixels within that 16 blender-unit square

  ##  metadata['alpha'] is either True or False
  if metadata['alpha']:   bpp  = 4  ##  RGBA
  else:                   bpp  = 3  ##  RGB
                      ##  bpp  = bits per plane
  #  print(str(bpp))
  #  print(metadata)

  ##  background  = top-left corner pixel
  background  = previousColor  = [R, G, B]  = array[0][0:3]
  print('\nWidth: %s,  Height: %s,  Background:  r%s g%s b%s' % (W, H, R, G, B))

##-------------------------------------v
##  find number of colors
  C= 0
  Y  = 0
  while Y < H:
    yy  = array[Y]
    X  = 0
    while X < W:
      xx  = X * bpp
      color  = [R, G, B]  = yy[xx : xx + 3]
      if color != background and color not in foundcolors:
        foundcolors .append(color)
        if C == 0:  print('Found %s color' % C, end = '\r')
        else:       print('Found %s colors' % C, end = '\r')
        C += 1
      X += 1
    Y += 1

  print('Found %s colors (excluding background)\n' % len(foundcolors))
##-------------------------------------^

  ww  = W / 2
  hh  = H / 2

  C= 1   ##  init loop counter
  numcolors  = len(foundcolors)

##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##  main color loop

  for color in foundcolors:
    R, G, B  = color

##-------------------------------------v
##  looptimer to print info
    looptime  = floor((time() - looptimer) * 100) / 100
    if C == 1:  print('Color: %s of: %s   Init took: %s secs          r%s g%s b%s' % (C, numcolors, looptime, R, G, B), end = '\r')
    else:       print('Color: %s of: %s   last color took: %s secs   r%s g%s b%s' % (C, numcolors, looptime, R, G, B), end = '\r')
    # if looptime > 2: Y = H; continue    ##  break out of loop, for testing
    looptimer  = time()   ##  re-init timer for next loop
    C += 1
##-------------------------------------
##  determine color info for this layer

##  divide by 255 to convert colors from (0 - 255) range into (0 - 1) range
##  floor(num * 100) / 100   drops digits off of floats to 2 decimal places

    rr  = floor((R / 255) * 100) / 100
    gg  = floor((G / 255) * 100) / 100
    bb  = floor((B / 255) * 100) / 100
    colorstring  = 'r%s g%s b%s' % (R, G, B)

    colors .append('newmtl %s' % colorstring)
    colors .append('Kd %s %s %s\n' % (rr, gg, bb))
    faces .append('usemtl %s' % colorstring)

    brightness  = (R+R + G+G+G + B) / 6

##    our eyes are sensitive to shades of red and even moreso to green,
##    so extra samples of them are taken when averaging luminosity value.
##    stackoverflow.com/a/596241                using fast approximation

    Z  = brightness / 50
    zz  = floor((Z / 10) * 10000) / 20

##-------------------------------------v
##  iterate through pixels

    Y  = 0
    while Y < H:
      yy  = array[Y]

      X  = 0
      while X < W:
        ##if metadata['indexed']:
          ##index  = array[Y][X]

        xx  = X * bpp
        pxlcolor  = yy[xx : xx + 3]

        if pxlcolor != color:
          previousColor  = pxlcolor
        else:
          #  print(str(X) + ', ' + str(Y) + ',  ' + str(color))
          offsetX  = offx + X * scale
          offsetY  = offy - Y * scale

##  floor(num * 10000) / 10000  drops digits off of floats to 4 decimal places

          if pxlcolor == color and previousColor == pxlcolor and newline == 0:
            top  = floor((offsetY + halfpxl) * 10000) / 10000
            right  = floor((offsetX + halfpxl) * 10000) / 10000
            bottom  = floor((offsetY - halfpxl) * 10000) / 10000

##  replace last two vertices in list, so we get RunLengthEncoding effect
            vertices[-2]  = ('v %s %s %s' % (right, bottom, zz))
            vertices[-1]  = ('v %s %s %s' % (right,  top,   zz))

          elif pxlcolor == color:
            newline  = 0

            top  = floor((offsetY + halfpxl) * 10000) / 10000
            left  = floor((offsetX - halfpxl) * 10000) / 10000
            right  = floor((offsetX + halfpxl) * 10000) / 10000
            bottom  = floor((offsetY - halfpxl) * 10000) / 10000

            vertices .append('v %s %s %s' % (left,   top,   zz))
            vertices .append('v %s %s %s' % (left,  bottom, zz))
            vertices .append('v %s %s %s' % (right, bottom, zz))
            vertices .append('v %s %s %s' % (right,  top,   zz))

            faces .append('f %s %s %s %s' % (vert, vert + 1, vert + 2, vert + 3))

            previousColor  = pxlcolor
            vert += 4
        X += 1
      newline  = 1
      Y += 1
  return vertices, faces, colors


##=============================================================
##  eof  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
