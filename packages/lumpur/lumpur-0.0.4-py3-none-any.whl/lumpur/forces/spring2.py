# spring2.py
# module for spring force between two point mass particles
# Sparisoma Viridi | https://github.com/dudung

# 20230522
#   1907 Start this module.
#   1919 Pass instantiation test.

from butiran.math.vect3 import Vect3
from butiran.grain import Grain

class Spring2:
  def __init__(self, length=1, constant=1, damping=0):
    self.length = length
    self.constant = constant
    self.damping = damping
  
  def __str__(self):
    str = '{\n'
    str += f'  "length": "{self.length}"' + ',\n'
    str += f'  "constant": "{self.constant}"' + ',\n'
    str += f'  "damping": "{self.damping}"' + ',\n'
    str += '}'
    return str
  
  def force(self, grain1, grain2):
    assert isinstance(grain1, Grain)
    assert isinstance(grain2, Grain)
    r1 = grain1.r
    r2 = grain2.r
    l = self.length
    k = self.constant
    d = Vect3.len(r1 - r2)
    u = (r1 - r2) >> 1
    fr = -k * (d - l) * u
    
    v1 = grain1.v
    v2 = grain2.v
    g = self.damping
    fv = -g * (v1 - v2)
    
    f = fr + fv
    return f
