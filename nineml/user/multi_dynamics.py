from itertools import chain
from . import BaseULObject
from abc import ABCMeta
import sympy
from .component import Property
from itertools import product
from nineml.abstraction import (
    Dynamics, Alias, TimeDerivative, Regime, AnalogSendPort, AnalogReceivePort,
    AnalogReducePort, EventSendPort, EventReceivePort, OnEvent, OnCondition,
    StateAssignment, Trigger, OutputEvent, StateVariable)
from nineml.reference import resolve_reference, write_reference
from nineml import DocumentLevelObject
from nineml.xmlns import NINEML, E
from nineml.utils import expect_single, normalise_parameter_as_list
from nineml.user import DynamicsProperties
from nineml.annotations import annotate_xml, read_annotations
from nineml.values import ArrayValue
from nineml.exceptions import NineMLRuntimeError
from .port_connections import AnalogPortConnection, EventPortConnection


class MultiDynamicsProperties(DynamicsProperties):

    element_name = "MultiDynamics"
    defining_attributes = ('_name', '_sub_component_properties',
                           '_port_exposures', '_port_connections')

    def __init__(self, name, sub_components, port_connections,
                 port_exposures=[]):
        component_class = MultiDynamics(
            name + '_Dynamics',
            (p.component_class for p in sub_components),
            port_exposures, port_connections)
        super(MultiDynamicsProperties, self).__init__(
            name, definition=component_class,
            properties=chain(*[p.properties for p in sub_components]))
        self._sub_component_properties = dict(
            (p.name, p) for p in sub_components)

    @property
    def name(self):
        return self._name

    @property
    def sub_components(self):
        return self._sub_component_properties.itervalues()

    @property
    def port_connections(self):
        return iter(self._port_connections)

    @property
    def port_exposures(self):
        return self._port_exposures.itervalues()

    def sub_component(self, name):
        return self._sub_component_properties[name]

    def port_exposure(self, name):
        return self._port_exposures[name]

    @property
    def sub_component_names(self):
        return self.sub_component.iterkeys()

    @property
    def port_exposure_names(self):
        return self._port_exposures.iterkeys()

    @property
    def attributes_with_units(self):
        return chain(*[c.attributes_with_units
                       for c in self.sub_component])

    @write_reference
    @annotate_xml
    def to_xml(self, document, **kwargs):
        members = [c.to_xml(document, **kwargs)
                   for c in self.sub_component_properties]
        members.extend(pe.to_xml(document, **kwargs)
                        for pe in self.port_exposures)
        members.extend(pc.to_xml(document, **kwargs)
                       for pc in self.port_connections)
        return E(self.element_name, *members, name=self.name)

    @classmethod
    @resolve_reference
    @read_annotations
    def from_xml(cls, element, document, **kwargs):
        cls.check_tag(element)
        sub_component_properties = [
            SubDynamicsProperties.from_xml(e, document, **kwargs)
            for e in element.findall(NINEML + 'SubDynamics')]
        port_exposures = [
            AnalogSendPortExposure.from_xml(e, document, **kwargs)
            for e in element.findall(NINEML + 'AnalogSendPortExposure')]
        port_exposures.extend(
            AnalogReceivePortExposure.from_xml(e, document, **kwargs)
            for e in element.findall(NINEML + 'AnalogReceivePortExposure'))
        port_exposures.extend(
            AnalogReducePortExposure.from_xml(e, document, **kwargs)
            for e in element.findall(NINEML + 'AnalogReducePortExposure'))
        port_exposures.extend(
            EventSendPortExposure.from_xml(e, document, **kwargs)
            for e in element.findall(NINEML + 'EventSendPortExposure'))
        port_exposures.extend(
            EventReceivePortExposure.from_xml(e, document, **kwargs)
            for e in element.findall(NINEML + 'EventReceivePortExposure'))
        analog_port_connections = [
            AnalogPortConnection.from_xml(e, document, **kwargs)
            for e in element.findall(NINEML + 'AnalogPortConnection')]
        event_port_connections = [
            EventPortConnection.from_xml(e, document, **kwargs)
            for e in element.findall(NINEML + 'EventPortConnection')]
        return cls(name=element.attrib['name'],
                   sub_component_properties=sub_component_properties,
                   port_exposures=port_exposures,
                   port_connections=chain(analog_port_connections,
                                          event_port_connections))


class SubDynamicsProperties(BaseULObject):

    element_name = 'SubDynamicsProperties'
    defining_attributes = ('_name', '_dynamics')

    def __init__(self, name, component):
        BaseULObject.__init__(self)
        self._name = name
        self._component = component

    @property
    def name(self):
        return self._name

    @property
    def component(self):
        return (NamespaceProperty(self, p) for p in self._component.properties)

    @annotate_xml
    def to_xml(self, document, **kwargs):  # @UnusedVariable
        return E(self.element_name, self._component.to_xml(document, **kwargs),
                 name=self.name)

    @classmethod
    @read_annotations
    def from_xml(cls, element, document, **kwargs):
        try:
            dynamics_properties = DynamicsProperties.from_xml(
                expect_single(
                    element.findall(NINEML + 'DynamicsProperties')),
                document, **kwargs)
        except NineMLRuntimeError:
            dynamics_properties = MultiDynamicsProperties.from_xml(
                expect_single(
                    element.findall(NINEML + 'MultiDynamics')),
                document, **kwargs)
        return cls(element.attrib['name'], dynamics_properties)


class MultiDynamics(Dynamics):

    def __init__(self, name, sub_components, port_exposures, port_connections):
        # =====================================================================
        # Create the structures unique to MultiDynamics
        # =====================================================================
        self._sub_components = dict((d.name, d) for d in sub_components)
        self._port_exposures = dict((pe.name, pe) for pe in port_exposures)
        self._analog_port_connections = {}
        self._event_port_connections = {}
        self._reduce_port_connections = {}
        # Insert an empty list for each event and reduce port in the combined
        # model
        for sub_component in sub_components:
            self._event_port_connections.update(
                (in_namespace(p.name, sub_component.name), [])
                for p in sub_component.event_receive_ports)
            self._reduce_port_connections.update(
                (in_namespace(p.name, sub_component.name), [])
                for p in sub_component.analog_reduce_ports)
        # Parse port connections (from tuples if required), bind them to the
        # ports within the subcomponents and append them to their respective
        # member dictionaries
        for port_connection in port_connections:
            snd_id, rcv_id, snd_port_name, rcv_port_name = port_connection
            sender = self.sub_component(snd_id).component
            receiver = self.sub_component(rcv_id).component
            if isinstance(port_connection, tuple):
                if isinstance(sender.port(snd_port_name), AnalogReceivePort):
                    port_connection = LocalAnalogPortConnection(
                        *port_connection)
                elif isinstance(receiver.port(rcv_port_name),
                                EventReceivePort):
                    port_connection = LocalEventPortConnection(
                        *port_connection)
                else:
                    assert False
            elif isinstance(port_connection, AnalogPortConnection):
                port_connection = LocalAnalogPortConnection(*port_connection)
            elif isinstance(port_connection, EventPortConnection):
                port_connection = LocalEventPortConnection(*port_connection)
            else:
                raise NineMLRuntimeError(
                    "Unrecognised port connection '{}'"
                    .format(port_connection))
            port_connection.bind_ports(sender, receiver)
            rcv_name = in_namespace(rcv_port_name, rcv_id)
            if isinstance(port_connection, LocalAnalogPortConnection):
                if rcv_name in self._analog_port_connections:
                    raise NineMLRuntimeError(
                        "Multiple connections to receive port '{}' in '{} "
                        "sub-component of '{}'"
                        .format(port_connection.receive_port_name,
                                port_connection.receiver_id, name))
                self._analog_port_connections[rcv_name] = port_connection
            elif isinstance(port_connection, EventPortConnection):
                self._event_port_connections[rcv_name].append(port_connection)
            else:
                assert False
        # =====================================================================
        # Create the structures required for the Dynamics base class
        # =====================================================================
        # Create multi-regimes for each combination of regimes
        # from across all the sub components
        regimes = chain(
            *[MultiRegime(*rs) for rs in product(
                *[c.regimes for c in sub_components])])
        # All "true" aliases from all sub_components wrapped by
        # NamespaceAliases
        aliases = list(chain(*[c.aliases for c in sub_components]))
        # Translate analog port connections into Aliases remapping the names
        for (rcv_id, port_name), port_connection in (
                self._analog_port_connections.iteritems()):
            receive_name = in_namespace(port_name, rcv_id)
            send_name = in_namespace(port_connection.send_port_name,
                                               port_connection.send_id)
            aliases.append(Alias(receive_name, sympy.Symbol(send_name)))
        # Translate reduce port connections into Aliases remapping the names
        for (rcv_id, port_name), port_connections in (
                self._reduce_port_connections.iteritems()):
            receive_name = in_namespace(port_name, rcv_id)
            rhs = 0
            for port_connection in port_connections:
                send_name = in_namespace(
                    port_connection.send_port_name, port_connection.send_id)
                rhs += sympy.Symbol(send_name)
            aliases.append(Alias(receive_name, rhs))
        for exposure in port_exposures:
            raise NotImplementedError
        super(MultiDynamics, self).__init__(
            name=name,
            parameters=chain(*[c.parameters for c in sub_components]),
            regimes=regimes,
            aliases=aliases,
            constants=chain(*[c.constants for c in sub_components]),
            state_variables=chain(*[c.aliases for c in sub_components]))

    @property
    def sub_components(self):
        return self._sub_components.itervalues()

    @property
    def port_exposures(self):
        return self._port_exposures.itervalues()

    @property
    def analog_port_connections(self):
        return self._analog_port_connections.itervalues()

    @property
    def event_port_connections(self):
        return self._analog_port_connections.itervalues()

    @property
    def reduce_port_connections(self):
        return self._reduce_port_connections.itervalues()

    @property
    def port_connections(self):
        return chain(self.analog_port_connections, self.event_port_connections,
                     self.reduce_port_connections)

    def sub_component(self, name):
        return self._sub_components[name]

    def port_exposure(self, name):
        return self._port_exposures[name]


class SubDynamics(object):

    def __init__(self, name, component):
        self._name = name
        self._component = component

    @property
    def name(self):
        return self._name

    @property
    def component(self):
        return self._component

    @property
    def aliases(self):
        return (NamespaceAlias(self, a) for a in self.component.aliases)

    @property
    def state_variables(self):
        return (NamespaceStateVariable(self, v)
                for v in self.component.state_variables)

    @property
    def regimes(self):
        return (NamespaceRegime(self, r) for r in self.component.regimes)


class NamespaceNamed(object):
    """
    Abstract base class for wrappers of abstraction layer objects with names
    """

    def __init__(self, sub_component, element):
        self._sub_component = sub_component
        self._element = element

    @property
    def sub_component(self):
        return self._sub_component

    @property
    def element(self):
        return self._element

    @property
    def name(self):
        return self._in_namespace(self._element.name)

    def _in_namespace(self, name):
        return in_namespace(name + self._sub_component.name)


class NamespaceExpression(object):

    def __init__(self, sub_component, element):
        self._sub_component = sub_component
        self._element = element

    @property
    def lhs(self):
        return self.name

    def lhs_name_transform_inplace(self, name_map):
        raise NotImplementedError  # Not sure if this should be implemented yet

    @property
    def rhs(self):
        """Return copy of rhs with all free symols suffixed by the namespace"""
        try:
            return self.element.rhs.xreplace(dict(
                (s, sympy.Symbol(self._in_namespace(s)))
                for s in self.rhs_symbols))
        except AttributeError:  # If rhs has been simplified to ints/floats
            assert float(self.element.rhs)
            return self.rhs

    @rhs.setter
    def rhs(self, rhs):
        raise NotImplementedError  # Not sure if this should be implemented yet

    def rhs_name_transform_inplace(self, name_map):
        raise NotImplementedError  # Not sure if this should be implemented yet

    def rhs_substituted(self, name_map):
        raise NotImplementedError  # Not sure if this should be implemented yet

    def subs(self, old, new):
        raise NotImplementedError  # Not sure if this should be implemented yet

    def rhs_str_substituted(self, name_map={}, funcname_map={}):
        raise NotImplementedError  # Not sure if this should be implemented yet

    def _in_namespace(self, name):
        return in_namespace(name + self._sub_component.name)


class NamespaceRegime(NamespaceNamed, Regime):

    @property
    def time_derivatives(self):
        return (NamespaceTimeDerivative(self.sub_component, td)
                for td in self.element.time_derivatives)

    @property
    def aliases(self):
        return (NamespaceAlias(self.sub_component, a)
                for a in self.element.aliases)

    @property
    def on_events(self):
        return (NamespaceOnEvent(self.sub_component, oe)
                for oe in self.element.on_events)

    @property
    def on_conditions(self):
        return (NamespaceOnEvent(self.sub_component, oc)
                for oc in self.element.on_conditions)

    def time_derivative(self, name):
        return NamespaceTimeDerivative(self.sub_component,
                                       self.element.time_derivative(name))

    def alias(self, name):
        return NamespaceAlias(self.sub_component, self.element.alias(name))

    def on_event(self, name):
        return NamespaceOnEvent(self.sub_component,
                                self.element.on_event(name))

    def on_condition(self, name):
        return NamespaceOnEvent(self.sub_component,
                                self.element.on_condition(name))

    @property
    def num_time_derivatives(self):
        return self.element.num_time_derivatives

    @property
    def num_aliases(self):
        return self.num_element.aliases

    @property
    def num_on_events(self):
        return self.element.num_on_events

    @property
    def num_on_conditions(self):
        return self.element.num_on_conditions


class MultiRegime(Regime):

    def __init__(self, *regimes):
        self._regimes = regimes

    @property
    def regimes(self):
        return iter(self._regimes)

    @property
    def name(self):
        return '__'.join(r.name for r in self.regimes) + '__regime'

    @property
    def time_derivatives(self):
        return chain(*[r.time_derivatives for r in self.regimes])

    @property
    def aliases(self):
        return chain(*[r.aliases for r in self.regimes])


class NamespaceTransition(NamespaceNamed):

    @property
    def target_regime(self):
        return NamespaceRegime(self.sub_component, self.element.target_regime)

    @property
    def target_regime_name(self):
        return self.element.target_regime_name + self.suffix

    @property
    def state_assignments(self):
        return (NamespaceStateAssignment(self.sub_component, sa)
                for sa in self.element.state_assignments)

    @property
    def output_events(self):
        return (NamespaceOutputEvent(self.sub_component, oe)
                for oe in self.element.output_events)

    def state_assignment(self, name):
        return NamespaceStateAssignment(
            self.sub_component, self.element.state_assignment(name))

    def output_event(self, name):
        return NamespaceOutputEvent(
            self.sub_component, self.element.output_event(name))

    @property
    def num_state_assignments(self):
        return self.element.num_state_assignments

    @property
    def num_output_events(self):
        return self.element.num_output_events


class NamespaceTrigger(NamespaceExpression, Trigger):
    pass


class NamespaceOutputEvent(NamespaceNamed, OutputEvent):

    @property
    def port_name(self):
        return self.element.port_name


class NamespaceOnEvent(NamespaceTransition, OnEvent):

    @property
    def src_port_name(self):
        return self.element.src_port_name


class NamespaceOnCondition(NamespaceTransition, OnCondition):

    @property
    def trigger(self):
        return NamespaceTrigger(self, self.element.trigger)


class NamespaceStateVariable(NamespaceNamed, StateVariable):
    pass


class NamespaceAlias(NamespaceNamed, NamespaceExpression, Alias):
    pass


class NamespaceTimeDerivative(NamespaceNamed, NamespaceExpression,
                              TimeDerivative):

    @property
    def variable(self):
        return self.element.variable


class NamespaceStateAssignment(NamespaceNamed, NamespaceExpression,
                               StateAssignment):
    pass


class NamespaceProperty(NamespaceNamed, Property):
    pass


class LocalAnalogPortConnection(AnalogPortConnection, Alias):

    def __init__(self, sender_id, receiver_id,
                 send_port_name, receive_port_name):
        AnalogPortConnection.__init__(self, sender_id, receiver_id,
                                      send_port_name, receive_port_name)
        Alias.__init__(self, in_namespace(receive_port_name, receiver_id),
                       in_namespace(send_port_name, sender_id))


class LocalEventPortConnection(EventPortConnection):

    def __init__(self):
        raise NotImplementedError(
            "Local event port connections are not currently "
            "supported")


class BasePortExposure(BaseULObject):

    defining_attributes = ('_name', '_component', '_port')

    def __init__(self, name, component, port):
        super(BasePortExposure, self).__init__()
        self._name = name
        self._component = component
        self._port = port

    @property
    def name(self):
        return self._name

    @property
    def component(self):
        return self._component

    @property
    def port(self):
        return self._port

    @property
    def attributes_with_units(self):
        return chain(*[c.attributes_with_units for c in self.sub_component])

    @write_reference
    @annotate_xml
    def to_xml(self, document, **kwargs):  # @UnusedVariable
        return E(self.element_name,
                 name=self.name,
                 component=self.component,
                 port=self.port)

    @classmethod
    @resolve_reference
    @read_annotations
    def from_xml(cls, element, document, **kwargs):  # @UnusedVariable
        cls.check_tag(element)
        return cls(name=element.attrib['name'],
                   component=element.attrib['component'],
                   port=element.attrib['port'])


class AnalogSendPortExposure(BasePortExposure, AnalogSendPort):

    element_name = 'AnalogSendPortExposure'


class AnalogReceivePortExposure(BasePortExposure, AnalogReceivePort):

    element_name = 'AnalogReceivePortExposure'


class AnalogReducePortExposure(BasePortExposure, AnalogReducePort):

    element_name = 'AnalogReducePortExposure'


class EventSendPortExposure(BasePortExposure, EventSendPort):

    element_name = 'EventSendPortExposure'


class EventReceivePortExposure(BasePortExposure, EventReceivePort):

    element_name = 'EventReceivePortExposure'


def in_namespace(name, namespace):
    return name + '_' + namespace

# =============================================================================
# Code for Multi-compartment tree representations (Experimental)
# =============================================================================


class MultiCompartment(BaseULObject, DocumentLevelObject):
    """
    A collection of spiking neurons all of the same type.

    **Arguments**:
        *name*
            a name for the population.
        *size*
            an integer, the size of neurons in the population
        *cell*
            a :class:`Component`, or :class:`Reference` to a component defining
            the cell type (i.e. the mathematical model and its
            parameterisation).
        *positions*
            TODO: need to check if positions/structure are in the v1 spec
    """
    element_name = "MultiCompartment"
    defining_attributes = ('_name', '_tree', '_mapping', '_domains')

    def __init__(self, name, tree, mapping, domains, url=None):
        BaseULObject.__init__(self)
        DocumentLevelObject.__init__(self, url)
        assert isinstance(name, basestring)
        self._name = name
        self._domains = dict((d.name, d) for d in domains)
        assert isinstance(mapping, Mapping)
        self._mapping = mapping
        if isinstance(tree, Tree):
            self._tree = tree
        elif hasattr(tree, '__iter__'):
            self._tree = Tree(normalise_parameter_as_list(tree))

    @property
    def name(self):
        return self._name

    @property
    def mapping(self):
        return self._mapping

    @property
    def domains(self):
        return self._domains.itervalues()

    def domain(self, name_or_index):
        """
        Returns the domain corresponding to either the compartment index if
        provided an int or the domain name if provided a str
        """
        if isinstance(name_or_index, int):
            name = self.mapping.domain_name(name_or_index)
        elif isinstance(name_or_index, basestring):
            name = name_or_index
        else:
            raise NineMLRuntimeError(
                "Unrecognised type of 'name_or_index' ({}) can be either int "
                "or str".format(name_or_index))
        return self._domains[name]

    @property
    def domain_names(self):
        return self._domains.iterkeys()

    @property
    def tree(self):
        return self._tree.indices

    def __str__(self):
        return ("MultiCompartment(name='{}', {} compartments, {} domains)"
                .format(self.name, len(self.tree), len(self._domains)))

    @property
    def attributes_with_units(self):
        return chain(*[d.attributes_with_units for d in self.domains])

    @write_reference
    @annotate_xml
    def to_xml(self, document, **kwargs):  # @UnusedVariable
        return E(self.element_name,
                 self._tree.to_xml(document, **kwargs),
                 self._mapping.to_xml(document, **kwargs),
                 *[d.to_xml(document, **kwargs) for d in self.domains],
                 name=self.name)

    @classmethod
    @resolve_reference
    @read_annotations
    def from_xml(cls, element, document, **kwargs):
        cls.check_tag(element)
        tree = Tree.from_xml(
            expect_single(element.findall(NINEML + 'Tree')),
            document, **kwargs)
        mapping = Mapping.from_xml(
            expect_single(element.findall(NINEML + 'Mapping')),
            document, **kwargs)
        domains = [Domain.from_xml(e, document, **kwargs)
                   for e in element.findall(NINEML + 'Domain')]
        return cls(name=element.attrib['name'], tree=tree, mapping=mapping,
                   domains=domains)


class Tree(BaseULObject):

    element_name = "Tree"
    __metaclass__ = ABCMeta  # Abstract base class

    defining_attributes = ("_indices",)

    def __init__(self, indices):
        super(Tree, self).__init__()
        if any(not isinstance(i, int) for i in indices):
            raise NineMLRuntimeError(
                "Mapping keys need to be ints ({})"
                .format(', '.join(str(i) for i in indices)))
        self._indices = indices

    @property
    def indices(self):
        return self._indices

    @annotate_xml
    def to_xml(self, document, **kwargs):  # @UnusedVariable
        return E(self.element_name,
                 ArrayValue(self._indices).to_xml(document, **kwargs))

    @classmethod
    @read_annotations
    def from_xml(cls, element, document, **kwargs):
        array = ArrayValue.from_xml(
            expect_single(element.findall(NINEML + 'ArrayValue')),
            document, **kwargs)
        return cls(array.values)


class Mapping(BaseULObject):

    element_name = "Mapping"
    defining_attributes = ("_indices", '_keys')

    def __init__(self, keys, indices):
        super(Mapping, self).__init__()
        self._keys = keys
        if any(not isinstance(k, int) for k in keys.iterkeys()):
            raise NineMLRuntimeError(
                "Mapping keys need to be ints ({})"
                .format(', '.join(str(k) for k in keys.iterkeys())))
        if any(i not in keys.iterkeys() for i in indices):
            raise NineMLRuntimeError(
                "Some mapping indices ({}) are not present in key"
                .format(', '.join(set(str(i) for i in indices
                                      if i not in keys.iterkeys()))))
        self._indices = indices

    @property
    def keys(self):
        return self._keys

    @property
    def indices(self):
        return self._indices

    def domain_name(self, index):
        domain_index = self.indices[index]
        return self.keys[domain_index]

    @annotate_xml
    def to_xml(self, document, **kwargs):  # @UnusedVariable
        return E(self.element_name,
                 ArrayValue(self._indices).to_xml(document, **kwargs),
                 *[Key(i, n).to_xml(document, **kwargs)
                   for i, n in self.keys.iteritems()])

    @classmethod
    @read_annotations
    def from_xml(cls, element, document, **kwargs):
        array = ArrayValue.from_xml(
            expect_single(element.findall(NINEML + 'ArrayValue')),
            document, **kwargs)
        keys = [Key.from_xml(e, document, **kwargs)
                for e in element.findall(NINEML + 'Key')]
        return cls(dict((k.index, k.domain) for k in keys), array.values)


class Key(BaseULObject):

    element_name = 'Key'

    def __init__(self, index, domain):
        BaseULObject.__init__(self)
        self._index = index
        self._domain = domain

    @property
    def index(self):
        return self._index

    @property
    def domain(self):
        return self._domain

    @annotate_xml
    def to_xml(self, document, **kwargs):  # @UnusedVariable
        return E(self.element_name, index=str(self.index),
                 domain=self.domain)

    @classmethod
    @read_annotations
    def from_xml(cls, element, document, **kwargs):  # @UnusedVariable
        return cls(int(element.attrib['index']), element.attrib['domain'])


class Domain(SubDynamics):

    element_name = 'Domain'