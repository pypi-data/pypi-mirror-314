# vect2.py
# vect2 module
# Sparisoma Viridi | https://github.com/dudung

# 20220914
#   1838 Change __str__ output to JSON format.
# 20220520
#   0503 copy from vect3.
#   0512 erase some methods.
#   0520 test all methods from vect3 and ok.
#   0528 define __neg__ and test ok.

import math

class Vect2:
  def __init__(self, x=0, y=0):
    self.x = x
    self.y = y
  
  def __str__(self):
    str = '{ '
    str += f'"x": {self.x}' + ', '
    str += f'"y": {self.y}'
    str += ' }'
    return str
  
  def __add__(self, other):
    r = Vect2()
    r.x = self.x + other.x
    r.y = self.y + other.y
    return r
  
  def __sub__(self, other):
    r = Vect2()
    r.x = self.x - other.x
    r.y = self.y - other.y
    return r
  
  def __mul__(self, other):
    r = Vect2()
    if isinstance(other, int) | isinstance(other, float):
      r.x = self.x * other
      r.y = self.y * other
    return r
  
  def __rmul__(self, other):
    r = Vect2()
    if isinstance(other, int) | isinstance(other, float):
      r = self.__mul__(other)
    return r
  
  def __or__(self, other):
    l = 0
    if isinstance(other, Vect2):
      lx = self.x * other.x
      ly = self.y * other.y
      l = lx + ly
    return l
  
  def __truediv__ (self, other):
    r = Vect2()
    if isinstance(other, float) | isinstance(other, int):
      r.x = self.x / other
      r.y = self.y / other
    return r
  
  def len(self):
    l = math.sqrt(self | self);
    return l
  
  def __rshift__(self, other):
    u = Vect2()
    r = self
    l = r.len()
    if l != 0:
      u = r / l
    s = u * other 
    return s

  def copy(self):
    r = Vect2()
    r.x = self.x
    r.y = self.y
    return r
  
  def __neg__(self):
    r = Vect2()
    r.x = -self.x
    r.y = -self.y
    return r