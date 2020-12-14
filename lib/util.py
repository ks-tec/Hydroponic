# MicroPython utility methods.
#
# Copyright (c) 2020 ks-tec
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the "Software"),
# to dealin the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sellcopies of the Software, and to permit persons to whom the Software
# is furnished to do so, subject to the following conditions:
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE NOT LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS INTHE SOFTWARE.


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
