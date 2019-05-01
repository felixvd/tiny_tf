# This Python file uses the following encoding: utf-8
"""Based on a ROS-generated file from geometry_msgs/Wrench.msg. Do not edit."""
import sys
python3 = True if sys.hexversion > 0x03000000 else False

import struct

import geometry_msgs.msg

class Wrench():
  _md5sum = "4f539cf138b23283b520fd271b567936"
  _type = "geometry_msgs/Wrench"
  _has_header = False #flag to mark the presence of a Header object
  _full_text = """# This represents force in free space, separated into
# its linear and angular parts.
Vector3  force
Vector3  torque

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
  __slots__ = ['force','torque']
  _slot_types = ['geometry_msgs/Vector3','geometry_msgs/Vector3']

  def __init__(self, *args, **kwds):
    """
    Constructor. Any message fields that are implicitly/explicitly
    set to None will be assigned a default value. The recommend
    use is keyword arguments as this is more robust to future message
    changes.  You cannot mix in-order arguments and keyword arguments.

    The available fields are:
       force,torque

    :param args: complete set of field values, in .msg order
    :param kwds: use keyword arguments corresponding to message field names
    to set specific fields.
    """
    if args or kwds:
      pass
      #message fields cannot be None, assign default values for those that are
      if self.force is None:
        self.force = geometry_msgs.msg.Vector3()
      if self.torque is None:
        self.torque = geometry_msgs.msg.Vector3()
    else:
      self.force = geometry_msgs.msg.Vector3()
      self.torque = geometry_msgs.msg.Vector3()

  def _get_types(self):
    """
    internal API method
    """
    return self._slot_types