# magnetic.py
# module for magnetic force on a moving charged point particle
# Sparisoma Viridi | https://github.com/dudung

# 20220917
#   1548 Start this module.
#   1614 Remove sys.path.insert(0, '../../butiran') line.
#   1628 Use isinstance() to assure field is Vect3.
#   1830 Try to use assert.
#   1903 Implement assert to force field argument as Vect3.
#   1929 Create force() for magnetic force worked on the grain.

from butiran.math.vect3 import Vect3
from butiran.grain import Grain

class Magnetic:
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
    v = grain.v
    q = grain.q
    B = self.field
    f = q * v * B
    return f