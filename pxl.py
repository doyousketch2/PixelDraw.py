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

def draw(W, H, pixels, meta, gloss=True, dimensions=3):
  looptimer  = time()   ##  initialize timer
  newline  = 0
  vert  = 1             ##  vertex counter
  vertices  = []
  faces  = ['\n\n']
  colors  = []
  foundcolors  = []
  array  = list(pixels)

  if W > H:  scale  = 1600 / W
  else:      scale  = 1600 / H

  halfpxl  = scale / 2
  offsetX  = -scale * W / 2
  offsetY  = scale * H / 2

  ##  the default grid is +8 & -8, along X and Y.
  ##  find the largest of those two  (W or H)
  ##  then use a scale-factor for the polygons
  ##  to center pixels within that 16 blender-unit square

  print('\nWidth: %s,  Height: %s' % (W, H))
  #  print(array[X][Y] / 255)

  ##  meta['alpha'] is either True or False
  if meta['alpha']:   bpp  = 4     ##  RGBA
  else:               bpp  = 3     ##  RGB
                  ##  bpp  = bits per plane
  #  print(str(bpp))
  #  print(meta)

  ##  background  = top-left corner pixel
  background  = previousColor  = [R, G, B]  = array[0][0:3]
  print('Background:  [%s, %s, %s]' % (R, G, B))

##-------------------------------------
##  find number of colors
  Y  = 0
  while Y < H:
    yy  = array[Y]
    X  = 0
    while X < W:
      xx  = X * bpp
      color  = [R, G, B]  = yy[xx : xx + 3]
      if color != background and color not in colors:
        colors .append(color)
      X += 1
    Y += 1

  print('Colors (excluding background): %s\n' % len(colors))
##-------------------------------------

  ww  = W / 2
  hh  = H / 2

  Y  = 0
  while Y < H:
    looptime  = floor((time() - looptimer) * 100) / 100
    if Y == 0:
      print('Line: %s of: %s   Init took: %s secs' % (Y + 1, H, looptime))
    else:
      print('Line: %s of: %s   last line took: %s secs' % (Y + 1, H, looptime))
    # if looptime > 2: Y = H; continue   ##  for testing
    looptimer  = time()   ##  re-init timer for next loop
    yy  = array[Y]

    X  = 0
    while X < W:
      ##if meta['indexed']:
        ##index  = array[Y][X]

      xx  = X * bpp
      color  = [R, G, B]  = yy[xx : xx + 3]

      xo  = offsetX + X * scale
      yo  = offsetY - Y * scale

      if color == background:
        previousColor  = color
      else:
        #  print(str(X) + ', ' + str(Y) + ',  ' + str(color))

        if color == previousColor and newline == 0:
          top  = floor((yo + halfpxl) * 10000) / 10000
          right  = floor((xo + halfpxl) * 10000) / 10000
          bottom  = floor((yo - halfpxl) * 10000) / 10000

          vertices[-2]  = ('v %s %s %s' % (right, bottom, zz))
          vertices[-1]  = ('v %s %s %s' % (right,  top,   zz))

        else:
          newline  = 0
          colorstring  = 'r%s g%s b%s' % (R, G, B)
          brightness  = (R+R + G+G+G + B) / 6
##    our eyes are sensitive to shades of red and even moreso to green,
##    so extra samples of them are taken when averaging luminosity value.
##    stackoverflow.com/a/596241       using fast approximation

          if colorstring not in foundcolors:
            rr  = floor((R / 255) * 100) / 100
            gg  = floor((G / 255) * 100) / 100
            bb  = floor((B / 255) * 100) / 100
            colors .append('newmtl %s' % colorstring)
            colors .append('Kd %s %s %s\n' % (rr, gg, bb))

          Z  = brightness / 50
          zz  = floor((Z / 10) * 10000) / 20

          top  = floor((yo + halfpxl) * 10000) / 10000
          left  = floor((xo - halfpxl) * 10000) / 10000
          right  = floor((xo + halfpxl) * 10000) / 10000
          bottom  = floor((yo - halfpxl) * 10000) / 10000

          vertices .append('v %s %s %s' % (left,   top,   zz))
          vertices .append('v %s %s %s' % (left,  bottom, zz))
          vertices .append('v %s %s %s' % (right, bottom, zz))
          vertices .append('v %s %s %s' % (right,  top,   zz))

          if ('usemtl %s' % colorstring) in faces:
            ci  = colors .index('newmtl %s' % colorstring)
            if ci + 3 < len(colors):
              ci += 2  ##  find next color, get index in faces for that color, skip 'newmtl '
            fi  = faces .index('usemtl %s' % colors[ci][7:])
            faces .insert(fi, 'f %s %s %s %s' % (vert, vert + 1, vert + 2, vert + 3))
          else:
            faces .append('usemtl %s' % colorstring)
            faces .append('f %s %s %s %s' % (vert, vert + 1, vert + 2, vert + 3))

          previousColor  = color
          vert += 4
      X += 1
    newline  = 1
    Y += 1
  return vertices, faces, colors


##=============================================================
##  eof  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
