# This Python file uses the following encoding: utf-8
"""Based on a ROS-generated file from geometry_msgs/Inertia.msg. Do not edit."""
import sys
python3 = True if sys.hexversion > 0x03000000 else False

import struct

import geometry_msgs.msg

class Inertia():
  _md5sum = "1d26e4bb6c83ff141c5cf0d883c2b0fe"
  _type = "geometry_msgs/Inertia"
  _has_header = False #flag to mark the presence of a Header object
  _full_text = """# Mass [kg]
float64 m

# Center of mass [m]
geometry_msgs/Vector3 com

# Inertia Tensor [kg-m^2]
#     | ixx ixy ixz |
# I = | ixy iyy iyz |
#     | ixz iyz izz |
float64 ixx
float64 ixy
float64 ixz
float64 iyy
float64 iyz
float64 izz

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
  __slots__ = ['m','com','ixx','ixy','ixz','iyy','iyz','izz']
  _slot_types = ['float64','geometry_msgs/Vector3','float64','float64','float64','float64','float64','float64']

  def __init__(self, *args, **kwds):
    """
    Constructor. Any message fields that are implicitly/explicitly
    set to None will be assigned a default value. The recommend
    use is keyword arguments as this is more robust to future message
    changes.  You cannot mix in-order arguments and keyword arguments.

    The available fields are:
       m,com,ixx,ixy,ixz,iyy,iyz,izz

    :param args: complete set of field values, in .msg order
    :param kwds: use keyword arguments corresponding to message field names
    to set specific fields.
    """
    if args or kwds:
      pass
      #message fields cannot be None, assign default values for those that are
      if self.m is None:
        self.m = 0.
      if self.com is None:
        self.com = geometry_msgs.msg.Vector3()
      if self.ixx is None:
        self.ixx = 0.
      if self.ixy is None:
        self.ixy = 0.
      if self.ixz is None:
        self.ixz = 0.
      if self.iyy is None:
        self.iyy = 0.
      if self.iyz is None:
        self.iyz = 0.
      if self.izz is None:
        self.izz = 0.
    else:
      self.m = 0.
      self.com = geometry_msgs.msg.Vector3()
      self.ixx = 0.
      self.ixy = 0.
      self.ixz = 0.
      self.iyy = 0.
      self.iyz = 0.
      self.izz = 0.

  def _get_types(self):
    """
    internal API method
    """
    return self._slot_types