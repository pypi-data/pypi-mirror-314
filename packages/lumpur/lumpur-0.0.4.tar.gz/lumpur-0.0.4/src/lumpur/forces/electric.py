# electric.py
# module for electric force on a point mass particle
# Sparisoma Viridi | https://github.com/dudung

# 20230516
#   1538 Correct m to q in force function, but not tested yet.
# 20220919
#   1846 Start this module.

from butiran.math.vect3 import Vect3
from butiran.grain import Grain

class Electric:
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
    q = grain.q
    E = self.field
    f = q * E
    return f