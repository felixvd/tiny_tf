# This Python file uses the following encoding: utf-8
"""Based on a ROS-generated file from geometry_msgs/PoseWithCovariance.msg. Do not edit."""
import sys
python3 = True if sys.hexversion > 0x03000000 else False

import struct

import geometry_msgs.msg

class PoseWithCovariance():
  _md5sum = "c23e848cf1b7533a8d7c259073a97e6f"
  _type = "geometry_msgs/PoseWithCovariance"
  _has_header = False #flag to mark the presence of a Header object
  _full_text = """# This represents a pose in free space with uncertainty.

Pose pose

# Row-major representation of the 6x6 covariance matrix
# The orientation parameters use a fixed-axis representation.
# In order, the parameters are:
# (x, y, z, rotation about X axis, rotation about Y axis, rotation about Z axis)
float64[36] covariance

================================================================================
MSG: geometry_msgs/Pose
# A representation of pose in free space, composed of position and orientation. 
Point position
Quaternion orientation

================================================================================
MSG: geometry_msgs/Point
# This contains the position of a point in free space
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
  __slots__ = ['pose','covariance']
  _slot_types = ['geometry_msgs/Pose','float64[36]']

  def __init__(self, *args, **kwds):
    """
    Constructor. Any message fields that are implicitly/explicitly
    set to None will be assigned a default value. The recommend
    use is keyword arguments as this is more robust to future message
    changes.  You cannot mix in-order arguments and keyword arguments.

    The available fields are:
       pose,covariance

    :param args: complete set of field values, in .msg order
    :param kwds: use keyword arguments corresponding to message field names
    to set specific fields.
    """
    if args or kwds:
      pass
      #message fields cannot be None, assign default values for those that are
      if self.pose is None:
        self.pose = geometry_msgs.msg.Pose()
      if self.covariance is None:
        self.covariance = [0.] * 36
    else:
      self.pose = geometry_msgs.msg.Pose()
      self.covariance = [0.] * 36

  def _get_types(self):
    """
    internal API method
    """
    return self._slot_types