class Coord:
  def __init__(self, x, y):
    self.x = x
    self.y = y
  def __eq__(self, other):
    if isinstance(other, Coord):
      return self.x == other.x and self.y == other.y
    return False
  def __ne__(self, other):
    return not self.__eq__(other)
  def __hash__(self):
    return hash((self.x, self.y))
  def __str__(self):
    return f"[{self.x}, {self.y}]"
