# spring.py
# module for spring force on a point mass particle to a point
# Sparisoma Viridi | https://github.com/dudung

# 20230516
#   1547 Start this module.
#   1625 Finish and start testing.

from butiran.math.vect3 import Vect3
from butiran.grain import Grain

class Spring:
  def __init__(self, length=1, constant=1, pivot=Vect3()):
    self.length = length
    self.constant = constant
    assert isinstance(pivot, Vect3), 'pivot should be a Vect3'
    self.pivot = pivot
  
  def __str__(self):
    str = '{\n'
    str += f'  "length": "{self.length}"' + ',\n'
    str += f'  "constant": "{self.constant}"' + ',\n'
    str += f'  "pivot": "{self.pivot}"' + ',\n'
    str += '}'
    return str
  
  def force(self, grain):
    assert isinstance(grain, Grain)
    r = grain.r
    l = self.length
    k = self.constant
    p = self.pivot
    d = Vect3.len(r - p)
    u = (r - p) >> 1
    f = -k * (d - l) * u
    return f
