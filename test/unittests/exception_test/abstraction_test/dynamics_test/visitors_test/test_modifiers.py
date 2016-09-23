import unittest
from nineml.abstraction.dynamics.visitors.modifiers import (DynamicsPortModifier)
from nineml.utils.testing.comprehensive import instances_of_all_types
from nineml.exceptions import (NineMLRuntimeError)


class TestDynamicsPortModifierExceptions(unittest.TestCase):

    def test_close_analog_port_ninemlruntimeerror(self):
        """
        line #: 61
        message: close_analog_port() on non-flat component_class

        context:
        --------
    def close_analog_port(cls, component_class, port_name, value="0"):
        \"\"\"Closes an incoming analog port by assigning its value to 0\"\"\"

        if not component_class.is_flat():
        """

        self.assertRaises(
            NineMLRuntimeError,
            DynamicsPortModifier.close_analog_port,
            component_class=None,
            port_name=None,
            value='0')

    def test_close_analog_port_typeerror(self):
        """
        line #: 78
        message: Expected an analog port

        context:
        --------
    def close_analog_port(cls, component_class, port_name, value="0"):
        \"\"\"Closes an incoming analog port by assigning its value to 0\"\"\"

        if not component_class.is_flat():
            raise NineMLRuntimeError('close_analog_port() on non-flat '
                                     'component_class')

        # Subsitute the value in:
        component_class.accept_visitor(cls._ExpandPortDefinition(port_name,
                                                                value))

        # Remove it from the list of ports:
        port = filter_expect_single(component_class.analog_ports,
                                    lambda ap: ap.name == port_name)
        if isinstance(port, AnalogSendPort):
            component_class._analog_send_ports.pop(port_name)
        elif isinstance(port, AnalogReceivePort):
            component_class._analog_receive_ports.pop(port_name)
        elif isinstance(port, AnalogReducePort):
            component_class._analog_reduce_ports.pop(port_name)
        else:
        """

        self.assertRaises(
            TypeError,
            DynamicsPortModifier.close_analog_port,
            component_class=None,
            port_name=None,
            value='0')

    def test_close_all_reduce_ports_ninemlruntimeerror(self):
        """
        line #: 87
        message: close_all_reduce_ports() on non-flat component_class

        context:
        --------
    def close_all_reduce_ports(cls, component_class, exclude=None):
        \"\"\"
        Closes all the ``reduce`` ports on a component_class by assigning them a
        value of 0
        \"\"\"
        if not component_class.is_flat():
        """

        self.assertRaises(
            NineMLRuntimeError,
            DynamicsPortModifier.close_all_reduce_ports,
            component_class=None,
            exclude=None)

    def test_rename_port_ninemlruntimeerror(self):
        """
        line #: 100
        message: rename_port() on non-flat component_class

        context:
        --------
    def rename_port(cls, component_class, old_port_name, new_port_name):
        \"\"\" Renames a port in a component_class \"\"\"
        if not component_class.is_flat():
        """

        self.assertRaises(
            NineMLRuntimeError,
            DynamicsPortModifier.rename_port,
            component_class=None,
            old_port_name=None,
            new_port_name=None)

    def test_remap_port_to_parameter_ninemlruntimeerror(self):
        """
        line #: 112
        message: rename_port_to_parameter() on non-flat component_class

        context:
        --------
    def remap_port_to_parameter(cls, component_class, port_name):
        \"\"\" Renames a port in a component_class \"\"\"
        if not component_class.is_flat():
        """

        self.assertRaises(
            NineMLRuntimeError,
            DynamicsPortModifier.remap_port_to_parameter,
            component_class=None,
            port_name=None)

