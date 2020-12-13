# MicroPython utility methods.


def strtobool(value):
  """
  This method convert string to bool.
  Return False for values of the keywords "false" "f" "no" "n" "0" or 0.
  Or, return True for values of the keywords "true" "t" "yes" "y" "1" or 1.
  Or, othres return None.

  Args:
    value : string value

  Return:
    Return False for values of the keywords "false" "f" "no" "n" "off" "0" or 0.
    Or, return True for values of the keywords "true" "t" "yes" "y" "on" "1" or 1.
    Or, othres return None.

  Raises:
    TypeError : The type of parameter is not string.
    ValueError : The parameter value can not be interpreted as a bool value.
  """
  if type(value) is not str and value not in [0, 1]:
    raise TypeError("The type of parameter value must be string.")

  ret_value = None
  if value.lower() in ["false", "f", "no", "n", "off", "0"] or value == 0:
    ret_value = False
  elif value.lower() in ["true", "t", "yes", "y", "on", "1"] or value == 1:
    ret_value = True
  else:
    raise ValueError("")

  return ret_value
