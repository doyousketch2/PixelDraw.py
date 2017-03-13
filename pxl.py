##=========================================================
##                                              11 Mar 2017
##  pxl.py
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

import bpy
import bmesh
from time import time
from math import floor
from random import uniform

##=========================================================
##  script  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def draw(W, H, pixels, meta, gloss=True):
  looptimer  = time()   ##  initialize timer
  array  = list(pixels)

  if W > H:  scale  = 16 / W
  else:      scale  = 16 / H

  ##  the default grid is +8 & -8, along X and Y.
  ##  find the largest of those two  (W or H)
  ##  then use a scale-factor for the polygons
  ##  to center pixels within that 16 blender-unit square

  print('Width: ' + str(W) + ', Height: ' + str(H))
  #  print(array[X][Y] / 255)

  ##  meta['alpha'] is either True or False
  if meta['alpha']:   bpp  = 4     ##  RGBA
  else:               bpp  = 3     ##  RGB
                  ##  bpp  = bits per plane

  #  print(str(bpp))
  #  print(meta)

  background  = [R, G, B]  = array[0][0:3]
  print('background:  [' + str(R) + ', ' + str(G) + ', ' + str(B) + ']')

  ww  = W / 2
  hh  = H / 2

  Y  = 0
  while Y < H:
    looptime  = floor((time() - looptimer) * 100) / 100
    print(str(looptime) + '  Line: ' + str(Y + 1) + ' of: ' + str(H))
    if looptime > 2: Y = H; continue
    looptimer  = time()   ##  re-init timer for next loop
    yy  = array[Y]

    X  = 0
    while X < W:
      ##if meta['indexed']:
        ##index  = array[Y][X]

      xx  = X * bpp
      color  = [R, G, B]  = yy[xx : xx + 3]

      if color != background:
        #  print(str(X) + ', ' + str(Y) + ',  ' + str(color))

        brightness  = (R+R + G+G+G + B) / 6
##    our eyes are sensitive to shades of red and even moreso to green,
##    so extra samples of them are taken when averaging luminosity value.
##    stackoverflow.com/a/596241       using fast approximation

        Z  = brightness / 50
        zz  = Z / 10

        if brightness < 10:   ##  shadow
          bpy.ops.mesh.primitive_ico_sphere_add(size= scale + 0.3,
              location= ((X - ww) * scale,  (-Y + hh) * scale,  Z),
              rotation= (0,  0,  uniform(-1, 1)))

        elif brightness < 200:   ##  midtone
          bpy.ops.mesh.primitive_cone_add(vertices= 4,   end_fill_type= 'NOTHING',
              depth= 4 - Z,  radius1= scale + 0.2 - zz,
              location= ((X - ww) * scale,  (-Y + hh) * scale,  Z * 0.7),
              rotation= (0,  0,  0.785398))      ##  + uniform(-0.5, 0.5)))

        else:   ##  highlight
          bpy.ops.mesh.primitive_cone_add(vertices  = 4,   end_fill_type= 'NOTHING',
              depth= 5.1 - Z,   radius1= scale,
              location= ((X - ww) * scale,  (-Y + hh) * scale,  Z * 0.5),
              rotation= (0, 0, 0.785398))

##  4 vertices = pyramid,  end_fill = nothing  cuts down on polygons,  depth is how tall it is
##  location is scaleed on the grid,  radius1 is width,  radius2 chops off the top...
##  but it'll look hollow without end_fill,  rotation on the Z-axis 45° = 0.785398 radians

        obj  = bpy.context.object
        colorstring  = 'r' + str(R) + ' g' + str(G) + ' b' + str(B)

        if colorstring in bpy.data.materials.keys():
          obj.data.materials.append(bpy.data.materials[colorstring])

        else:
          material  = bpy.data.materials.new(colorstring)
          obj.data.materials.append(material)
          material.diffuse_color  = (R / 256, G / 256, B / 256)

          if gloss:
            material.raytrace_mirror.use  = True
            material.raytrace_mirror.reflect_factor  = 0.25
            material.raytrace_mirror.fresnel_factor  = 3
            material.raytrace_mirror.fade_to  = 'FADE_TO_MATERIAL'

          bpy.ops.object.material_slot_assign()

      X += 1
    Y += 1



##=============================================================
##  eof  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
