import math
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing

class Triangle:
  '''
  A class used to create and show a Triangle
  
  ...
    
  Attributes
  ----------
  name : str
    name of the file
  a : int
    cathetus value for side a
  b : int
    cathetus value for side b
  grid_color : str
    default color for grid
  triangle_color : str
    default color for triangle_color
  
  Methods
  -------
  set()
    Setting up the graph and adds triangle lines
  show()
    Open new window with drawn graph
  get()
    Create img of graph
  '''

  grid_color = 'gray'
  triangle_color = 'purple'
  
  def __init__(self, name, a=5, b=5):
    self.name = name
    self.a = int(a)
    self.b = int(b)
  def set(self):
    fig, ax = plt.subplots()
    ax.plot([0, self.a, self.a, 0], [0, 0, self.b, 0], color=self.triangle_color, marker='.', label='Meet this is triangle')
    ax.set_title('Triangle')
    ax.set_xlabel('this is x')
    ax.set_ylabel('this is y')
    ax.legend()
    plt.grid(color=self.grid_color)   
    return self
  def show(self):
    plt.show()
    return self
  def get(self):
    plt.savefig(self.name, dpi=300, bbox_inches='tight')
    return self.name
    

class Figure:
  '''
  A class used to determine figure and put it to Queue
  
  ...
  
  Attributes
  ----------
  figurename : str
    name of the graph file
  
  Methods
  -------
  add_value()
    Create figure, save it to img and put file name to Queue
  '''
  
  def __init__(self, figurename):
    self.fname = figurename
  
  def add_value(self, q, coors, graph_name):
    if self.fname == 'triangle':
      t = Triangle(graph_name, *coors)
      img = t.set().get()
      q.put(img)

