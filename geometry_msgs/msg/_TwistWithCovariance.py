# This Python file uses the following encoding: utf-8
"""Based on a ROS-generated file from geometry_msgs/TwistWithCovariance.msg. Do not edit."""
import sys
python3 = True if sys.hexversion > 0x03000000 else False

import struct

import geometry_msgs.msg

class TwistWithCovariance():
  _md5sum = "1fe8a28e6890a4cc3ae4c3ca5c7d82e6"
  _type = "geometry_msgs/TwistWithCovariance"
  _has_header = False #flag to mark the presence of a Header object
  _full_text = """# This expresses velocity in free space with uncertainty.

Twist twist

# Row-major representation of the 6x6 covariance matrix
# The orientation parameters use a fixed-axis representation.
# In order, the parameters are:
# (x, y, z, rotation about X axis, rotation about Y axis, rotation about Z axis)
float64[36] covariance

================================================================================
MSG: geometry_msgs/Twist
# This expresses velocity in free space broken into its linear and angular parts.
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
  __slots__ = ['twist','covariance']
  _slot_types = ['geometry_msgs/Twist','float64[36]']

  def __init__(self, *args, **kwds):
    """
    Constructor. Any message fields that are implicitly/explicitly
    set to None will be assigned a default value. The recommend
    use is keyword arguments as this is more robust to future message
    changes.  You cannot mix in-order arguments and keyword arguments.

    The available fields are:
       twist,covariance

    :param args: complete set of field values, in .msg order
    :param kwds: use keyword arguments corresponding to message field names
    to set specific fields.
    """
    if args or kwds:
      super(TwistWithCovariance, self).__init__(*args, **kwds)
      #message fields cannot be None, assign default values for those that are
      if self.twist is None:
        self.twist = geometry_msgs.msg.Twist()
      if self.covariance is None:
        self.covariance = [0.] * 36
    else:
      self.twist = geometry_msgs.msg.Twist()
      self.covariance = [0.] * 36

  def _get_types(self):
    """
    internal API method
    """
    return self._slot_types