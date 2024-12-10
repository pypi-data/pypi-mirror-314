# gravitational.py
# module for gravitational force on a point mass particle
# Sparisoma Viridi | https://github.com/dudung

# 20230526
#   0509 Correct .grain to .entity.grain (change folder).
# 20220919
#   1731 Start this module.
#   1743 Finish test it.

from butiran.math.vect3 import Vect3
from butiran.entity.grain import Grain

class Gravitational:
  def __init__(self, field=Vect3()):
    assert isinstance(field, Vect3), 'field should be a Vect3'
    self.field = field
  
  def __str__(self):
    str = '{\n'
    str += f'  "field": "{self.field}"' + ',\n'
    str += '}'
    return str
  
  def force(self, grain):
    assert isinstance(grain, Grain)
    m = grain.m
    g = self.field
    f = m * g
    return f