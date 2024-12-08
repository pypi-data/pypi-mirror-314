from avlos import get_registry
from avlos.mixins.comm_node import CommNode
from avlos.mixins.named_node import NamedNode
from avlos.mixins.meta_node import MetaNode
from avlos.mixins.impex_node import ImpexNode
from avlos.mixins.func_attr_node import FuncAttrNode


class RemoteAttribute(CommNode, NamedNode, MetaNode, ImpexNode, FuncAttrNode):
    """
    Remote Endpoint with a value, parent and a comms channel
    """

    def __init__(
        self,
        name,
        summary,
        dtype,
        func_attr=None,
        getter_name=None,
        setter_name=None,
        unit=None,
        rst_target=None,
        ep_id=-1,
        meta={},
    ):
        CommNode.__init__(self)
        NamedNode.__init__(self, name)
        MetaNode.__init__(self, meta_dict=meta)
        FuncAttrNode.__init__(self, func_attr)
        self.summary = summary
        self.dtype = dtype
        self.unit = unit
        self.getter_name = getter_name
        self.setter_name = setter_name
        self.rst_target = rst_target
        self.ep_id = ep_id

    def get_value(self):
        assert self.getter_name, "No getter function available"
        self.channel.send([], self.ep_id)
        data = self.channel.recv(self.ep_id)
        value, *_ = self.channel.serializer.deserialize(data, self.dtype)
        try:
            return value * self.unit
        except TypeError:
            return value

    def set_value(self, __value):
        assert self.setter_name, "No setter function available"
        try:
            __value = __value.to(self.unit).magnitude
        except AttributeError:
            pass
        data = self.channel.serializer.serialize([__value], self.dtype)
        self.channel.send(data, self.ep_id)

    def set_value_with_string(self, __str_value):
        self.set_value(get_registry()(__str_value))

    def str_dump(self):                                                
         value = self.get_value()                                       
         if isinstance(value, (int, float)):                            
             format_str = "{0} [{1}]: {2:.6g}"                          
         else:                                                          
             format_str = "{0} [{1}]: {2}"                              
         return format_str.format(                                      
             self.name,                                                 
             self.dtype.nickname,                                       
             value                                                      
         )
