# normal.py
# module for normal force between spherical particle and triangle
# Sparisoma Viridi | https://github.com/dudung

# 20230524
#   0515 Add force() for interaction with rectangle mesh.
# 20230524
#   1734 Start this module.
#   1836 Finish formulating normal force.
#   1907 Correct overlap.
#   1911 Pass the test but not completely.

from butiran.math.vect3 import Vect3
from butiran.entity.grain import Grain
from butiran.entity.triangle import Triangle
from butiran.entity.rectangle import Rectangle

class Normal:
  def __init__(self, constant=1, damping=0):
    self.constant = constant
    self.damping = damping
  
  def __str__(self):
    str = '{\n'
    str += f'  "constant": "{self.constant}"' + ',\n'
    str += f'  "damping": "{self.damping}"' + ',\n'
    str += '}'
    return str
  
  def force(self, grain, triangle):
    assert isinstance(grain, Grain)
    assert isinstance(triangle, Triangle)
    
    # calculate normal vector of triangle mesh
    p0 = triangle.p0
    p1 = triangle.p1
    p2 = triangle.p2
    q1 = p1 - p0
    q2 = p2 - p0
    n = (q1 * q2) >> 1
    pc = (p0 + p1 + p2) / 3
    
    r = grain.r
    l = 0.5 * grain.d
    k = self.constant
    d = (r - pc) | n
    fr = k * max(0, l - d) * n
    
    v = grain.v
    g = self.damping
    fv = -g * (v - Vect3())
    
    f = fr + fv
    return f
  
  def force(self, grain, rectangle):
    assert isinstance(grain, Grain)
    assert isinstance(rectangle, Rectangle)
    
    # calculate normal vector of rectangle mesh
    p0 = rectangle.p0
    p1 = rectangle.p1
    p2 = rectangle.p2
    p3 = rectangle.p3
    q1 = p1 - p0
    q2 = p2 - p0
    n = (q1 * q2) >> 1
    pc = (p0 + p1 + p2 + p3) / 4
    
    r = grain.r
    l = 0.5 * grain.d
    k = self.constant
    d = (r - pc) | n
    fr = k * max(0, l - d) * n
    
    v = grain.v
    g = self.damping
    fv = -g * (v - Vect3())
    
    f = fr + fv
    return f
