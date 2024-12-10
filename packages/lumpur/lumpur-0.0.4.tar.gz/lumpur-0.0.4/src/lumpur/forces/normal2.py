# normal2.py
# module for normal force between two spherical particles
# Sparisoma Viridi | https://github.com/dudung

# 20230525
#   2049 Correct .grain to .entity.grain (entity folder).
# 20230523
#   0449 Start this module.
#   0504 Pass instantiation test.

from butiran.math.vect3 import Vect3
from butiran.entity.grain import Grain

class Normal2:
  def __init__(self, constant=1, damping=0):
    self.constant = constant
    self.damping = damping
  
  def __str__(self):
    str = '{\n'
    str += f'  "constant": "{self.constant}"' + ',\n'
    str += f'  "damping": "{self.damping}"' + ',\n'
    str += '}'
    return str
  
  def force(self, grain1, grain2):
    assert isinstance(grain1, Grain)
    assert isinstance(grain2, Grain)
    r1 = grain1.r
    r2 = grain2.r
    l = 0.5 * (grain1.d + grain2.d)
    k = self.constant
    d = Vect3.len(r1 - r2)
    u = (r1 - r2) >> 1
    fr = -k * min(0, d - l) * u
    
    v1 = grain1.v
    v2 = grain2.v
    g = self.damping
    fv = -g * (v1 - v2)
    
    f = fr + fv
    return f
