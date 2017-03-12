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
import bpy
import bmesh
from random import uniform

def draw(W, H, pixels, meta):
  array  = list(pixels)

  if W > H:
    MajorAxis  = W
  else:
    MajorAxis  = H

  center  = 16 / MajorAxis

  ##  the default grid is +8 & -8, along X and Y.
  ##  so it finds the largest of those two  (W or H)
  ##  and centers pixels within that 16 blender-unit square

  #  print(str(W) + ', ' + str(H))
  #  print(array[X][Y] / 255)

  ##  meta['alpha'] is either True or False
  if meta['alpha']:
    bpp  = 4  ##  RGBA
  else:      ##  bpp  = bits per plane
    bpp  = 3  ##  RGB
  #  print(str(bpp))
  #  print(meta)

  R, G, B  = array[0][0:3]
  background  = [R, G, B]
  #  print('background:  ' + str(background))

  Y  = 0
  while Y < H:
    X  = 0
    while X < W:
      ##if meta['indexed']:
        ##index  = array[Y][X]

      xx  = X * bpp
      yy  = array[Y]
      R, G, B  = yy[xx : xx + 3]
      color  = [R, G, B]

      if color != background:
        #  print(str(X) + ', ' + str(Y) + ',  ' + str(color))

        brightness  = (R+R+R + G+G+G+G + B) / 8
##    our eyes are sensitive to shades of red and even moreso to green,
##    so more samples of them are taken when averaging luminosity value.
##    stackoverflow.com/a/596241

        Z = brightness / 50

        if brightness < 10:
          bpy.ops.mesh.primitive_ico_sphere_add(size  = center + 0.285 - Z / 10,
              location  = ((X - W / 2) * center,  (-Y + H / 2) * center,  Z),
              rotation  = (0,  0,  uniform(-1, 1)))

        elif brightness < 200:
          bpy.ops.mesh.primitive_cone_add(vertices  = 5,   end_fill_type  = 'NOTHING',
              depth  = 4.5 - Z,   location  = ((X - W / 2) * center,  (-Y + H / 2) * center,  Z),
              radius1  = center + 0.285 - Z / 10,
              rotation  = (0,  0,  0.785398 + uniform(-0.5, 0.5)))

        else:
          bpy.ops.mesh.primitive_cone_add(vertices  = 4,   end_fill_type  = 'NOTHING',
              depth  = 4.5 - Z,   location  = ((X - W / 2) * center,  (-Y + H / 2) * center,  Z),
              radius1  = center + 0.285 - Z / 10,   rotation  = (0, 0, 0.785398))

##  4 vertices = pyramid,  end_fill = nothing  cuts down on polygons,  depth is how tall it is
##  location is centered on the grid,  radius1 is width,  radius2 chops off the top...
##  but it'll look hollow without end_fill,  rotation on the Z-axis 45° = 0.785398 radians

        obj  = bpy.context.scene.objects.active
        name  = obj.name

        material  = bpy.data.materials.new(name)
        obj.data.materials.append(material)

        material.diffuse_color  = (R / 256, G / 256, B / 256)
        material.raytrace_mirror.use  = True
        material.raytrace_mirror.reflect_factor  = 0.25
        material.raytrace_mirror.fresnel_factor  = 3
        material.raytrace_mirror.fade_to  = 'FADE_TO_MATERIAL'

        bpy.ops.object.material_slot_assign()

      X += 1
    Y += 1



##=============================================================
##  eof  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
