"""
A module containing wrappers for abstraction layer elements that
append the namespace of a sub component to every identifier to avoid
name clashes in the global scope
"""
import re
import sympy
from ..component import Property
from nineml.abstraction import (
    Alias, TimeDerivative, Regime, OnEvent, OnCondition, StateAssignment,
    Trigger, OutputEvent, StateVariable, Constant, Parameter)
from nineml.exceptions import NineMLImmutableError


# Matches multiple underscores, so they can be escaped by appending another
# underscore (double underscores are used to delimit namespaces).
multiple_underscore_re = re.compile(r'(.*)(__+)()')
# Match only double underscores (no more or less)
double_underscore_re = re.compile(r'(?<!_)__(?!_)')
# Match more than double underscores to reverse escaping of double underscores
# in sub-component suffixes by adding an additional underscore.
more_than_double_underscore_re = re.compile(r'(__)_+')


def append_namespace(identifier, namespace):
    """
    Appends a namespace to an identifier in such a way that it avoids name
    clashes and the two parts can be split again using 'split_namespace'
    """
    # Since double underscores are used to delimit namespaces from names
    # within the namesapace (and 9ML names are not allowed to start or end
    # in underscores) we append an underscore to each multiple underscore
    # to avoid clash with the delimeter in the suffix
    return (identifier + '__' +
            multiple_underscore_re.sub(r'/1/2_/3', namespace))


def split_namespace(cls, identifier_in_namespace):
    """
    Splits an identifer and a namespace that have been concatenated by
    'append_namespace'
    """
    parts = double_underscore_re.split(identifier_in_namespace)
    name = '__'.join(parts[:-1])
    comp_name = parts[-1]
    comp_name = more_than_double_underscore_re.sub('_', comp_name)
    return name, comp_name


def make_delay_trigger_name(port_conn):
    """
    Creates a name for a delay trigger statevariable from a given event port
    connection object
    """
    parts = (
        (port_conn.sender_role
         if port_conn.sender_role is not None else port_conn.sender_name),
        port_conn.send_port_name,
        (port_conn.receiver_role
         if port_conn.receiver_role is not None else port_conn.receiver_name),
        port_conn.receive_port_name)
    return ('_'.join(multiple_underscore_re.sub(r'/1/2_/3', p) for p in parts)
            + '_delay_trigger')


def make_regime_name(self, sub_regimes_dict):
    sorted_keys = sorted(sub_regimes_dict.iterkeys())
    return '_'.join(multiple_underscore_re.sub(r'/1/2_/3', sub_regimes_dict[k])
                    for k in sorted_keys) + '_regime'


class _NamespaceNamed(object):
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
        return self.sub_component.append_namespace(self._element.name)


class _NamespaceExpression(object):

    def __init__(self, sub_component, element):
        self._sub_component = sub_component
        self._element = element

    @property
    def sub_component(self):
        return self._sub_component

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
                (s, sympy.Symbol(self.sub_component.append_namespace(s)))
                for s in self.rhs_symbols))
        except AttributeError:  # If rhs has been simplified to ints/floats
            assert float(self.element.rhs)
            return self.rhs

    @rhs.setter
    def rhs(self, rhs):
        raise NineMLImmutableError(
            "Cannot change expression in global namespace of "
            "multi-component element. The multi-component elemnt should either"
            " be flattened or the substitution should be done in the "
            "sub-component")

    def rhs_name_transform_inplace(self, name_map):
        raise NineMLImmutableError(
            "Cannot change expression in global namespace of "
            "multi-component element. The multi-component elemnt should either"
            " be flattened or the substitution should be done in the "
            "sub-component")

    def rhs_substituted(self, name_map):
        raise NineMLImmutableError(
            "Cannot change expression in global namespace of "
            "multi-component element. The multi-component elemnt should either"
            " be flattened or the substitution should be done in the "
            "sub-component")

    def subs(self, old, new):
        raise NineMLImmutableError(
            "Cannot change expression in global namespace of "
            "multi-component element. The multi-component elemnt should either"
            " be flattened or the substitution should be done in the "
            "sub-component")

    def rhs_str_substituted(self, name_map={}, funcname_map={}):
        raise NineMLImmutableError(
            "Cannot change expression in global namespace of "
            "multi-component element. The multi-component elemnt should either"
            " be flattened or the substitution should be done in the "
            "sub-component")


class _NamespaceTransition(_NamespaceNamed):

    @property
    def target_regime(self):
        return _NamespaceRegime(self.sub_component, self.element.target_regime)

    @property
    def target_regime_name(self):
        return self.element.target_regime_name + self.suffix

    @property
    def state_assignments(self):
        return (_NamespaceStateAssignment(self.sub_component, sa)
                for sa in self.element.state_assignments)

    @property
    def output_events(self):
        return (_NamespaceOutputEvent(self.sub_component, oe)
                for oe in self.element.output_events)

    def state_assignment(self, name):
        return _NamespaceStateAssignment(
            self.sub_component, self.element.state_assignment(name))

    def output_event(self, name):
        return _NamespaceOutputEvent(
            self.sub_component, self.element.output_event(name))

    @property
    def num_state_assignments(self):
        return self.element.num_state_assignments

    @property
    def num_output_events(self):
        return self.element.num_output_events


class _NamespaceOnEvent(_NamespaceTransition, OnEvent):

    @property
    def src_port_name(self):
        return self.element.src_port_name


class _NamespaceOnCondition(_NamespaceTransition, OnCondition):

    @property
    def trigger(self):
        return _NamespaceTrigger(self, self.element.trigger)


class _NamespaceTrigger(_NamespaceExpression, Trigger):
    pass


class _NamespaceOutputEvent(_NamespaceNamed, OutputEvent):

    @property
    def port_name(self):
        return self.element.port_name


class _NamespaceStateVariable(_NamespaceNamed, StateVariable):
    pass


class _NamespaceAlias(_NamespaceNamed, _NamespaceExpression, Alias):
    pass


class _NamespaceParameter(_NamespaceNamed, Parameter):
    pass


class _NamespaceConstant(_NamespaceNamed, Constant):
    pass


class _NamespaceTimeDerivative(_NamespaceNamed, _NamespaceExpression,
                               TimeDerivative):

    @property
    def variable(self):
        return self.element.variable


class _NamespaceStateAssignment(_NamespaceNamed, _NamespaceExpression,
                                StateAssignment):
    pass


class _NamespaceProperty(_NamespaceNamed, Property):
    pass


class _NamespaceRegime(_NamespaceNamed, Regime):

    @property
    def time_derivatives(self):
        return (_NamespaceTimeDerivative(self.sub_component, td)
                for td in self.element.time_derivatives)

    @property
    def aliases(self):
        return (_NamespaceAlias(self.sub_component, a)
                for a in self.element.aliases)

    @property
    def on_events(self):
        return (_NamespaceOnEvent(self.sub_component, oe)
                for oe in self.element.on_events)

    @property
    def on_conditions(self):
        return (_NamespaceOnEvent(self.sub_component, oc)
                for oc in self.element.on_conditions)

    def time_derivative(self, name):
        return _NamespaceTimeDerivative(self.sub_component,
                                        self.element.time_derivative(name))

    def alias(self, name):
        return _NamespaceAlias(self.sub_component, self.element.alias(name))

    def on_event(self, name):
        return _NamespaceOnEvent(self.sub_component,
                                 self.element.on_event(name))

    def on_condition(self, name):
        return _NamespaceOnEvent(self.sub_component,
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
