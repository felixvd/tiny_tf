# This Python file uses the following encoding: utf-8
"""Based on a ROS-generated file from geometry_msgs/Accel.msg. Do not edit."""
import sys
python3 = True if sys.hexversion > 0x03000000 else False

import struct

import geometry_msgs.msg

class Accel():
  _md5sum = "9f195f881246fdfa2798d1d3eebca84a"
  _type = "geometry_msgs/Accel"
  _has_header = False #flag to mark the presence of a Header object
  _full_text = """# This expresses acceleration in free space broken into its linear and angular parts.
Vector3  linear
Vector3  angular

================================================================================
MSG: geometry_msgs/Vector3
# This represents a vector in free space. 
# It is only meant to represent a direction. Therefore, it does not
# make sense to apply a translation to it (e.g., when applying a 
# generic rigid transformation to a Vector3, tf2 will only apply the
# rotation). If you want your data to be translatable too, use the
# geometry_msgs/Point message instead.

float64 x
float64 y
float64 z"""
  __slots__ = ['linear','angular']
  _slot_types = ['geometry_msgs/Vector3','geometry_msgs/Vector3']

  def __init__(self, *args, **kwds):
    """
    Constructor. Any message fields that are implicitly/explicitly
    set to None will be assigned a default value. The recommend
    use is keyword arguments as this is more robust to future message
    changes.  You cannot mix in-order arguments and keyword arguments.

    The available fields are:
       linear,angular

    :param args: complete set of field values, in .msg order
    :param kwds: use keyword arguments corresponding to message field names
    to set specific fields.
    """
    if args or kwds:
      pass
      #message fields cannot be None, assign default values for those that are
      if self.linear is None:
        self.linear = geometry_msgs.msg.Vector3()
      if self.angular is None:
        self.angular = geometry_msgs.msg.Vector3()
    else:
      self.linear = geometry_msgs.msg.Vector3()
      self.angular = geometry_msgs.msg.Vector3()

  def _get_types(self):
    """
    internal API method
    """
    return self._slot_types