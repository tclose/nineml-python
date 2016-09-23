import unittest
from nineml.user.port_connections import (EventPortConnection, BasePortConnection, AnalogPortConnection)
from nineml.utils.testing.comprehensive import instances_of_all_types
from nineml.exceptions import (NineMLDimensionError, NineMLNameError, NineMLRuntimeError)


class TestEventPortConnectionExceptions(unittest.TestCase):

    def test__check_ports_ninemlruntimeerror(self):
        """
        line #: 382
        message: Send port '{}' must be an EventSendPort to be connected with an EventPortConnection

        context:
        --------
    def _check_ports(self):
        if not isinstance(self.send_port, EventSendPort):
        """

        eventportconnection = next(instances_of_all_types['EventPortConnection'].itervalues())
        self.assertRaises(
            NineMLRuntimeError,
            eventportconnection._check_ports)

    def test__check_ports_ninemlruntimeerror2(self):
        """
        line #: 386
        message: Send port '{}' must be an EventSendPort to be connected with an EventPortConnection

        context:
        --------
    def _check_ports(self):
        if not isinstance(self.send_port, EventSendPort):
            raise NineMLRuntimeError(
                "Send port '{}' must be an EventSendPort to be connected with"
                " an EventPortConnection".format(self.send_port.name))
        if not isinstance(self.receive_port, EventReceivePort):
        """

        eventportconnection = next(instances_of_all_types['EventPortConnection'].itervalues())
        self.assertRaises(
            NineMLRuntimeError,
            eventportconnection._check_ports)


class TestBasePortConnectionExceptions(unittest.TestCase):

    def test___init___ninemlruntimeerror(self):
        """
        line #: 52
        message: Both 'sender_role' ({}) and 'sender_name' ({}) cannot be provided to PortConnection __init__

        context:
        --------
    def __init__(self, send_port, receive_port,
                 sender_role=None, receiver_role=None,
                 sender_name=None, receiver_name=None):
        \"\"\"
        `send_port`     -- The name of the sending port
        `receiver_port` -- The name of the receiving port
        `sender_role`   -- A reference to the sending object via the role it
                           plays in the container
        `receiver_role` -- A reference to the receiving object via the role it
                           plays in the container
        `sender_name`   -- A reference to the sending object via its name,
                           which uniquely identifies it within the container
        `receiver_name` -- A reference to the receiving object via its name,
                           which uniquely identifies it within the container
        \"\"\"
        BaseULObject.__init__(self)
        if isinstance(send_port, basestring):
            self._send_port_name = send_port
            self._send_port = None
        else:
            self._send_port = send_port
            self._send_port_name = None
        if isinstance(receive_port, basestring):
            self._receive_port_name = receive_port
            self._receive_port = None
        else:
            self._receive_port = receive_port
            self._receive_port_name = None
        if sender_role is not None:
            if sender_name is not None:
        """

        baseportconnection = next(instances_of_all_types['BasePortConnection'].itervalues())
        self.assertRaises(
            NineMLRuntimeError,
            baseportconnection.__init__,
            send_port=None,
            receive_port=None,
            sender_role=None,
            receiver_role=None,
            sender_name=None,
            receiver_name=None)

    def test___init___ninemlruntimeerror2(self):
        """
        line #: 57
        message: Either 'sender_role' or 'sender_name' must be provided to PortConnection __init__

        context:
        --------
    def __init__(self, send_port, receive_port,
                 sender_role=None, receiver_role=None,
                 sender_name=None, receiver_name=None):
        \"\"\"
        `send_port`     -- The name of the sending port
        `receiver_port` -- The name of the receiving port
        `sender_role`   -- A reference to the sending object via the role it
                           plays in the container
        `receiver_role` -- A reference to the receiving object via the role it
                           plays in the container
        `sender_name`   -- A reference to the sending object via its name,
                           which uniquely identifies it within the container
        `receiver_name` -- A reference to the receiving object via its name,
                           which uniquely identifies it within the container
        \"\"\"
        BaseULObject.__init__(self)
        if isinstance(send_port, basestring):
            self._send_port_name = send_port
            self._send_port = None
        else:
            self._send_port = send_port
            self._send_port_name = None
        if isinstance(receive_port, basestring):
            self._receive_port_name = receive_port
            self._receive_port = None
        else:
            self._receive_port = receive_port
            self._receive_port_name = None
        if sender_role is not None:
            if sender_name is not None:
                raise NineMLRuntimeError(
                    "Both 'sender_role' ({}) and 'sender_name' ({}) cannot"
                    " be provided to PortConnection __init__"
                    .format(sender_role, sender_name))
        elif sender_name is None:
        """

        baseportconnection = next(instances_of_all_types['BasePortConnection'].itervalues())
        self.assertRaises(
            NineMLRuntimeError,
            baseportconnection.__init__,
            send_port=None,
            receive_port=None,
            sender_role=None,
            receiver_role=None,
            sender_name=None,
            receiver_name=None)

    def test___init___ninemlruntimeerror3(self):
        """
        line #: 62
        message: Both 'receiver_role' ({}) and 'receiver_name' ({}) cannot be provided to PortConnection __init__

        context:
        --------
    def __init__(self, send_port, receive_port,
                 sender_role=None, receiver_role=None,
                 sender_name=None, receiver_name=None):
        \"\"\"
        `send_port`     -- The name of the sending port
        `receiver_port` -- The name of the receiving port
        `sender_role`   -- A reference to the sending object via the role it
                           plays in the container
        `receiver_role` -- A reference to the receiving object via the role it
                           plays in the container
        `sender_name`   -- A reference to the sending object via its name,
                           which uniquely identifies it within the container
        `receiver_name` -- A reference to the receiving object via its name,
                           which uniquely identifies it within the container
        \"\"\"
        BaseULObject.__init__(self)
        if isinstance(send_port, basestring):
            self._send_port_name = send_port
            self._send_port = None
        else:
            self._send_port = send_port
            self._send_port_name = None
        if isinstance(receive_port, basestring):
            self._receive_port_name = receive_port
            self._receive_port = None
        else:
            self._receive_port = receive_port
            self._receive_port_name = None
        if sender_role is not None:
            if sender_name is not None:
                raise NineMLRuntimeError(
                    "Both 'sender_role' ({}) and 'sender_name' ({}) cannot"
                    " be provided to PortConnection __init__"
                    .format(sender_role, sender_name))
        elif sender_name is None:
            raise NineMLRuntimeError(
                "Either 'sender_role' or 'sender_name' must be "
                "provided to PortConnection __init__")
        if receiver_role is not None:
            if receiver_name is not None:
        """

        baseportconnection = next(instances_of_all_types['BasePortConnection'].itervalues())
        self.assertRaises(
            NineMLRuntimeError,
            baseportconnection.__init__,
            send_port=None,
            receive_port=None,
            sender_role=None,
            receiver_role=None,
            sender_name=None,
            receiver_name=None)

    def test___init___ninemlruntimeerror4(self):
        """
        line #: 67
        message: Either 'receiver_role' or 'receiver_name' must be provided to PortConnection __init__

        context:
        --------
    def __init__(self, send_port, receive_port,
                 sender_role=None, receiver_role=None,
                 sender_name=None, receiver_name=None):
        \"\"\"
        `send_port`     -- The name of the sending port
        `receiver_port` -- The name of the receiving port
        `sender_role`   -- A reference to the sending object via the role it
                           plays in the container
        `receiver_role` -- A reference to the receiving object via the role it
                           plays in the container
        `sender_name`   -- A reference to the sending object via its name,
                           which uniquely identifies it within the container
        `receiver_name` -- A reference to the receiving object via its name,
                           which uniquely identifies it within the container
        \"\"\"
        BaseULObject.__init__(self)
        if isinstance(send_port, basestring):
            self._send_port_name = send_port
            self._send_port = None
        else:
            self._send_port = send_port
            self._send_port_name = None
        if isinstance(receive_port, basestring):
            self._receive_port_name = receive_port
            self._receive_port = None
        else:
            self._receive_port = receive_port
            self._receive_port_name = None
        if sender_role is not None:
            if sender_name is not None:
                raise NineMLRuntimeError(
                    "Both 'sender_role' ({}) and 'sender_name' ({}) cannot"
                    " be provided to PortConnection __init__"
                    .format(sender_role, sender_name))
        elif sender_name is None:
            raise NineMLRuntimeError(
                "Either 'sender_role' or 'sender_name' must be "
                "provided to PortConnection __init__")
        if receiver_role is not None:
            if receiver_name is not None:
                raise NineMLRuntimeError(
                    "Both 'receiver_role' ({}) and 'receiver_name' ({}) cannot"
                    " be provided to PortConnection __init__"
                    .format(receiver_role, receiver_name))
        elif receiver_name is None:
        """

        baseportconnection = next(instances_of_all_types['BasePortConnection'].itervalues())
        self.assertRaises(
            NineMLRuntimeError,
            baseportconnection.__init__,
            send_port=None,
            receive_port=None,
            sender_role=None,
            receiver_role=None,
            sender_name=None,
            receiver_name=None)

    def test_sender_ninemlruntimeerror(self):
        """
        line #: 111
        message: Ports have not been bound

        context:
        --------
    def sender(self):
        if not self.is_bound():
        """

        baseportconnection = next(instances_of_all_types['BasePortConnection'].itervalues())
        with self.assertRaises(NineMLRuntimeError):
            print baseportconnection.sender

    def test_receiver_ninemlruntimeerror(self):
        """
        line #: 117
        message: Ports have not been bound

        context:
        --------
    def receiver(self):
        if not self.is_bound():
        """

        baseportconnection = next(instances_of_all_types['BasePortConnection'].itervalues())
        with self.assertRaises(NineMLRuntimeError):
            print baseportconnection.receiver

    def test_send_port_ninemlruntimeerror(self):
        """
        line #: 123
        message: Ports have not been bound

        context:
        --------
    def send_port(self):
        if not self.is_bound():
        """

        baseportconnection = next(instances_of_all_types['BasePortConnection'].itervalues())
        with self.assertRaises(NineMLRuntimeError):
            print baseportconnection.send_port

    def test_receive_port_ninemlruntimeerror(self):
        """
        line #: 129
        message: Ports have not been bound

        context:
        --------
    def receive_port(self):
        if not self.is_bound():
        """

        baseportconnection = next(instances_of_all_types['BasePortConnection'].itervalues())
        with self.assertRaises(NineMLRuntimeError):
            print baseportconnection.receive_port

    def test_sender_role_ninemlruntimeerror(self):
        """
        line #: 149
        message: Sender object was not identified by its role

        context:
        --------
    def sender_role(self):
        if self._sender_role is None:
        """

        baseportconnection = next(instances_of_all_types['BasePortConnection'].itervalues())
        with self.assertRaises(NineMLRuntimeError):
            print baseportconnection.sender_role

    def test_receiver_role_ninemlruntimeerror(self):
        """
        line #: 156
        message: Sender object was not identified by its role

        context:
        --------
    def receiver_role(self):
        if self._receiver_role is None:
        """

        baseportconnection = next(instances_of_all_types['BasePortConnection'].itervalues())
        with self.assertRaises(NineMLRuntimeError):
            print baseportconnection.receiver_role

    def test_sender_name_ninemlruntimeerror(self):
        """
        line #: 163
        message: Sender object was not identified by its name

        context:
        --------
    def sender_name(self):
        if self._sender_name is None:
        """

        baseportconnection = next(instances_of_all_types['BasePortConnection'].itervalues())
        with self.assertRaises(NineMLRuntimeError):
            print baseportconnection.sender_name

    def test_receiver_name_ninemlruntimeerror(self):
        """
        line #: 170
        message: Sender object was not identified by its name

        context:
        --------
    def receiver_name(self):
        if self._receiver_name is None:
        """

        baseportconnection = next(instances_of_all_types['BasePortConnection'].itervalues())
        with self.assertRaises(NineMLRuntimeError):
            print baseportconnection.receiver_name

    def test_bind_ninemlnameerror(self):
        """
        line #: 236
        message: Could not bind to missing send port, '{}', in '{}'

        context:
        --------
    def bind(self, container, to_roles=False):
        \"\"\"
        Binds the PortConnection to the components it is connecting
        \"\"\"
        # If the sender and receiver should be identified by their role
        # i.e. pre, pos, response, plasticity, etc... or by name
        if to_roles:
            self._sender = getattr(container, self.sender_role)
            self._receiver = getattr(container, self.receiver_role)
        else:
            self._sender = container[self.sender_name]
            self._receiver = container[self.receiver_name]
        try:
            self._send_port = self._sender.send_port(self.send_port_name)
        except NineMLNameError:
        """

        baseportconnection = next(instances_of_all_types['BasePortConnection'].itervalues())
        self.assertRaises(
            NineMLNameError,
            baseportconnection.bind,
            container=None,
            to_roles=False)

    def test_bind_ninemlnameerror2(self):
        """
        line #: 243
        message: Could not bind {} to missing receive port, '{}', in '{}'

        context:
        --------
    def bind(self, container, to_roles=False):
        \"\"\"
        Binds the PortConnection to the components it is connecting
        \"\"\"
        # If the sender and receiver should be identified by their role
        # i.e. pre, pos, response, plasticity, etc... or by name
        if to_roles:
            self._sender = getattr(container, self.sender_role)
            self._receiver = getattr(container, self.receiver_role)
        else:
            self._sender = container[self.sender_name]
            self._receiver = container[self.receiver_name]
        try:
            self._send_port = self._sender.send_port(self.send_port_name)
        except NineMLNameError:
            raise NineMLNameError(
                "Could not bind to missing send port, '{}', in '{}'"
                .format(self.send_port_name, self.sender.name))
        try:
            self._receive_port = self._receiver.receive_port(
                self.receive_port_name)
        except NineMLNameError:
        """

        baseportconnection = next(instances_of_all_types['BasePortConnection'].itervalues())
        self.assertRaises(
            NineMLNameError,
            baseportconnection.bind,
            container=None,
            to_roles=False)

    def test_from_tuple_ninemlruntimeerror(self):
        """
        line #: 314
        message: Did not find sender {} '{}' in '{}' container

        context:
        --------
    def from_tuple(cls, tple, container):
        # FIXME: Needs comments to explain what is going on and better
        #        exception messages
        sender, send_port, receiver, receive_port = tple
        init_kwargs = {}
        try:
            sender_dynamicss = getattr(container, sender).component_classes
            init_kwargs['sender_role'] = sender
        except AttributeError:
            try:
                sender_dynamicss = [container[sender].component_class]
                init_kwargs['sender_name'] = sender
            except (TypeError, KeyError), e:
        """

        self.assertRaises(
            NineMLRuntimeError,
            BasePortConnection.from_tuple,
            tple=None,
            container=None)

    def test_from_tuple_ninemlruntimeerror2(self):
        """
        line #: 326
        message: Did not find receiver {} '{}' in '{}' container

        context:
        --------
    def from_tuple(cls, tple, container):
        # FIXME: Needs comments to explain what is going on and better
        #        exception messages
        sender, send_port, receiver, receive_port = tple
        init_kwargs = {}
        try:
            sender_dynamicss = getattr(container, sender).component_classes
            init_kwargs['sender_role'] = sender
        except AttributeError:
            try:
                sender_dynamicss = [container[sender].component_class]
                init_kwargs['sender_name'] = sender
            except (TypeError, KeyError), e:
                raise NineMLRuntimeError(
                    "Did not find sender {} '{}' in '{}' container"
                    .format('name' if isinstance(e, KeyError) else 'role',
                            receiver, container.name))
        try:
            getattr(container, receiver).component_classes
            init_kwargs['receiver_role'] = receiver
        except AttributeError:
            try:
                container[receiver].component_class
                init_kwargs['receiver_name'] = receiver
            except (TypeError, KeyError), e:
        """

        self.assertRaises(
            NineMLRuntimeError,
            BasePortConnection.from_tuple,
            tple=None,
            container=None)

    def test_from_tuple_ninemlruntimeerror3(self):
        """
        line #: 336
        message: Mismatching port types for '{}' port in populations in Selection '{}'

        context:
        --------
    def from_tuple(cls, tple, container):
        # FIXME: Needs comments to explain what is going on and better
        #        exception messages
        sender, send_port, receiver, receive_port = tple
        init_kwargs = {}
        try:
            sender_dynamicss = getattr(container, sender).component_classes
            init_kwargs['sender_role'] = sender
        except AttributeError:
            try:
                sender_dynamicss = [container[sender].component_class]
                init_kwargs['sender_name'] = sender
            except (TypeError, KeyError), e:
                raise NineMLRuntimeError(
                    "Did not find sender {} '{}' in '{}' container"
                    .format('name' if isinstance(e, KeyError) else 'role',
                            receiver, container.name))
        try:
            getattr(container, receiver).component_classes
            init_kwargs['receiver_role'] = receiver
        except AttributeError:
            try:
                container[receiver].component_class
                init_kwargs['receiver_name'] = receiver
            except (TypeError, KeyError), e:
                raise NineMLRuntimeError(
                    "Did not find receiver {} '{}' in '{}' container"
                    .format('name' if isinstance(e, KeyError) else 'role',
                            receiver, container.name))
        port_type = None
        for dyn in sender_dynamicss:
            pt = dyn.port(send_port).nineml_type
            if port_type is None:
                port_type = pt
            elif port_type != pt:
        """

        self.assertRaises(
            NineMLRuntimeError,
            BasePortConnection.from_tuple,
            tple=None,
            container=None)


class TestAnalogPortConnectionExceptions(unittest.TestCase):

    def test__check_ports_ninemlruntimeerror(self):
        """
        line #: 358
        message: Send port '{}' must be an AnalogSendPort to be connected with an AnalogPortConnection

        context:
        --------
    def _check_ports(self):
        if not isinstance(self.send_port, AnalogSendPort):
        """

        analogportconnection = next(instances_of_all_types['AnalogPortConnection'].itervalues())
        self.assertRaises(
            NineMLRuntimeError,
            analogportconnection._check_ports)

    def test__check_ports_ninemlruntimeerror2(self):
        """
        line #: 363
        message: Send port '{}' must be an AnalogSendPort to be connected with an AnalogPortConnection

        context:
        --------
    def _check_ports(self):
        if not isinstance(self.send_port, AnalogSendPort):
            raise NineMLRuntimeError(
                "Send port '{}' must be an AnalogSendPort to be connected with"
                " an AnalogPortConnection".format(self.send_port.name))
        if not isinstance(self.receive_port, (AnalogReceivePort,
                                              AnalogReducePort)):
        """

        analogportconnection = next(instances_of_all_types['AnalogPortConnection'].itervalues())
        self.assertRaises(
            NineMLRuntimeError,
            analogportconnection._check_ports)

    def test__check_ports_ninemldimensionerror(self):
        """
        line #: 367
        message: Dimensions do not match in analog port connection: sender port '{}' has dimensions of '{}' and receive port '{}' has dimensions of '{}'

        context:
        --------
    def _check_ports(self):
        if not isinstance(self.send_port, AnalogSendPort):
            raise NineMLRuntimeError(
                "Send port '{}' must be an AnalogSendPort to be connected with"
                " an AnalogPortConnection".format(self.send_port.name))
        if not isinstance(self.receive_port, (AnalogReceivePort,
                                              AnalogReducePort)):
            raise NineMLRuntimeError(
                "Send port '{}' must be an AnalogSendPort to be connected with"
                " an AnalogPortConnection".format(self.receive_port.name))
        if self.send_port.dimension != self.receive_port.dimension:
        """

        analogportconnection = next(instances_of_all_types['AnalogPortConnection'].itervalues())
        self.assertRaises(
            NineMLDimensionError,
            analogportconnection._check_ports)

