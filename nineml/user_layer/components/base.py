# encoding: utf-8
from operator import and_
from itertools import chain
import nineml
from ..base import BaseULObject, E, NINEML
# This line is imported at the end of the file to avoid recursive imports
# from .interface import Property, InitialValue, InitialValueSet, PropertySet


class BaseComponent(BaseULObject):

    """
    Base class for model components that are defined in the abstraction layer.
    """
    element_name = "Component"
    defining_attributes = ("name")
    children = ("Property", "Definition", 'Prototype')

    # initial_values is temporary, the idea longer-term is to use a separate
    # library such as SEDML
    def __init__(self, name, definition, properties={}, initial_values={}):
        """
        Create a new component with the given name, definition and properties,
        or create a prototype to another component that will be resolved later.

        `name` - a name for the component that can be used to prototype it.
        `definition` - a Definition instance, the URL of a component
                       definition, or None if creating a prototype.
        `properties` - a PropertySet instance or a dictionary containing
                       (value,unit) pairs.
        `prototype` - the name of another component in the model, or None.
        """
        self.name = name
        if not (isinstance(definition, Definition) or
                isinstance(definition, Prototype)):
            raise ValueError("'definition' must be either a 'Definition' or "
                             "'Prototype' element")
        self._definition = definition
        if isinstance(properties, PropertySet):
            self._properties = properties
        elif isinstance(properties, dict):
            self._properties = PropertySet(**properties)
        else:
            raise TypeError("properties must be a PropertySet or a dict")
        if isinstance(initial_values, InitialValueSet):
            self.initial_values = initial_values
        elif isinstance(initial_values, dict):
            self.initial_values = InitialValueSet(**initial_values)
        else:
            raise TypeError("initial_values must be an InitialValueSet or a "
                            "dict, not a %s" % type(initial_values))
        self.check_properties()
        try:
            self.check_initial_values()
        except AttributeError:  # 'check_initial_values' is only in dynamics
            pass

    @property
    def component_class(self):
        """
        Returns the component class from the definition object or the
        prototype's definition, or the prototype's prototype's definition, etc.
        depending on how the component is defined.
        """
        defn = self._definition
        while not isinstance(defn, Definition):
            defn = defn._definition
        return defn.component_class

    @property
    def properties(self):
        """
        Recursively retrieves properties defined in prototypes and updates them
        with properties defined locally
        """
        props = PropertySet()
        if isinstance(self._definition, Prototype):
            props.update(self._definition.properties)
        props.update(self._properties)
        return props

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        assert not (self.unresolved or other.unresolved)
        return reduce(and_, (self.name == other.name,
                             self.component_class == other.component_class,
                             self.properties == other.properties))

    def __hash__(self):
        assert not self.unresolved
        return (hash(self.__class__) ^ hash(self.name) ^
                hash(self.component_class) ^ hash(self.properties))

    def __repr__(self):
        return ('%s(name="%s", componentclass="%s")' %
                (self.__class__.__name__, self.name,
                 self.component_class.name))

    def diff(self, other):
        d = []
        if self.name != other.name:
            d += ["name: %s != %s" % (self.name, other.name)]
        if self.definition != other.definition:
            d += ["definition: %s != %s" % (self.definition, other.definition)]
        if self.properties != other.properties:
            d += ["properties: %s != %s" % (self.properties, other.properties)]
        return "\n".join(d)

    def get_definition(self):
        if not self.definition.component:
            self.definition.retrieve()
        return self.definition.component

    def check_properties(self):
        # First check the names
        properties = set(self.properties.iterkeys())
        parameters = set(p.name
                         for p in self.definition.component_class.parameters)
        msg = []
        diff_a = properties.difference(parameters)
        diff_b = parameters.difference(properties)
        if diff_a:
            msg.append("User properties contains the following parameters "
                       "that are not present in the definition: %s" %
                       ",".join(diff_a))
        if diff_b:
            msg.append("Definition contains the following parameters that are "
                       "not present in the user properties: %s" %
                       ",".join(diff_b))
        if msg:
            # need a more specific type of Exception
            raise Exception(". ".join(msg))
        # TODO: Now check dimensions

    def _to_xml(self):
        properties_and_initial_values = (self.properties.to_xml() +
                                         [iv.to_xml()
                                          for iv in
                                                 self.initial_values.values()])
        element = E(self.element_name,
                    self._definition.to_xml(),
                    *properties_and_initial_values,
                    name=self.name)
        return element

    @classmethod
    def from_xml(cls, element, context):
        if element.tag != NINEML + cls.element_name:
            raise Exception("Expecting tag name %s%s, actual tag name %s" % (
                NINEML, cls.element_name, element.tag))
        name = element.attrib.get("name", None)
        properties = PropertySet.from_xml(
                               element.findall(NINEML + Property.element_name),
                               context)
        initial_values = InitialValueSet.from_xml(
                           element.findall(NINEML + InitialValue.element_name),
                           context)
        definition_element = element.find(NINEML + Definition.element_name)
        if definition_element:
            definition = Definition.from_xml(definition_element, context)
        else:
            prototype_element = element.find(NINEML + "Prototype")
            if not prototype_element:
                raise Exception("A component must contain either a defintion "
                                "or a prototype")
            definition = Prototype.from_xml(element, context)
        return cls(name, definition, properties,
                       initial_values=initial_values)


class BaseReference(BaseULObject):

    """
    Base class for model components that are defined in the abstraction layer.
    """

    # initial_values is temporary, the idea longer-term is to use a separate
    # library such as SEDML
    def __init__(self, name, context, url=None):
        """
        Create a new component with the given name, definition and properties,
        or create a prototype to another component that will be resolved later.

        `name` - a name of an existing component to refer to
        `url`            - a url of the file containing the exiting component
        """
        self.url = url
        if self.url:
            context = nineml.read(url)
        self._referred_to = context[name]

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return reduce(and_, (self.component_name == other.component_name,
                             self.url == other.url))

    def __hash__(self):
        assert not self.unresolved
        return (hash(self.__class__) ^ hash(self.component_name) ^
                hash(self.url))

    def __repr__(self):
            return ('{}(refers_to="{}"{})'
                    .format(self.__class__.__name__, self.component_name,
                            ' in "{}"'.format(self.url) if self.url else ''))

    def to_xml(self):
        kwargs = {'url': self.url} if self.url else {}
        element = E(self.element_name,
                    self.component_name,
                    **kwargs)
        return element

    @classmethod
    def from_xml(cls, element, context):
        if element.tag != NINEML + cls.element_name:
            raise Exception("Expecting tag name %s%s, actual tag name %s" % (
                NINEML, cls.element_name, element.tag))
        name = element.text
        url = element.attrib.get("url", None)
        return cls(name, context, url)


class Reference(BaseReference):

    """
    Base class for model components that are defined in the abstraction layer.
    """
    element_name = "Reference"

    # initial_values is temporary, the idea longer-term is to use a separate
    # library such as SEDML
    def __init__(self, name, context, url=None):
        """
        Create a new component with the given name, definition and properties,
        or create a prototype to another component that will be resolved later.

        `name`    -- a name of an existing component to refer to
        `context` -- a nineml.context.Context object containing the top-level
                     objects in the current file
        `url`     -- a url of the file containing the exiting component
        """
        super(Reference, self).__init__(name, context, url)
        self._referred_to.set_reference(self)

    @property
    def user_layer_object(self):
        return self._referred_to


class Definition(BaseReference):

    """
    Base class for model components that are defined in the abstraction layer.
    """
    element_name = "Definition"

    @property
    def component_class(self):
        return self._referred_to


class Prototype(BaseReference):

    element_name = "Prototype"

    @property
    def component(self):
        return self._referred_to


# class Definition(BaseULObject):
# 
#     """
#     Encapsulate a component definition.
# 
#     For now, this holds only the URI of an abstraction layer file, but this
#     could be expanded later to include definitions external to 9ML.
#     """
#     element_name = "Definition"
#     defining_attributes = ("url",)
# 
#     def __init__(self, component_class_name, context=Context(), url=None):
#         def_context = context
#         if url:
#             def_context = nineml.read(url)
#         self.component_class = def_context[component_class_name]
#         self.url = url
# 
#     def __hash__(self):
#         if self._component:
#             return hash(self._component)
#         else:
#             return hash(self.url)
# 
#     @property
#     def component(self):
#         return self.retrieve()
# 
#     def retrieve(self):
#         reader = getattr(abstraction_layer,
#                          self.abstraction_layer_module).readers.XMLReader
#         if self.abstraction_layer_module == "random":  # hack
#             self._component = reader.read_component(self.url)
#         else:
#             f = urllib.urlopen(self.url)
#             try:
#                 component_class = reader.read_component(self.url)
#             finally:
#                 f.close()
#         return component_class
# 
#     def to_xml(self):
#         if hasattr(self, "url") and self.url:
#             return E(self.element_name, (E.link(self.url)), language="NineML")
#         else:  # inline
#             al_writer = getattr(abstraction_layer,
#                                 self.abstraction_layer_module).\
#                                                             writers.XMLWriter()
#             return E(self.element_name,
#                      al_writer.visit(self._component),
#                      language="NineML")
# 
#     @classmethod
#     def from_xml(cls, element, context):
#         url = element.attrib.get('url', None)
#         component_class_name = element.text
#         return cls(component_class_name, context, url=url)


# def get_or_create_component(ref, cls, components):
#     """
#     Each entry in `components` is either an instance of a BaseComponent
#     subclass, or the XML (elementtree Element) defining such an instance.
# 
#     If given component does not exist, we create it and replace the XML in
#     `components` with the actual component. We then return the component.
#     """
#     assert ref in components, "%s not in %s" % (ref, components.keys())
#     if not isinstance(components[ref], BaseComponent):
#         components[ref] = cls.from_xml(components[ref], components)
#     return components[ref]

# This is imported at the end to avoid recursive imports
from .interface import Property, InitialValue, InitialValueSet, PropertySet
