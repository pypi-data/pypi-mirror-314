import math

def round_number(result) -> float:
  """
  Rounds a given number to the nearest integer or the nearest half integer.

  This function can handle both numbers and strings containing a number. 
  If a string is provided, it will extract the first numeric value and round it. 
  The rest of the string, if present, will be returned along with the rounded number.

  Parameters:
  result (float or str): The number to be rounded. If a string is provided, 
                          it must contain a valid numeric value as the first word.

  Returns:
  float or str: 
      - If a number is provided, the function returns the rounded number (nearest integer or nearest 0.5).
      - If a string is provided, the function returns the rounded number followed by the rest of the string.

  Examples:
  1. 4.9 -> 5
  2. 4.4 -> 4.5
  3. 2.97 -> 3
  4. "3.8 apples" -> "4 apples"
  5. "2.4 oranges" -> "2.5 oranges"

  Raises:
  ValueError: If the provided string does not contain a valid number.
  """
  if isinstance(result, str):
    try:
      parts = result.split()
      number = float(parts[0])
      string = " ".join(parts[1:])

      decimal_part = number % 1

      if decimal_part < 0.25:
        result_num = math.floor(number)
      elif 0.25 <= decimal_part < 0.75:
        result_num = math.floor(number) + 0.5
      else:
        result_num = math.ceil(number)

      return f"{result_num} {string}"
    except ValueError:
      raise ValueError("The provided string does not contain a valid number")

  number = result
  decimal_part = number % 1

  if decimal_part < 0.25:
    return math.floor(number)
  elif 0.25 <= decimal_part < 0.75:
    return math.floor(number) + 0.5
  else:
    return math.ceil(number)
