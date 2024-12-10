# drag.py
# module for drag force on a point particle
# Sparisoma Viridi | https://github.com/dudung

# 20230516
#   1928 Start this module, raw copy from magnetic force.
#   1937 Pause zum Abendessen.

from butiran.math.vect3 import Vect3
from butiran.grain import Grain

class Drag:
  def __init__(self, coeff=1, field=Vect3()):
    self.coeff = coeff
    assert isinstance(field, Vect3), 'field should be a Vect3'
    self.field = field
  
  def __str__(self):
    str = '{\n'
    str += f'  "field": "{self.field}"' + ',\n'
    str += '}'
    return str
  
  def force(self, grain):
    assert isinstance(grain, Grain)
    v = grain.v
    u = self.field
    b = self.coeff
    f = - b * (v - u)
    return f