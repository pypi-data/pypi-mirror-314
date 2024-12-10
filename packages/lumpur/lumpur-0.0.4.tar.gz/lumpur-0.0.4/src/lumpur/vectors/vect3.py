# vect3.py
# vect3 module
# Sparisoma Viridi | https://github.com/dudung

# 20220914
#   1839 Change __str__ output to JSON format.
# 20220519
#   1909 define __init__, _str__ and test ok.
#   1915 define __add__, __sub__ and test ok.
#   1928 define __mul__, __rmul__ and test ok.
#   1938 define __or__ and test ok.
#   1945 define __truediv__ and test ok.
# 20220520
#   0313 define len and test ok.
#   0314 add space between __str__ items after comma.
#   0324 define __rshift__ and test ok.
#   0334 define copy and test ok.
#   0524 define __neg__ and test ok.

import math

class Vect3:
  def __init__(self, x=0, y=0, z=0):
    self.x = x
    self.y = y
    self.z = z
  
  def __str__(self):
    str = '{ '
    str += f'"x": {self.x}' + ', '
    str += f'"y": {self.y}' + ', '
    str += f'"z": {self.z}'
    str += ' }'
    return str
  
  def __add__(self, other):
    r = Vect3()
    r.x = self.x + other.x
    r.y = self.y + other.y
    r.z = self.z + other.z
    return r
  
  def __sub__(self, other):
    r = Vect3()
    r.x = self.x - other.x
    r.y = self.y - other.y
    r.z = self.z - other.z
    return r
  
  def __mul__(self, other):
    r = Vect3()
    if isinstance(other, int) | isinstance(other, float):
      r.x = self.x * other
      r.y = self.y * other
      r.z = self.z * other
    elif isinstance(other, Vect3):
      r.x = self.y * other.z - self.z * other.y
      r.y = self.z * other.x - self.x * other.z
      r.z = self.x * other.y - self.y * other.x
    return r
  
  def __rmul__(self, other):
    r = Vect3()
    if isinstance(other, int) | isinstance(other, float):
      r = self.__mul__(other)
    return r
  
  def __or__(self, other):
    l = 0
    if isinstance(other, Vect3):
      lx = self.x * other.x
      ly = self.y * other.y
      lz = self.z * other.z
      l = lx + ly + lz
    return l
  
  def __truediv__ (self, other):
    r = Vect3()
    if isinstance(other, float) | isinstance(other, int):
      r.x = self.x / other
      r.y = self.y / other
      r.z = self.z / other
    return r
  
  def len(self):
    l = math.sqrt(self | self);
    return l
  
  def __rshift__(self, other):
    u = Vect3()
    r = self
    l = r.len()
    if l != 0:
      u = r / l
    s = u * other 
    return s

  def copy(self):
    r = Vect3()
    r.x = self.x
    r.y = self.y
    r.z = self.z
    return r
  
  def __neg__(self):
    r = Vect3()
    r.x = -self.x
    r.y = -self.y
    r.z = -self.z
    return r