# gravitational2.py
# module for gravitational force between two point mass particles
# Sparisoma Viridi | https://github.com/dudung

# 20220922
#   0834 Start this module.

from butiran.math.vect3 import Vect3
from butiran.grain import Grain

class Gravitational2:
  def __init__(self, constant=1):
    self.constant = constant
  
  def __str__(self):
    str = '{\n'
    str += f'  "constant": "{self.constant}"' + ',\n'
    str += '}'
    return str
  
  def force(self, grain1, grain2):
    assert isinstance(grain1, Grain)
    assert isinstance(grain2, Grain)
    m1 = grain1.m
    m2 = grain2.m
    r1 = grain1.r
    r2 = grain2.r
    r12 = r1 - r2
    d12 = Vect3.len(r12)
    u12 = r12 >> 1
    G = self.constant
    f = -G * (m1 * m2) / (d12 * d12) * u12
    return f
 
"""
 $ python force_gravitational2.py
{
  "constant": "5",
}
{
  "id": "0000",
  "m": 5,
  "d": 0,
  "q": 0,
  "b": 0,
  "color": { "stroke": "#000", "fill": "#fff" },
  "r": { "x": 0, "y": 0, "z": 0 },
  "v": { "x": 0, "y": 0, "z": 0 },
  "a": { "x": 0, "y": 0, "z": 0 }
}
{
  "id": "0034",
  "m": 10,
  "d": 0,
  "q": 0,
  "b": 0,
  "color": { "stroke": "#000", "fill": "#fff" },
  "r": { "x": 3, "y": 4, "z": 0 },
  "v": { "x": 0, "y": 0, "z": 0 },
  "a": { "x": 0, "y": 0, "z": 0 }
}
{ "x": 6.0, "y": 8.0, "z": -0.0 }
{ "x": -6.0, "y": -8.0, "z": -0.0 }
"""
