# This Python file uses the following encoding: utf-8
"""Based on a ROS-generated file from std_msgs/MultiArrayLayout.msg. Do not edit."""
import sys
python3 = True if sys.hexversion > 0x03000000 else False

import struct

import std_msgs.msg

class MultiArrayLayout():
  _md5sum = "0fed2a11c13e11c5571b4e2a995a91a3"
  _type = "std_msgs/MultiArrayLayout"
  _has_header = False #flag to mark the presence of a Header object
  _full_text = """# The multiarray declares a generic multi-dimensional array of a
# particular data type.  Dimensions are ordered from outer most
# to inner most.

MultiArrayDimension[] dim # Array of dimension properties
uint32 data_offset        # padding elements at front of data

# Accessors should ALWAYS be written in terms of dimension stride
# and specified outer-most dimension first.
# 
# multiarray(i,j,k) = data[data_offset + dim_stride[1]*i + dim_stride[2]*j + k]
#
# A standard, 3-channel 640x480 image with interleaved color channels
# would be specified as:
#
# dim[0].label  = "height"
# dim[0].size   = 480
# dim[0].stride = 3*640*480 = 921600  (note dim[0] stride is just size of image)
# dim[1].label  = "width"
# dim[1].size   = 640
# dim[1].stride = 3*640 = 1920
# dim[2].label  = "channel"
# dim[2].size   = 3
# dim[2].stride = 3
#
# multiarray(i,j,k) refers to the ith row, jth column, and kth channel.

================================================================================
MSG: std_msgs/MultiArrayDimension
string label   # label of given dimension
uint32 size    # size of given dimension (in type units)
uint32 stride  # stride of given dimension"""
  __slots__ = ['dim','data_offset']
  _slot_types = ['std_msgs/MultiArrayDimension[]','uint32']

  def __init__(self, *args, **kwds):
    """
    Constructor. Any message fields that are implicitly/explicitly
    set to None will be assigned a default value. The recommend
    use is keyword arguments as this is more robust to future message
    changes.  You cannot mix in-order arguments and keyword arguments.

    The available fields are:
       dim,data_offset

    :param args: complete set of field values, in .msg order
    :param kwds: use keyword arguments corresponding to message field names
    to set specific fields.
    """
    if args or kwds:
      super(MultiArrayLayout, self).__init__(*args, **kwds)
      #message fields cannot be None, assign default values for those that are
      if self.dim is None:
        self.dim = []
      if self.data_offset is None:
        self.data_offset = 0
    else:
      self.dim = []
      self.data_offset = 0

  def _get_types(self):
    """
    internal API method
    """
    return self._slot_types