from itertools import chain
from . import BaseULObject
from abc import ABCMeta
from nineml.reference import resolve_reference, write_reference
from nineml import DocumentLevelObject
from nineml.xmlns import NINEML, E
from nineml.utils import expect_single, normalise_parameter_as_list
from nineml.user import DynamicsProperties
from nineml.annotations import annotate_xml, read_annotations
from .values import ArrayValue
from nineml.exceptions import NineMLRuntimeError
from .port_connections import PortConnection, Sender


class MultiComponent(BaseULObject, DocumentLevelObject):

    element_name = "MultiComponent"
    defining_attributes = ('_name', '_subcomponents', '_port_exposures')

    def __init__(self, name, subcomponents, port_exposures=()):
        super(MultiComponent, self).__init__()
        self._name = name
        self._subcomponents = dict((c.name, c) for c in subcomponents)
        self._port_exposures = dict((pe.name, pe) for pe in port_exposures)

    @property
    def name(self):
        return self._name

    @property
    def subcomponents(self):
        return self._subcomponents.itervalues()

    @property
    def port_exposures(self):
        return self._port_exposures.itervalues()

    def subcomponent(self, name):
        return self._subcomponents[name]

    def port_exposure(self, name):
        return self._port_exposures[name]

    @property
    def subcomponent_names(self):
        return self._subcomponents.iterkeys()

    @property
    def port_exposure_names(self):
        return self._port_exposures.iterkeys()

    @property
    def attributes_with_units(self):
        return chain(*[c.attributes_with_units for c in self.subcomponents])

    @write_reference
    @annotate_xml
    def to_xml(self, document, **kwargs):
        return E(self.element_name,
                 *list(chain((c.to_xml(document, **kwargs)
                              for c in self.subcomponents),
                             (pe.to_xml(document, **kwargs)
                              for pe in self.port_exposures))),
                 name=self.name)

    @classmethod
    @resolve_reference
    @read_annotations
    def from_xml(cls, element, document):
        cls.check_tag(element)
        subcomponents = [SubComponent.from_xml(e, document)
                         for e in element.findall(NINEML + 'SubComponent')]
        port_exposures = [PortExposure.from_xml(e, document)
                          for e in element.findall(NINEML + 'PortExposure')]
        return cls(name=element.attrib['name'],
                   subcomponents=subcomponents, port_exposures=port_exposures)


class PortExposure(BaseULObject):

    element_name = 'PortExposure'
    defining_attributes = ('_name', '_component', '_port')

    def __init__(self, name, component, port):
        super(PortExposure, self).__init__()
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
        return chain(*[c.attributes_with_units for c in self.subcomponents])

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
    def from_xml(cls, element, document):  # @UnusedVariable
        cls.check_tag(element)
        return cls(name=element.attrib['name'],
                   component=element.attrib['component'],
                   port=element.attrib['port'])


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
    def from_xml(cls, element, document):
        cls.check_tag(element)
        tree = Tree.from_xml(
            expect_single(element.findall(NINEML + 'Tree')), document)
        mapping = Mapping.from_xml(
            expect_single(element.findall(NINEML + 'Mapping')), document)
        domains = [Domain.from_xml(e, document)
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
    def from_xml(cls, element, document):
        array = ArrayValue.from_xml(
            expect_single(element.findall(NINEML + 'ArrayValue')), document)
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
    def from_xml(cls, element, document):
        array = ArrayValue.from_xml(
            expect_single(element.findall(NINEML + 'ArrayValue')), document)
        keys = [Key.from_xml(e, document)
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
    def from_xml(cls, element, document):  # @UnusedVariable
        return cls(int(element.attrib['index']), element.attrib['domain'])


class SubComponent(BaseULObject):

    element_name = 'SubComponent'
    defining_attributes = ('_name', '_dynamics', '_port_connections')

    def __init__(self, name, dynamics, port_connections=()):
        BaseULObject.__init__(self)
        self._name = name
        self._dynamics = dynamics
        self._port_connections = port_connections

    @property
    def name(self):
        return self._name

    @property
    def dynamics(self):
        return self._dynamics

    @property
    def port_connections(self):
        return self._port_connections

    @property
    def attributes_with_units(self):
        return self._dynamics.attributes_with_units

    @annotate_xml
    def to_xml(self, document, **kwargs):  # @UnusedVariable
        return E(self.element_name, self._dynamics.to_xml(document, **kwargs),
                 *[pc.to_xml(document, **kwargs)
                   for pc in self._port_connections],
                 name=self.name)

    @classmethod
    @read_annotations
    def from_xml(cls, element, document):
        try:
            dynamics = DynamicsProperties.from_xml(expect_single(
                element.findall(NINEML + 'DynamicsProperties')), document)
        except NineMLRuntimeError:
            dynamics = MultiComponent.from_xml(expect_single(
                element.findall(NINEML + 'MultiComponent')), document)
        port_connections = [
            PortConnection.from_xml(e, document)
            for e in element.findall(NINEML + 'PortConnection')]
        return cls(element.attrib['name'], dynamics, port_connections)


class Domain(SubComponent):

    element_name = 'Domain'


class FromSibling(Sender):

    element_name = 'FromSibling'

    def __init__(self, component, port):
        super(FromSibling, self).__init__(port)
        self.component = component

    def key(self):
        """
        Generates a unique key for the Sender so it can be stored in a dict
        """
        return (self.element_name, self.component, self._port_name)

    @annotate_xml
    def to_xml(self, document, **kwargs):  # @UnusedVariable
        return E(self.element_name, component=self.component,
                 port=self.port_name)

    @classmethod
    @read_annotations
    def _from_xml(cls, element, document):  # @UnusedVariable
        cls.check_tag(element)
        return cls(component=element.attrib['component'],
                   port=element.attrib['port'])


class MultiCompartmentSender(Sender):

    def __init__(self, port, domain=None):
        super(MultiCompartmentSender, self).__init__(port)
        self.domain = domain

    def key(self):
        """
        Generates a unique key for the Sender so it can be stored in a dict
        """
        return (self.element_name, self.domain, self._port_name)

    @annotate_xml
    def to_xml(self, document, **kwargs):  # @UnusedVariable
        kwargs = {'port': self.port_name}
        if self.domain:
            kwargs['domain'] = str(self.domain)
        return E(self.element_name, **kwargs)

    @classmethod
    @read_annotations
    def _from_xml(cls, element, document):  # @UnusedVariable
        cls.check_tag(element)
        return cls(domain=element.get('domain', None),
                   port=element.attrib['port'])


class FromProximal(MultiCompartmentSender):

    element_name = 'FromProximal'


class FromDistal(MultiCompartmentSender):

    element_name = 'FromDistal'
