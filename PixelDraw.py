#!/usr/bin/python3
##=========================================================
##  PixelDraw.py                                10 Mar 2017
##
##  turn pixels into polygons, from spritesheets to Blender
##
##  Eli Leigh Innis
##  Twitter :  @ Doyousketch2
##  Email :  Doyousketch2 @ yahoo.com
##
##  GNU GPLv3                 gnu.org/licenses/gpl-3.0.html
##=========================================================
##  required  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##
##  first, get Blender from their website.
##
##  then you'll need PyPNG:
##  -----------------------
##    you can use pip for Python3:
##        pip should come with any recent version of Python.
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
##=============================================================
##  vars  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

##  image name you're currently on:
img   = 'Tanooki'

##  no need to specify file extension,
##  PyPNG uses PNG files, exclusively.
filetype  = '.png'

##  it doesn't like indexed images yet...
##  you may need to convert to RGB instead.

##  glossy Raytrace?  True / False
gloss  = False

##  if set to 2, pixels will be planes (still elevated along Z axis)
##  if set to 3, pixels will be pyramids
dimensions  = 2

##  printed between verts and faces
divider = '##======================================'

##=============================================================
##  libs  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os
import sys
from time import time
from math import floor
import png
import pxl

begin  = time()        ##  initialize timer. Blender advises it
##=============================================================
##  script  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

getsize  = os .path .getsize
cwd  = os .getcwd()

if cwd[0] is '/':   ##  linux
  inpu  = '/Input/'
  outpu  = '/Output/'
else:                 ##  win
  inpu  = '\\Input\\'
  outpu  = '\\Output\\'

print('Loading:  %s%s%s.png' % (cwd, inpu, img))
Re  = png .Reader(cwd + inpu + img + filetype)
W, H, pixels, meta  = Re .read()


##  draw(W, H, pixels, meta, gloss=True)

vertices, faces, colors  = pxl .draw(W, H, pixels, meta, gloss, dimensions)

##-------------------------------------
##  material

with open(cwd + outpu + img + '.mtl', 'w') as mtl:

  print('\nWriting header to %s.mtl' % img)
  mtl .write('%s\n' % divider)
  mtl .write('##  Materials exported from PixelDraw\n')
  mtl .write('##  github.com/doyousketch2/PixelDraw.py\n')
  mtl .write('%s\n' % divider)
  mtl .write('##  Colors used by %s.obj\n\n' % img)

  print('Writing colors to %s.mtl' % img)
  for c in colors:
    mtl .write(('%s\n') % c)

##  filesize
size  = getsize(cwd + outpu + img + '.mtl')
KiB  = size / 1024
floored  = floor(KiB * 100) / 100
print('      %s KiB written\n' % floored)

##-------------------------------------
##  object data

with open(cwd + outpu + img + '.obj', 'w') as obj:

  print('Writing header to %s.obj' % img)
  obj .write('%s\n' % divider)
  obj .write('##  Model exported from PixelDraw\n')
  obj .write('##  github.com/doyousketch2/PixelDraw.py\n')
  obj .write('%s\n\n' % divider)
  obj .write(('mtllib %s.mtl\n\n') % img)
  obj .write('%s\n##  Vertices:\n\n' % divider)

  print('Writing vertices to %s.obj' % img)
  for v in vertices:
    obj .write(('%s\n') % v)

  print('Writing faces to %s.obj' % img)
  obj .write(('\n%s\n##  Faces:\n\n') % divider)
  for f in faces:
    obj .write(('%s\n') % f)

##  filesize
size  = getsize(cwd + outpu + img + '.obj')
KiB  = size / 1024
floored  = floor(KiB * 100) / 100
print('      %s KiB written\n' % floored)

##-------------------------------------

print('Blender > File > Import > Wavefront (.obj)')
print('%s%s%s.obj\n' % (cwd, outpu, img))
print('PixelDraw finished: %.4f sec\n' % (time() - begin))
##=============================================================
'''
Sampling notes:     square unchecked.  seems like a joke button
                               adds confusion to the interface.
Branched Path Tracing
Clamp Direct   10.00         this could be turned down to say 4
Clamp Indirect 10.00       or 6, but it clamps down on fireflys
Light Sample Thresh 0.5

AA Samples:
Render:       25             <-- AntiAlias reduces noise
Preview:       0

Diffuse:       1
Glossy:       50      glossy tends to be noisy, doesn't take much
                  time to calculate extra samples, so set it high
rest of 'em:   1

Turn transmission up to 5 if using transparent material

Pattern:  Correlated Multi-jitter
it's a Sudoku style render pattern


===========================================================

Camera notes:

Location:
X:         0.0
Y:         0.5
Z:         depends on focal length


 Z    Focal len         Notes
===   =========   =====================
120     200       extended for accuracy
 50      30
 20      14       decreased for spikes


Clipping:
Start:    0.1
End:      greater than your Z location value
'''
##=============================================================
##  eof  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
