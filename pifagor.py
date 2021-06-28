import math

class Pifagor:
  def __init__(self, a, b, c):  
    self.a = a
    self.b = b
    self.c = c
  
  def countup(self):
    a, b, c = self.a, self.b, self.c
    if not a:
      a = math.sqrt(int(c) ** 2 - int(b) ** 2)
    if not b:
      b = math.sqrt(int(c) ** 2 - int(a) ** 2)
    if not c:
      c = math.sqrt(int(a) ** 2 + int(b) ** 2)
  
    return (int(x) if isinstance(x, float) or f'{x}'.isnumeric() else x for x in [a, b, c])  

