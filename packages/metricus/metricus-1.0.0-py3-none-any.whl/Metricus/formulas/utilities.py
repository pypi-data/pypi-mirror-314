import math
  
class Base:
  def round_number(number) -> float: 
    """
    Rounds the number to the nearest value or nearest half.
    
    Example: 4.9 -> 5, 4.4 -> 4.5, 2.97 -> 3
    """
    decimal_part = number % 1
    
    if decimal_part < 0.25:
      return math.floor(number)
    elif 0.25 <= decimal_part < 0.75:
      return math.floor(number) + 0.5
    else:
      return math.ceil(number) 
