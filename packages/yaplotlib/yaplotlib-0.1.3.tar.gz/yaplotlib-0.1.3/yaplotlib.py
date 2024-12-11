# -*- coding: utf-8 -*-
# even: stable; odd: develop
__version__ = "0.1.3"

import colorsys


def plaintext(a):
    s = ""
    for x in a:
        s += "{0:.4f} ".format(x)
    return s


def Line(v0,v1):
    return "l " + plaintext(v0) + plaintext(v1) + "\n"


def Text(v,txt):
    return "t " + plaintext(v) + " " + txt + "\n"


def Circle(v0):
    return "c " + plaintext(v0) + "\n"


def Arrow(v0,v1):
    return "s " + plaintext(v0) + plaintext(v1) + "\n"



def Polygon(vertices):
    s = f"p {len(vertices)} "
    for v in vertices:
        s += plaintext(v)
    return s + "\n"



def Color(x):
    return f"@ {int(x)}\n"

# R,G,B in range 0..255
def SetPalette(x,R,G=None,B=None,maxval=255):
    if G is None:
        R,G,B = R
    r = int(R*255/maxval)
    g = int(G*255/maxval)
    b = int(B*255/maxval)
    return f"@ {int(x)} {r} {g} {b}\n"


def Size(x):
    return f"r {float(x)}\n"


def Layer(x):
    return f"y {int(x)}\n"


def ArrowType(x):
    return f"a {int(x)}\n"


def NewPage():
    return "\n"


def RandomPalettes(N, offset=10):
    omega = 2 / (5**0.5 - 1)
    s = ""
    for i in range(N):
        hue = (omega * i) % 1.0
        sat = 0.5
        bri = 1.0
        r,g,b = colorsys.hsv_to_rgb(hue, sat, bri)
        s += SetPalette(i+offset, r,g,b, maxval=1.0)
    return s


def RainbowPalettes(N, offset=10):
    s = ""
    for i in range(N):
        hue = i / N
        sat = 0.5
        bri = 1.0
        r,g,b = colorsys.hsv_to_rgb(hue, sat, bri)
        s += SetPalette(i+offset, r,g,b, maxval=1.0)
    return s


def GradationPalettes(N, color, color1=None, offset=10, maxval=255):
    """
    いずれ、dictやlistでも与えられるようにする。
    """
    s = ""
    for i in range(N):
        ratio = i / (N-1)
        r = color[0]*(1-ratio) + color1[0]*ratio
        g = color[1]*(1-ratio) + color1[1]*ratio
        b = color[2]*(1-ratio) + color1[2]*ratio
        s += SetPalette(i+offset, r, g, b, maxval)
    return s


class Yaplot():
    def __init__(self):
        self.s = ""
        self.layer = 1
        self.color = 2
        self.size = 1
        self.arrowtype = 1
    def Layer(self, layer):
        if layer < 0:
            return
        if layer != self.layer:
            self.s += Layer(layer)
            self.layer = layer
    def Color(self, color):
        if color < 0:
            return
        if color != self.color:
            self.s += Color(color)
            self.color = color
    def Size(self, size):
        if size < 0:
            return
        if size != self.size:
            self.s += Size(size)
            self.size = size
    def ArrowType(self, arrowtype):
        if arrowtype < 0:
            return
        if arrowtype != self.arrowtype:
            self.s += ArrowType(arrowtype)
            self.arrowtype = arrowtype
    def Line(self, a, b, layer=-1, color=-1):
        if layer > 0:
            self.s += self.Layer(layer)
        if color >= 0:
            self.s += self.Color(color)
        self.s += Line(a, b)
    def Arrow(self, a, b, layer=-1, color=-1, size=-1, arrowtype=-1):
        self.s += self.Layer(layer)
        self.s += self.Color(color)
        self.s += Line(a, b)
    def Polygon(self, p, layer=-1, color=-1):
        self.s += self.Layer(layer)
        self.s += self.Color(color)
        self.s += Polygon(p)
    def Circle(self, c, layer=-1, color=-1, size=-1):
        self.s += self.Layer(layer)
        self.s += self.Color(color)
        self.s += self.Size(size)
        self.s += Circle(c)
    def SetPalette(self, x, R, G=None, B=None, maxval=255):
        self.s += SetPalette(x, R, G, B, maxval)
    def GradationPalettes(self, N, color, color1=None, offset=10, maxval=255):
        self.s += GradationPalettes(N, color, color1, offset, maxval)
    def RandomPalettes(self, N, offset=10):
        self.s += RandomPalettes(N, offset)
    def RainbowPalettes(self, N, offset=10):
        self.s += RainbowPalettes(N, offset)
    def NewPage(self):
        self.s += NewPage()
        self.layer = 1
        self.color = 2
        self.arrowtype = 1
        self.size = 1
    def dumps(self):
        return self.s
