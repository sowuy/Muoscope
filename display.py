

import os
import sys
import struct

from functools import partial

import matplotlib
matplotlib.use('Qt5Agg')

import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d as m3d

from PyQt5.QtWidgets import QLabel, QSpinBox

import numpy as np



def randrange(n, min, max):
    return (max - min) * np.random.rand(n) + min

def display(f, ax, entry):
#entry = ? 1-2-3-4 detecteurs ?
#ax = ?
    n = 1000 
#geometry
    w = 10 #Largeur de la strip 10mm =1cm
    h = 150 # 150mm =15cm z (espace entre 
    l = 160 # x ou y 
#Positions des muons 
#Detecteur 1 & 3
    x1 = []
    y1 = []
    z1 = []
#Detecteur 0 & 2
    x2 = []
    y2 = []
    z2 = []

    f.seek((entry - 1) * 16) #Place la tête de lecture (position courante dans le fichier)
    event = f.read(16) #Lis les 16 octets après la tête de lecture
    data, time = struct.unpack('QQ', event)
    for i in range(64): # 4 detecteurs avec chacun 16 strips  - calcul des positions des strips pour les dessiner - génère points aléatoires dans rectangle
        if not data >> i & 1: continue
        layer = i // 16 #0->3 pour les detecteurs 
        strip = i % 16 #0->15 strips x4
        layer = 3-layer #changer l'ordre des détecteurs.
        if layer % 2: #Detecteur 0 et 2 
            x2 = np.append(x2, randrange(n, 0, l)) #donne un vecteur de 100 nombres entre 0 et l
            y2 = np.append(y2, randrange(n, strip * w, strip * w + w)) #(n, left, right)
            z2 = np.append(z2, randrange(n, layer * h, layer * h + w)) #changer z2 et z1 pour modifier écart entre détecteurs
        else: #Detecteur 1 & 3
            x1 = np.append(x1, randrange(n, strip * w, strip * w + w))
            y1 = np.append(y1, randrange(n, 0, l))
            z1 = np.append(z1, randrange(n, layer * h, layer * h + w))

    a1 = np.vstack((x1, np.ones(len(x1)))).T #vecteur de type array([[ 1.,  1.],
      								    #[ 2.,  1.],
      								    #[ 3.,  1.]])

    m1, c1 = np.linalg.lstsq(a1, z1)[0] #Solve linear least-squares problem

    a2 = np.vstack((y2, np.ones(len(y2)))).T  #prend l'info des strips qui vont dans le même sens pour obtenir x-z dans un cas et y-z dans l'autre

    m2, c2 = np.linalg.lstsq(a2, z2)[0]

#display
    ax.cla() #?? axis plot
    ax.scatter3D(x1, y1, z1, c='b', marker='o') #points en bleu
    ax.scatter3D(x2, y2, z2, c='r', marker='o') #points en rouge 
    zz = np.linspace(0, 3 * h + w) #samples : ndarray There are `num` equally spaced samples in the closed interval ``[start, stop]``
    xx = (zz - c1) / m1  #eq ligne droites
    yy = (zz - c2) / m2  #same
    ax.plot3D(xx, yy, zz) #plot fit
    ax.set_xlim(0, l)
    ax.set_ylim(0, l)
    ax.set_zlim(0, 500)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.figure.canvas.draw()

if len(sys.argv) < 2:
    print('Usage: display.py input_file')
    sys.exit(1)

try:
    f = open(sys.argv[1], 'rb')
except (OSError, IOError) as e:
    print('Cannot open input file')
    sys.exit(1)

f.seek(0, os.SEEK_END)
size = f.tell()

fig = plt.figure()
ax = m3d.Axes3D(fig)

toolbar = fig.canvas.toolbar
toolbar.addSeparator()
label = QLabel('Event')
event = QSpinBox()
event.valueChanged.connect(partial(display, f, ax))
event.setRange(1, size // 16)
toolbar.addWidget(label)
toolbar.addWidget(event)


plt.show()
