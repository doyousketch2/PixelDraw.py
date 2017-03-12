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

##  tell it where your PixelDraw dir is:
path  = '/home/eli/Pictures/Blend/Python/PixelDraw/'

##  image name you're currently on:
img   = 'Sonic2'

##  no need to specify file extension,
##  PyPNG uses PNG files, exclusively.
filetype  = '.png'

##  it doesn't like indexed images yet...
##  you may need to convert to RGB instead.

##  point this to wherever pip installed your PyPNG module:
pngmodule  = '/usr/local/lib/python3.4/dist-packages/'
##=============================================================
##  libs  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import sys
from time import time

sys.path.append(pngmodule)

import png

sys.path.append(path)

import pxl

begin  = time()  ##  initialize timer. Blender advised using it
##=============================================================
##  script  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Re  = png.Reader(path + img + filetype)
W, H, pixels, meta  = Re.read()

pxl.draw(W, H, pixels, meta)

##=============================================================
print('PixelDraw finished: %.4f sec' % (time() - begin))

'''
Sampling notes:        square unchecked.  seems like a joke button.
                                   adds confusion to the interface.
Branched Path Tracing
Clamp Direct   10.00         this could be turned down to say 4
Clamp Indirect 10.00       or 6, but it clamps down on fireflys
Light Sample Thresh 0.5

AA Samples:
Render:       25             <-- AntiAlias reduces noise
Preview:       0

Diffuse:       1
Glossy:       50          glossy tends to be noisy, but doesn't take much
                          time to calculate extra samples, so I set this high
rest of 'em:   1

Turn transmission up to 5 if using transparent material

Pattern:  Correlated Multi-jitter,  it's a Sudoku style render pattern



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
