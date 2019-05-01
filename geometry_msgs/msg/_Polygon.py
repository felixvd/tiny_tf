# This Python file uses the following encoding: utf-8
"""Based on a ROS-generated file from geometry_msgs/Polygon.msg. Do not edit."""
import sys
python3 = True if sys.hexversion > 0x03000000 else False

import struct

import geometry_msgs.msg

class Polygon():
  _md5sum = "cd60a26494a087f577976f0329fa120e"
  _type = "geometry_msgs/Polygon"
  _has_header = False #flag to mark the presence of a Header object
  _full_text = """#A specification of a polygon where the first and last points are assumed to be connected
Point32[] points

================================================================================
MSG: geometry_msgs/Point32
# This contains the position of a point in free space(with 32 bits of precision).
# It is recommeded to use Point wherever possible instead of Point32.  
# 
# This recommendation is to promote interoperability.  
#
# This message is designed to take up less space when sending
# lots of points at once, as in the case of a PointCloud.  

float32 x
float32 y
float32 z"""
  __slots__ = ['points']
  _slot_types = ['geometry_msgs/Point32[]']

  def __init__(self, *args, **kwds):
    """
    Constructor. Any message fields that are implicitly/explicitly
    set to None will be assigned a default value. The recommend
    use is keyword arguments as this is more robust to future message
    changes.  You cannot mix in-order arguments and keyword arguments.

    The available fields are:
       points

    :param args: complete set of field values, in .msg order
    :param kwds: use keyword arguments corresponding to message field names
    to set specific fields.
    """
    if args or kwds:
      pass
      #message fields cannot be None, assign default values for those that are
      if self.points is None:
        self.points = []
    else:
      self.points = []

  def _get_types(self):
    """
    internal API method
    """
    return self._slot_types