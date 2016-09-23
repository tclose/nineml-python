import unittest
from nineml.base import (BaseNineMLObject, DynamicPortsObject, ContainerObject, accessor_name_from_type)
from nineml.utils.testing.comprehensive import instances_of_all_types
from nineml.exceptions import (NineMLNameError, NineMLInvalidElementTypeException, NineMLRuntimeError)


class TestExceptions(unittest.TestCase):

    def test_accessor_name_from_type_ninemlinvalidelementtypeexception(self):
        """
        line #: 537
        message: Could not get member attr for element of type '{}', available types are {}

        context:
        --------
def accessor_name_from_type(class_map, element_type):
    \"\"\"
    Looks up the name of the accessor method from the nineml_type of the
    element argument for a given container type
    \"\"\"
    if not isinstance(element_type, basestring):
        element_type = element_type.nineml_type
    try:
        return class_map[element_type]
    except KeyError:
        """

        self.assertRaises(
            NineMLInvalidElementTypeException,
            accessor_name_from_type,
            class_map=None,
            element_type=None)


class TestBaseNineMLObjectExceptions(unittest.TestCase):

    def test_accept_visitor_notimplementederror(self):
        """
        line #: 77
        message: Derived class '{}' has not overriden accept_visitor method.

        context:
        --------
    def accept_visitor(self, visitor):
        """

        baseninemlobject = next(instances_of_all_types['BaseNineMLObject'].itervalues())
        self.assertRaises(
            NotImplementedError,
            baseninemlobject.accept_visitor,
            visitor=None)


class TestDynamicPortsObjectExceptions(unittest.TestCase):

    def test_port_ninemlnameerror(self):
        """
        line #: 222
        message: '{}' Dynamics object does not have a port named '{}'

        context:
        --------
    def port(self, name):
        try:
            return self.send_port(name)
        except NineMLNameError:
            try:
                return self.receive_port(name)
            except NineMLNameError:
        """

        dynamicportsobject = next(instances_of_all_types['DynamicPortsObject'].itervalues())
        self.assertRaises(
            NineMLNameError,
            dynamicportsobject.port,
            name=None)

    def test_receive_port_ninemlnameerror(self):
        """
        line #: 240
        message: '{}' Dynamics object does not have a receive port named '{}'

        context:
        --------
    def receive_port(self, name):
        try:
            return self.event_receive_port(name)
        except NineMLNameError:
            try:
                return self.analog_receive_port(name)
            except NineMLNameError:
                try:
                    return self.analog_reduce_port(name)
                except NineMLNameError:
        """

        dynamicportsobject = next(instances_of_all_types['DynamicPortsObject'].itervalues())
        self.assertRaises(
            NineMLNameError,
            dynamicportsobject.receive_port,
            name=None)

    def test_send_port_ninemlnameerror(self):
        """
        line #: 251
        message: '{}' Dynamics object does not have a send port named '{}'

        context:
        --------
    def send_port(self, name):
        try:
            return self.event_send_port(name)
        except NineMLNameError:
            try:
                return self.analog_send_port(name)
            except NineMLNameError:
        """

        dynamicportsobject = next(instances_of_all_types['DynamicPortsObject'].itervalues())
        self.assertRaises(
            NineMLNameError,
            dynamicportsobject.send_port,
            name=None)


class TestContainerObjectExceptions(unittest.TestCase):

    def test_add_ninemlruntimeerror(self):
        """
        line #: 346
        message: Could not add '{}' {} to component class as it clashes with an existing element of the same name

        context:
        --------
    def add(self, *elements):
        for element in elements:
            dct = self._member_dict(element)
            if element._name in dct:
        """

        containerobject = next(instances_of_all_types['ContainerObject'].itervalues())
        self.assertRaises(
            NineMLRuntimeError,
            containerobject.add)

    def test_remove_ninemlruntimeerror(self):
        """
        line #: 358
        message: Could not remove '{}' from component class as it was not found in member dictionary (use 'ignore_missing' option to ignore)

        context:
        --------
    def remove(self, *elements):
        for element in elements:
            dct = self._member_dict(element)
            try:
                del dct[element._name]
            except KeyError:
        """

        containerobject = next(instances_of_all_types['ContainerObject'].itervalues())
        self.assertRaises(
            NineMLRuntimeError,
            containerobject.remove)

    def test_element_ninemlnameerror(self):
        """
        line #: 424
        message: '{}' was not found in '{}' {} object

        context:
        --------
    def element(self, name, class_map=None, include_send_ports=False):
        \"\"\"
        Looks a member item by "name" (identifying characteristic)

        Parameters
        ----------
        name : str
            Name of the element to return
        class_map : dict[str, str]
            Mapping from element type to accessor name
        include_send_ports:
            As send ports will typically mask the name as an alias or
            state variable (although not necessarily in MultiDynamics objects)
            they are ignored unless this kwarg is set to True, in which case
            they will be returned only if no state variable or alias is found.

        Returns
        -------
        elem : NineMLBaseObject
            The element corresponding to the provided 'name' argument
        \"\"\"
        if class_map is None:
            class_map = self.class_to_member
        send_port = None
        for element_type in class_map:
            try:
                elem = self._member_accessor(
                    element_type, class_map=class_map)(name)
                # Ignore send ports as they otherwise mask
                # aliases/state variables
                if isinstance(elem, SendPortBase):
                    send_port = elem
                else:
                    return elem  # No need to wait to end of loop
            except NineMLNameError:
                pass
        if include_send_ports and send_port is not None:
            return send_port
        else:
        """

        containerobject = next(instances_of_all_types['ContainerObject'].itervalues())
        self.assertRaises(
            NineMLNameError,
            containerobject.element,
            name=None,
            class_map=None,
            include_send_ports=False)

    def test___iter___typeerror(self):
        """
        line #: 453
        message: '{}' {} container is not iterable

        context:
        --------
    def __iter__(self):
        """

        containerobject = next(instances_of_all_types['ContainerObject'].itervalues())
        self.assertRaises(
            TypeError,
            containerobject.__iter__)

