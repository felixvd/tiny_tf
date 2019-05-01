# This Python file uses the following encoding: utf-8
"""Based on a ROS-generated file from geometry_msgs/Point.msg. Do not edit."""
import sys
python3 = True if sys.hexversion > 0x03000000 else False

import struct


class Point():
  _md5sum = "4a842b65f413084dc2b10fb484ea7f17"
  _type = "geometry_msgs/Point"
  _has_header = False #flag to mark the presence of a Header object
  _full_text = """# This contains the position of a point in free space
float64 x
float64 y
float64 z
"""
  __slots__ = ['x','y','z']
  _slot_types = ['float64','float64','float64']

  def __init__(self, *args, **kwds):
    """
    Constructor. Any message fields that are implicitly/explicitly
    set to None will be assigned a default value. The recommend
    use is keyword arguments as this is more robust to future message
    changes.  You cannot mix in-order arguments and keyword arguments.

    The available fields are:
       x,y,z

    :param args: complete set of field values, in .msg order
    :param kwds: use keyword arguments corresponding to message field names
    to set specific fields.
    """
    if args or kwds:
      super(Point, self).__init__(*args, **kwds)
      #message fields cannot be None, assign default values for those that are
      if self.x is None:
        self.x = 0.
      if self.y is None:
        self.y = 0.
      if self.z is None:
        self.z = 0.
    else:
      self.x = 0.
      self.y = 0.
      self.z = 0.

  def _get_types(self):
    """
    internal API method
    """
    return self._slot_types