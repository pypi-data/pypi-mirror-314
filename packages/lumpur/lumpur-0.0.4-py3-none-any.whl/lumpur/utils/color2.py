# color2.py
# color2 module
# Sparisoma Viridi | https://github.com/dudung

# 20220917
#   1611 Remove sys.path.insert(0, '../../butiran') line.
# 20220916
#   1639 Rename it from Color to Color2.
# 20220914
#   2039 Learn to make this module.
#   XXXX sys.path.insert(0, '../../butiran') line.

class Color2:
  def __init__(self, stroke='#000', fill='#fff'):
    self.stroke = stroke
    self.fill = fill
  
  def __str__(self):
    str = '{ '
    str += f'"stroke": "{self.stroke}"' + ', '
    str += f'"fill": "{self.fill}"'
    str += ' }'
    return str