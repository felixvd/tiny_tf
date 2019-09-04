# Software License Agreement (BSD License)
#
# Copyright (c) 2008, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""
Support library for Python autogenerated message files. This defines
the Message base class used by genpy as well as support
libraries for type checking and retrieving message classes by type
name.
"""

import math
import itertools
import struct
import sys
import yaml

from .. import genmsg

from .base import is_simple
from .rostime import Time, Duration, TVal

try:
    reload  # Python 2
except NameError:  # Python 3
    from importlib import reload

# common struct pattern singletons for msgs to use. Although this
# would better placed in a generator-specific module, we don't want to
# add another import to messages (which incurs higher import cost)

if sys.version > '3':
    long = int

struct_I = struct.Struct('<I')

def isstring(s):
    """Small helper version to check an object is a string in a way that works
    for both Python 2 and 3
    """
    try:
        return isinstance(s, basestring)
    except NameError:
        return isinstance(s, str)

class MessageException(Exception):
    """
    Base exception type for errors in genmsg routines
    """
    pass

class DeserializationError(MessageException):
    """Message deserialization error"""
    pass

class SerializationError(MessageException):
    """Message serialization error"""
    pass

# we expose the generic message-strify routine for fn-oriented code like rostopic

def strify_message(val, indent='', time_offset=None, current_time=None, field_filter=None, fixed_numeric_width=None):
    """
    Convert value to string representation
    :param val: to convert to string representation. Most likely a Message.  ``Value``
    :param indent: indentation. If indent is set, then the return value will have a leading \n, ``str``
    :param time_offset: if not None, time fields will be displayed
      as deltas from  time_offset, ``Time``

    :param current_time: currently not used. Only provided for API
      compatibility. current_time passes in the current time with
      respect to the message, ``Time``
    :param field_filter: filter the fields that are strified for Messages, ``fn(Message)->iter(str)``
    :returns: string (YAML) representation of message, ``str``
    """

    type_ = type(val)
    if type_ in (int, long, float) and fixed_numeric_width is not None:
        if type_ is float:
            num_str = ('%.' + str(fixed_numeric_width) + 'f') % val
            return num_str[:max(num_str.find('.'), fixed_numeric_width)]
        else:
            return ('%' + str(fixed_numeric_width) + 'd') % val
    elif type_ in (int, long, float, bool):
        return str(val)
    elif isstring(val):
        if not val:
            return "''"
        # escape strings for use in yaml file using yaml dump with default style to avoid trailing "...\n"
        return yaml.dump(val, default_style='"').rstrip('\n')
    elif isinstance(val, TVal):
        
        if time_offset is not None and isinstance(val, Time):
            val = val-time_offset

        if fixed_numeric_width is not None:
            format_str = '%' + str(fixed_numeric_width) + 'd'
            sec_str = '\n%ssecs: ' % indent + (format_str % val.secs)
            nsec_str = '\n%snsecs: ' % indent + (format_str % val.nsecs)
            return sec_str + nsec_str
        else:
            return '\n%ssecs: %s\n%snsecs: %9d'%(indent, val.secs, indent, val.nsecs)
        
    elif type_ in (list, tuple):
        if len(val) == 0:
            return "[]"
        val0 = val[0]
        if type(val0) in (int, float) and fixed_numeric_width is not None:
            list_str = '[' + ''.join(strify_message(v, indent, time_offset, current_time, field_filter, fixed_numeric_width) + ', ' for v in val).rstrip(', ') + ']'
            return list_str
        elif isstring(val0):
            # escape list of strings for use in yaml file using yaml dump
            return yaml.dump(val).rstrip('\n')
        elif type(val0) in (int, float, bool):
            return str(list(val))
        else:
            pref = indent + '- '
            indent = indent + '  '
            return '\n'+'\n'.join([pref+strify_message(v, indent, time_offset, current_time, field_filter, fixed_numeric_width) for v in val])
    elif isinstance(val, Message):
        # allow caller to select which fields of message are strified
        if field_filter is not None:
            fields = list(field_filter(val))
        else:
            fields = val.__slots__

        p = '%s%%s: %%s'%(indent)
        ni = '  '+indent
        if sys.hexversion > 0x03000000: #Python3
            vals = '\n'.join([p%(f,
                                 strify_message(_convert_getattr(val, f, t), ni, time_offset, current_time, field_filter, fixed_numeric_width)) for f,t in zip(val.__slots__, val._slot_types) if f in fields])			
        else: #Python2
            vals = '\n'.join([p%(f,
                                 strify_message(_convert_getattr(val, f, t), ni, time_offset, current_time, field_filter, fixed_numeric_width)) for f,t in itertools.izip(val.__slots__, val._slot_types) if f in fields])
        if indent:
            return '\n'+vals
        else:
            return vals
        
    else:
        return str(val) #punt

def _convert_getattr(val, f, t):
    """
    Convert atttribute types on the fly, if necessary.  This is mainly
    to convert uint8[] fields back to an array type.
    """
    attr = getattr(val, f)
    if isstring(attr) and 'uint8[' in t:
        return [ord(x) for x in attr]
    elif isinstance(attr, bytes) and 'uint8[' in t:
        return list(attr)
    else:
        return attr

# check_type mildly violates some abstraction boundaries between .msg
# representation and the python Message representation. The
# alternative is to have the message generator map .msg types to
# python types beforehand, but that would make it harder to do
# width/signed checks.

_widths = {
    'byte': 8, 'char': 8, 'int8': 8, 'uint8': 8,
    'int16': 16, 'uint16': 16, 
    'int32': 32, 'uint32': 32, 
    'int64': 64, 'uint64': 64, 
}

def check_type(field_name, field_type, field_val):
    """
    Dynamic type checker that maps ROS .msg types to python types and
    verifies the python value.  check_type() is not designed to be
    fast and is targeted at error diagnosis. This type checker is not
    designed to run fast and is meant only for error diagnosis.
    
    :param field_name: ROS .msg field name, ``str``
    :param field_type: ROS .msg field type, ``str``
    :param field_val: field value, ``Any``
    :raises: :exc:`SerializationError` If typecheck fails
    """
    if is_simple(field_type):
        # check sign and width
        if field_type in ['byte', 'int8', 'int16', 'int32', 'int64']:
            if type(field_val) not in [long, int]:
                raise SerializationError('field %s must be an integer type'%field_name)
            maxval = int(math.pow(2, _widths[field_type]-1))
            if field_val >= maxval or field_val <= -maxval:
                raise SerializationError('field %s exceeds specified width [%s]'%(field_name, field_type))
        elif field_type in ['char', 'uint8', 'uint16', 'uint32', 'uint64']:
            if type(field_val) not in [long, int] or field_val < 0:
                raise SerializationError('field %s must be unsigned integer type'%field_name)
            maxval = int(math.pow(2, _widths[field_type]))
            if field_val >= maxval:
                raise SerializationError('field %s exceeds specified width [%s]'%(field_name, field_type))
        elif field_type == 'bool':
            if field_val not in [True, False, 0, 1]:
                raise SerializationError('field %s is not a bool'%(field_name))
    elif field_type == 'string':
        if sys.hexversion > 0x03000000:
            if type(field_val) == str:
                try:
                    field_val.encode('ascii')
                except UnicodeEncodeError:
                    raise SerializationError('field %s is a non-ascii string'%field_name)
            elif not type(field_val) == bytes:
                raise SerializationError('field %s must be of type bytes or an ascii string'%field_name)
        else:		
            if type(field_val) == unicode:  # noqa: F821
                raise SerializationError('field %s is a unicode string instead of an ascii string'%field_name)
            elif not isstring(field_val):
                raise SerializationError('field %s must be of type str'%field_name)
    elif field_type == 'time':
        if not isinstance(field_val, Time):
            raise SerializationError('field %s must be of type Time'%field_name)
    elif field_type == 'duration':
        if not isinstance(field_val, Duration):
            raise SerializationError('field %s must be of type Duration'%field_name)
        
    elif field_type.endswith(']'): # array type
        # use index to generate error if '[' not present
        base_type = field_type[:field_type.index('[')]

        if type(field_val) == str:
            if not base_type in ['char', 'uint8']:
                raise SerializationError('field %s must be a list or tuple type. Only uint8[] can be a string' % field_name);
            else:
                #It's a string so its already in byte format and we
                #don't need to check the individual bytes in the
                #string.
                return
            
        if not type(field_val) in [list, tuple]:
            raise SerializationError('field %s must be a list or tuple type'%field_name)
        for v in field_val:
            check_type(field_name+"[]", base_type, v)
    else:
        if isinstance(field_val, Message):
            # roslib/Header is the old location of Header. We check it for backwards compat
            if field_val._type in ['std_msgs/Header', 'roslib/Header']:
                if field_type not in ['Header', 'std_msgs/Header', 'roslib/Header']:
                    raise SerializationError("field %s must be a Header instead of a %s"%(field_name, field_val._type))
            elif field_val._type != field_type:
                raise SerializationError("field %s must be of type %s instead of %s"%(field_name, field_type, field_val._type))
            for n, t in zip(field_val.__slots__, field_val._get_types()):
                check_type("%s.%s"%(field_name,n), t, getattr(field_val, n))
        else:
            raise SerializationError("field %s must be of type [%s]"%(field_name, field_type))

        #TODO: dynamically load message class and do instance compare

class Message(object):
    """Base class of Message data classes auto-generated from msg files. """

    # slots is explicitly both for data representation and
    # performance. Higher-level code assumes that there is a 1-to-1
    # mapping between __slots__ and message fields. In terms of
    # performance, explicitly settings slots eliminates dictionary for
    # new-style object.
    __slots__ = ['_connection_header']
    
    def __init__(self, *args, **kwds):
        """
        Create a new Message instance. There are multiple ways of
        initializing Message instances, either using a 1-to-1
        correspondence between constructor arguments and message
        fields (*args), or using Python "keyword" arguments (**kwds) to initialize named field
        and leave the rest with default values.
        """
        if args and kwds:
            raise TypeError("Message constructor may only use args OR keywords, not both")
        if args:
            if len(args) != len(self.__slots__):
                raise TypeError("Invalid number of arguments, args should be %s"%str(self.__slots__)+" args are"+str(args))
            for i, k in enumerate(self.__slots__):
                setattr(self, k, args[i])
        else:
            # validate kwds
            for k,v in kwds.items():
                if not k in self.__slots__:
                    raise AttributeError("%s is not an attribute of %s"%(k, self.__class__.__name__))
            # iterate through slots so all fields are initialized.
            # this is important so that subclasses don't reference an
            # uninitialized field and raise an AttributeError.
            for k in self.__slots__:
                if k in kwds:
                    setattr(self, k, kwds[k])
                else:
                    setattr(self, k, None)

    def __getstate__(self):
        """
        support for Python pickling
        """
        return [getattr(self, x) for x in self.__slots__]

    def __setstate__(self, state):
        """
        support for Python pickling
        """
        for x, val in zip(self.__slots__, state):
            setattr(self, x, val)

    def _get_types(self):
        raise Exception("must be overriden")
    def _check_types(self, exc=None):
        """
        Perform dynamic type-checking of Message fields. This is performance intensive
        and is meant for post-error diagnosis
        :param exc: underlying exception that gave cause for type check, ``Exception``
        :raises: exc:`genpy.SerializationError` If typecheck fails
        """
        for n, t in zip(self.__slots__, self._get_types()):
            check_type(n, t, getattr(self, n))
        if exc: # if exc is set and check_type could not diagnose, raise wrapped error
            raise SerializationError(str(exc))

    def serialize(self, buff):
        """
        Serialize data into buffer
        :param buff: buffer, ``StringIO``
        """
        pass
    def deserialize(self, str):
        """
        Deserialize data in str into this instance
        :param str: serialized data, ``str``
        """
        pass
    def __repr__(self):
        return strify_message(self)
    def __str__(self):
        return strify_message(self)
    # TODO: unit test
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        for f in self.__slots__:
            try:
                v1 = getattr(self, f) 
                v2 = getattr(other, f)
                if type(v1) in (list, tuple) and type(v2) in (list, tuple):
                    # we treat tuples and lists as equivalent
                    if tuple(v1) != tuple(v2):
                        return False
                elif not v1 == v2:
                    return False
            except AttributeError:
                return False
        return True
    def __ne__(self, other):
        return not self == other
    

def get_printable_message_args(msg, buff=None, prefix=''):
    """
    Get string representation of msg arguments
    :param msg: msg message to fill, ``Message``
    :param prefix: field name prefix (for verbose printing), ``str``
    :returns: printable representation of  msg args, ``str``
    """
    try:
        from cStringIO import StringIO # Python 2.x
        python3 = 0
    except ImportError:
        from io import BytesIO # Python 3.x
        python3 = 1

    if buff is None:
        if python3 == 1:
            buff = BytesIO()
        else: 
            buff = StringIO()
    for f in msg.__slots__:
        if isinstance(getattr(msg, f), Message):
            get_printable_message_args(getattr(msg, f), buff=buff, prefix=(prefix+f+'.'))
        else:
            buff.write(prefix+f+' ')
    return buff.getvalue().rstrip()

def _fill_val(msg, f, v, keys, prefix):
    """
    Subroutine of L{_fill_message_args()}. Sets a particular field on a message
    :param f: field name, ``str``
    :param v: field value
    :param keys: keys to use as substitute values for messages and timestamps, ``dict``
    :raises: exc:`MessageException`
    """
    if not f in msg.__slots__:
        raise MessageException("No field name [%s%s]"%(prefix, f))
    def_val = getattr(msg, f)
    if isinstance(def_val, Message) or isinstance(def_val, TVal):
        # check for substitution key, e.g. 'now'
        if type(v) == str:
            if v in keys:
                setattr(msg, f, keys[v])
            else:
                raise MessageException("No key named [%s]"%(v))
        elif isinstance(def_val, TVal) and type(v) in (int, long):
            #special case to handle time value represented as a single number
            #TODO: this is a lossy conversion
            if isinstance(def_val, Time):
                setattr(msg, f, Time.from_sec(v/1e9))
            elif isinstance(def_val, Duration):                    
                setattr(msg, f, Duration.from_sec(v/1e9))
            else:
                raise MessageException("Cannot create time values of type [%s]"%(type(def_val)))
        else:
            _fill_message_args(def_val, v, keys, prefix=(prefix+f+'.'))
    elif type(def_val) == list:
        if not type(v) in [list, tuple]:
            raise MessageException("Field [%s%s] must be a list or tuple instead of: %s"%(prefix, f, type(v).__name__))
        # determine base_type of field by looking at _slot_types
        idx = msg.__slots__.index(f)
        t = msg._slot_types[idx]
        base_type, is_array, length = genmsg.msgs.parse_type(t)
        # - for primitives, we just directly set (we don't
        #   type-check. we rely on serialization type checker)
        if base_type in genmsg.msgs.PRIMITIVE_TYPES:
            # 3785
            if length is not None and len(v) != length:
                raise MessageException("Field [%s%s] has incorrect number of elements: %s != %s"%(prefix, f, len(v), length))                
            setattr(msg, f, v)

        # - for complex types, we have to iteratively append to def_val
        else:
            # 3785            
            if length is not None and len(v) != length:
                raise MessageException("Field [%s%s] has incorrect number of elements: %s != %s"%(prefix, f, len(v), length))
            list_msg_class = get_message_class(base_type)
            if list_msg_class is None:
                raise MessageException("Cannot instantiate messages for field [%s%s] : cannot load class %s"%(prefix, f, base_type))                
            del def_val[:]
            for el in v:
                inner_msg = list_msg_class()
                if isinstance(inner_msg, TVal) and type(el) in (int, long):
                    #special case to handle time value represented as a single number
                    #TODO: this is a lossy conversion
                    if isinstance(inner_msg, Time):
                        inner_msg = Time.from_sec(el/1e9)
                    elif isinstance(inner_msg, Duration):
                        inner_msg = Duration.from_sec(el/1e9)
                    else:
                        raise MessageException("Cannot create time values of type [%s]"%(type(inner_msg)))
                else:
                    _fill_message_args(inner_msg, el, keys, prefix)
                def_val.append(inner_msg)
    else:
        setattr(msg, f, v)
    
    
def _fill_message_args(msg, msg_args, keys, prefix=''):
    """
    Populate message with specified args.
    
    :param msg: message to fill, ``Message``
    :param msg_args: list of arguments to set fields to, ``[args]``
    :param keys: keys to use as substitute values for messages and timestamps.  ``dict``
    :param prefix: field name prefix (for verbose printing), ``str``
    :returns: unused/leftover message arguments.  ``[args]``
    :raise :exc:`MessageException` If not enough message arguments to fill message
    :raises: :exc:`ValueError` If msg or msg_args is not of correct type
    """
    if not isinstance(msg, (Message, TVal)):
        raise ValueError("msg must be a Message instance: %s"%msg)

    if type(msg_args) == dict:
        
        #print "DICT ARGS", msg_args
        #print "ACTIVE SLOTS",msg.__slots__
        
        for f, v in msg_args.items():
            # assume that an empty key is actually an empty string
            if v == None:
                v = ''
            _fill_val(msg, f, v, keys, prefix)
    elif type(msg_args) == list:
        
        #print "LIST ARGS", msg_args
        #print "ACTIVE SLOTS",msg.__slots__
        
        if len(msg_args) > len(msg.__slots__):
            raise MessageException("Too many arguments:\n * Given: %s\n * Expected: %s"%(msg_args, msg.__slots__))
        elif len(msg_args) < len(msg.__slots__):
            raise MessageException("Not enough arguments:\n * Given: %s\n * Expected: %s"%(msg_args, msg.__slots__))
        
        for f, v in zip(msg.__slots__, msg_args):
            _fill_val(msg, f, v, keys, prefix)
    else:
        raise ValueError("invalid msg_args type: %s"%str(msg_args))

def fill_message_args(msg, msg_args, keys={}):
    """
    Populate message with specified args. Args are assumed to be a
    list of arguments from a command-line YAML parser. See
    http://www.ros.org/wiki/ROS/YAMLCommandLine for specification on
    how messages are filled.

    fill_message_args also takes in an optional 'keys' dictionary
    which contain substitute values for message and time types. These
    values must be of the correct instance type, i.e. a Message, Time,
    or Duration. In a string key is encountered with these types, the
    value from the keys dictionary will be used instead. This is
    mainly used to provide values for the 'now' timestamp.

    :param msg: message to fill, ``Message``
    :param msg_args: list of arguments to set fields to, or 
      If None, msg_args will be made an empty list., ``[args]``
    :param keys: keys to use as substitute values for messages and timestamps, ``dict``
    :raises: :exc:`MessageException` If not enough/too many message arguments to fill message
    """
    # a list of arguments is similar to python's
    # *args, whereas dictionaries are like **kwds. 

    # empty messages serialize as a None, which we make equivalent to
    # an empty message
    if msg_args is None:
        msg_args = []
    
    # msg_args is always a list, due to the fact it is parsed from a
    # command-line argument list.  We have to special-case handle a
    # list with a single dictionary, which has precedence over the
    # general list representation. We offer this precedence as there
    # is no other way to do kwd assignments into the outer message.
    if len(msg_args) == 1 and type(msg_args[0]) == dict:
        # according to spec, if we only get one msg_arg and it's a dictionary, we
        # use it directly
        _fill_message_args(msg, msg_args[0], keys, '')
    else:
        _fill_message_args(msg, msg_args, keys, '')

def _get_message_or_service_class(type_str, message_type, reload_on_error=False):
    """
    Utility for retrieving message/service class instances. Used by
    get_message_class and get_service_class. 
    :param type_str: 'msg' or 'srv', ``str``
    :param message_type: type name of message/service, ``str``
    :returns: Message/Service  for message/service type or None, ``class``
    :raises: :exc:`ValueError` If message_type is invalidly specified
    """
    if message_type == 'time':
        return Time
    if message_type == 'duration':
        return Duration
    ## parse package and local type name for import
    package, base_type = genmsg.package_resource_name(message_type)
    if not package:
        if base_type == 'Header':
            package = 'std_msgs'
        else:
            raise ValueError("message type is missing package name: %s"%str(message_type))
    pypkg = val = None
    try:
        # import the package
        pypkg = __import__('%s.%s' % (package, type_str))
    except ImportError:
        # try importing from dry package if available
        try:
            from roslib import load_manifest
            from rospkg import ResourceNotFound
            try:
                load_manifest(package)
                try:
                    pypkg = __import__('%s.%s' % (package, type_str))
                except ImportError:
                    pass
            except ResourceNotFound:
                pass
        except ImportError:
            pass
    if pypkg:
        try:
            val = getattr(getattr(pypkg, type_str), base_type)
        except AttributeError:
            pass

    # this logic is mainly to support rosh, so that a user doesn't
    # have to exit a shell just because a message wasn't built yet
    if val is None and reload_on_error:
        try:
            if pypkg:
                reload(pypkg)
            val = getattr(getattr(pypkg, type_str), base_type)
        except:
            val = None
    return val
        
## cache for get_message_class
_message_class_cache = {}

def get_message_class(message_type, reload_on_error=False):
    """
    Get the message class. NOTE: this function maintains a
    local cache of results to improve performance.
    :param message_type: type name of message, ``str``
    :param reload_on_error: (optional). Attempt to reload the Python
      module if unable to load message the first time. Defaults to
      False. This is necessary if messages are built after the first load.
    :returns: Message class for message/service type, ``Message class``
    :raises :exc:`ValueError`: if  message_type is invalidly specified
    """
    if message_type in _message_class_cache:
        return _message_class_cache[message_type]
    cls = _get_message_or_service_class('msg', message_type, reload_on_error=reload_on_error)
    if cls:
        _message_class_cache[message_type] = cls
    return cls

## cache for get_service_class
_service_class_cache = {}

def get_service_class(service_type, reload_on_error=False):
    """
    Get the service class. NOTE: this function maintains a
    local cache of results to improve performance.
    :param service_type: type name of service, ``str``
    :param reload_on_error: (optional). Attempt to reload the Python
      module if unable to load message the first time. Defaults to
      False. This is necessary if messages are built after the first load.
    :returns: Service class for service type, ``Service class``
    :raises :exc:`Exception` If service_type is invalidly specified
    """
    if service_type in _service_class_cache:
        return _service_class_cache[service_type]
    cls = _get_message_or_service_class('srv', service_type, reload_on_error=reload_on_error)
    _service_class_cache[service_type] = cls
    return cls

