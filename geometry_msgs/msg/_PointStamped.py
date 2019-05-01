# This Python file uses the following encoding: utf-8
"""Based on a ROS-generated file from geometry_msgs/PointStamped.msg. Do not edit."""
import sys
python3 = True if sys.hexversion > 0x03000000 else False

import struct

import geometry_msgs.msg
import std_msgs.msg

class PointStamped():
  _md5sum = "c63aecb41bfdfd6b7e1fac37c7cbe7bf"
  _type = "geometry_msgs/PointStamped"
  _has_header = True #flag to mark the presence of a Header object
  _full_text = """# This represents a Point with reference coordinate frame and timestamp
Header header
Point point

================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
# 0: no frame
# 1: global frame
string frame_id

================================================================================
MSG: geometry_msgs/Point
# This contains the position of a point in free space
float64 x
float64 y
float64 z
"""
  __slots__ = ['header','point']
  _slot_types = ['std_msgs/Header','geometry_msgs/Point']

  def __init__(self, *args, **kwds):
    """
    Constructor. Any message fields that are implicitly/explicitly
    set to None will be assigned a default value. The recommend
    use is keyword arguments as this is more robust to future message
    changes.  You cannot mix in-order arguments and keyword arguments.

    The available fields are:
       header,point

    :param args: complete set of field values, in .msg order
    :param kwds: use keyword arguments corresponding to message field names
    to set specific fields.
    """
    if args or kwds:
      pass
      #message fields cannot be None, assign default values for those that are
      if self.header is None:
        self.header = std_msgs.msg.Header()
      if self.point is None:
        self.point = geometry_msgs.msg.Point()
    else:
      self.header = std_msgs.msg.Header()
      self.point = geometry_msgs.msg.Point()

  def _get_types(self):
    """
    internal API method
    """
    return self._slot_types