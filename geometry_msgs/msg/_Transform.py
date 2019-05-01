# This Python file uses the following encoding: utf-8
"""Based on a ROS-generated file from geometry_msgs/Transform.msg. Do not edit."""
import sys
python3 = True if sys.hexversion > 0x03000000 else False

import struct

import geometry_msgs.msg

class Transform():
  _md5sum = "ac9eff44abf714214112b05d54a3cf9b"
  _type = "geometry_msgs/Transform"
  _has_header = False #flag to mark the presence of a Header object
  _full_text = """# This represents the transform between two coordinate frames in free space.

Vector3 translation
Quaternion rotation

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
float64 z
================================================================================
MSG: geometry_msgs/Quaternion
# This represents an orientation in free space in quaternion form.

float64 x
float64 y
float64 z
float64 w
"""
  __slots__ = ['translation','rotation']
  _slot_types = ['geometry_msgs/Vector3','geometry_msgs/Quaternion']

  def __init__(self, *args, **kwds):
    """
    Constructor. Any message fields that are implicitly/explicitly
    set to None will be assigned a default value. The recommend
    use is keyword arguments as this is more robust to future message
    changes.  You cannot mix in-order arguments and keyword arguments.

    The available fields are:
       translation,rotation

    :param args: complete set of field values, in .msg order
    :param kwds: use keyword arguments corresponding to message field names
    to set specific fields.
    """
    if args or kwds:
      super(Transform, self).__init__(*args, **kwds)
      #message fields cannot be None, assign default values for those that are
      if self.translation is None:
        self.translation = geometry_msgs.msg.Vector3()
      if self.rotation is None:
        self.rotation = geometry_msgs.msg.Quaternion()
    else:
      self.translation = geometry_msgs.msg.Vector3()
      self.rotation = geometry_msgs.msg.Quaternion()

  def _get_types(self):
    """
    internal API method
    """
    return self._slot_types