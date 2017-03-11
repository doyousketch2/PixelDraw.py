##=========================================================
##                                              10 Mar 2017
##  PixelDraw.py
##
##  turn pixels into polygons, from spritesheets to Blender
##
##  Eli Leigh Innis
##  Twitter :  @ Doyousketch2
##  Email :  Doyousketch2 @ yahoo.com
##
##  GNU GPLv3                 gnu.org/licenses/gpl-3.0.html
##=========================================================
##  required  ---------------------------------------------
##
##  first, get Blender from their website.
##
##  then you'll need PyPNG:
##  -----------------------
##    you can use pip for Python3:
##    pip should come with any recent version of Python.
##    (linux - use synaptic package manager, or...)
##        sudo apt-get install python3-pip
##    (mac)
##        sudo easy_install pip
##
##  next, use pip to install PyPNG:
##    (debian)
##        sudo pip3 install pypng
##    (linux, mac)
##        sudo python3 -m pip install pypng
##    (or win)
##        py -m pip install pypng
##  --------------------------------
##  or skip the whole pip method and download PyPNG from GitHub
##    github.com/drj11/pypng
##    then unzip it in your Blender modules dir
##=============================================================
#  libs

import sys
import bpy
import bmesh
from time import time

##  point this to wherever pip installed your PyPNG module:
sys.path.append('/usr/local/lib/python3.4/dist-packages/')
import png

begin  = time()  ##  initialize timer. Blender advised using it
##=============================================================
#  vars


path  = '/home/eli/Pictures/Blend/py/PixelDraw/'
img  = 'sprite.png'
##  it doesn't like indexed images yet...
##  you may need to convert to RGB instead.


##  flat for these colors
outline  = [[0, 0, 0], [255, 255, 255]]

##  shallow depth for these colors
flesh  = [[248, 112, 104], [248, 208, 192], [252, 181, 168]]


##=============================================================
#  script

r  = png.Reader(path + img)
W, H, pixels, meta  = r.read()
array  = list(pixels)

##  print(str(W) + ', ' + str(H))
##  print(array[x][y] / 255)

##  meta['alpha'] is either True or False
if meta['alpha']:
  bpp  = 4  ##  RGBA
else:      ##  bpp  = bits per plane
  bpp  = 3  ##  RGB
print(str(bpp))
print(meta)

r, g, b  = array[0][0:3]
background  = [r, g, b]
print('background:  ' + str(background))

y  = 0
while y < H:
  x  = 0
  while x < W:
    ##if meta['indexed']:
      ##index  = array[y][x]

    xx = x * bpp
    yy = array[y]
    r, g, b  = yy[xx : xx + 3]
    color  = [r, g, b]

    if color != background:
      ##  print(str(x) + ', ' + str(y) + ',  ' + str(color))

##  4 vertices = pyramid, end_fill = nothing is to cut down on polygons, depth is how tall it is
##  location is centered on the grid, radius1 is width, radius2 chops off the top...
##  but it'll look hollow without end_fill, rotation on the Z-axis 45° = 0.785398 radians

      if color in outline:
        bpy.ops.mesh.primitive_cone_add(vertices=4, end_fill_type='NOTHING', depth=0.1,
            location=(x - W / 2, -y + H / 2, 0), radius1=1, rotation=(0, 0, 0.785398))

      elif color in flesh:
        bpy.ops.mesh.primitive_cone_add(vertices=4, end_fill_type='NOTHING', depth=0.2,
            location=(x - W / 2, -y + H / 2, 0), radius1=1, rotation=(0, 0, 0.785398))

      else:
        bpy.ops.mesh.primitive_cone_add(vertices=4, end_fill_type='NOTHING', depth=2,
            location=(x - W / 2, -y + H / 2, 0), radius1=1, rotation=(0, 0, 0.785398))

      obj = bpy.context.scene.objects.active
      name = obj.name

      material = bpy.data.materials.new(name)
      obj.data.materials.append(material)
      material.diffuse_color = (r / 255, g / 255, b / 255)
      material.raytrace_mirror.use = True
      material.raytrace_mirror.reflect_factor = 0.25
      material.raytrace_mirror.fresnel_factor = 3
      material.raytrace_mirror.fade_to = 'FADE_TO_MATERIAL'
      bpy.ops.object.material_slot_assign()

    x += 1
  y += 1

##=============================================================
print('PixelDraw finished: %.4f sec' % (time() - begin))

'''
Sampling notes

Branched Path Tracing
Clamp Direct   10.00   this could be turned down to say 4
Clamp Indirect 10.00   or 6, but it clamps down on fireflys
Light Sample Thresh 0.5

AA Samples:
Render:       25
Preview:       0

Diffuse:       1
Glossy:       50
rest of 'em:   1

Turn transmission up to 5 if using transparent material

Pattern:  Correlated Multi-jitter, it's like Sudoku render pattern
'''
##=============================================================
#  eof
