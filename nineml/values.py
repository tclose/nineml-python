# encoding: utf-8
from . import BaseNineMLObject
from nineml.xmlns import E, NINEML
from abc import ABCMeta, abstractmethod
from nineml.annotations import read_annotations, annotate_xml
from urllib import urlopen
import contextlib
import collections
import sympy
import itertools
from operator import itemgetter
from nineml.reference import Reference
import numpy
from nineml.exceptions import (
    NineMLRuntimeError, NineMLMissingElementError, NineMLDimensionError)
from nineml.utils import expect_single, expect_none_or_single
from nineml.user.component import RandomDistributionProperties
from nineml.units import unitless, Unit


class BaseValue(BaseNineMLObject):

    __metaclass__ = ABCMeta

    @abstractmethod
    def to_xml(self, document, **kwargs):
        pass

    @classmethod
    @read_annotations
    def from_parent_xml(cls, element, document, **kwargs):  # @UnusedVariable
        if element.find(NINEML + 'SingleValue') is not None:
            value = SingleValue.from_xml(
                expect_single(element.findall(NINEML + 'SingleValue')),
                document)
        elif element.find(NINEML + 'ArrayValue') is not None:
            value = ArrayValue.from_xml(
                expect_single(element.findall(NINEML + 'ArrayValue')),
                document)
        elif element.find(NINEML + 'ExternalArrayValue') is not None:
            value = ArrayValue.from_xml(
                expect_single(element.findall(NINEML + 'ExternalArrayValue')),
                document)
        elif element.find(NINEML + 'RandomDistributionValue') is not None:
            value = RandomDistributionValue.from_xml(
                expect_single(
                    element.findall(NINEML + 'RandomDistributionValue')),
                document)
        else:
            raise NineMLRuntimeError(
                "Did not find recognised value tag in property (found {})"
                .format(', '.join(c.tag for c in element.getchildren())))
        return value


class SingleValue(BaseValue):

    """
    Representation of a numerical- or string-valued parameter.

    A numerical parameter is a (name, value, units) triplet, a string parameter
    is a (name, value) pair.

    Numerical values may either be numbers, or a component that generates
    numbers, e.g. a RandomDistribution instance.
    """
    element_name = "SingleValue"
    defining_attributes = ("value",)

    def __init__(self, value):
        super(SingleValue, self).__init__()
        self._value = float(value)

    @property
    def value(self):
        return self._value

    def __iter__(self):
        """Infinitely iterate the same value"""
        return itertools.repeat(self._value)

    def __len__(self):
        return 0

    def __str__(self):
        return str(self._value)

    def __repr__(self):
        return "SingleValue(value={})".format(self.value)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.value == other.value

    def __hash__(self):
        return hash(self.value)

    @annotate_xml
    def to_xml(self, document, **kwargs):  # @UnusedVariable
        return E(self.element_name, str(self.value))

    @classmethod
    @read_annotations
    def from_xml(cls, element, document):  # @UnusedVariable
        cls.check_tag(element)
        return cls(float(element.text))

    # =========================================================================
    # Magic methods to allow the SingleValue to be treated like a
    # floating point number
    # =========================================================================

    def _sympy_(self):
        return self._value

    def __float__(self):
        return self._value

    def __int__(self):
        return self._value

    def __add__(self, num):
        return self._value + num

    def __sub__(self, num):
        return self._value - num

    def __mul__(self, num):
        return self._value * num

    def __truediv__(self, num):
        return self._value / num

    def __div__(self, num):
        return self.__truediv__(num)

    def __divmod__(self, num):
        return divmod(self, num)

    def __pow__(self, power):
        return self._value ** power

    def __floordiv__(self, num):
        return self._value // num

    def __mod__(self, num):
        return self._value % num

    def __radd__(self, num):
        return self.__add__(num)

    def __rsub__(self, num):
        return num - self._value

    def __rmul__(self, num):
        return self.__mul__(num)

    def __rtruediv__(self, num):
        return num.__truediv__(self._value)

    def __rdiv__(self, num):
        return self.__rtruediv__(num)

    def __rdivmod__(self, num):
        return divmod(num, self)

    def __rpow__(self, num):
        return num ** self._value

    def __rfloordiv__(self, num):
        return num // self._value

    def __rmod__(self, num):
        return num % self._value

    def __neg__(self):
        return -self._value

    def __abs__(self):
        return abs(self._value)

    def __round__(self, num_digits=0):
        return round(self._value, num_digits)

    def __floor__(self):
        return self._value.__floor__()

    def __ceil__(self):
        return self._value.__ceil__()


class ArrayValue(BaseValue):

    element_name = "ArrayValue"
    defining_attributes = ("_values",)
    DataFile = collections.namedtuple('DataFile', 'url mimetype, columnName')

    def __init__(self, values, datafile=None):
        super(ArrayValue, self).__init__()
        try:
            iter(values)
        except TypeError:
            raise NineMLRuntimeError(
                "'values' argument provided to ArrayValue is not iterable")
        self._values = values
        if datafile is None:
            self._datafile = None
        else:
            self._datafile = self.DataFile(*datafile)

    @property
    def values(self):
        return iter(self._values)

    def __iter__(self):
        return iter(self._values)

    def __getitem__(self, index):
        return self._values[index]

    def __len__(self):
        return len(self._values)

    def __repr__(self):
        return "ArrayValue(with {} values)".format(len(self._values))

    def __hash__(self):
        return hash(self.value)

    @annotate_xml
    def to_xml(self, document, **kwargs):  # @UnusedVariable
        if self._datafile is None:
            return E.ArrayValue(
                *[E.ArrayValueRow(index=i, value=v).to_xml()
                  for i, v in enumerate(self._values)])
        else:
            raise NotImplementedError(
                "TODO: Need to implement code to save data to external file")
            return E.ExternalArrayValue(
                url=self.url, mimetype=self.mimetype,
                columnName=self.columnName)

    @classmethod
    @read_annotations
    def from_xml(cls, element, document, **kwargs):  # @UnusedVariable
        if element.tag == 'ExternalArrayValue':
            url = element.attrib["url"]
            with contextlib.closing(urlopen(url)) as f:
                # FIXME: Should use a non-numpy version of this load function
                values = numpy.loadtxt(f)
            return cls(values, (element.attrib["url"],
                                element.attrib["mimetype"],
                                element.attrib["columnName"]))
        else:
            rows = [(int(e.attrib['index']), float(e.attrib['value']))
                    for e in element.findall(NINEML + 'ArrayValueRow')]
            sorted_rows = sorted(rows, key=itemgetter(0))
            indices, values = zip(*sorted_rows)
            if indices[0] < 0:
                raise NineMLRuntimeError(
                    "Negative indices found in array rows")
            if len(list(itertools.groupby(indices))) != len(indices):
                groups = [list(g) for g in itertools.groupby(indices)]
                raise NineMLRuntimeError(
                    "Duplicate indices ({}) found in array rows".format(
                        ', '.join(str(g[0]) for g in groups if len(g) > 1)))
            if indices[-1] >= len(indices):
                raise NineMLRuntimeError(
                    "Indices greater or equal to the number of array rows")
            return cls(values)

    # =========================================================================
    # Magic methods to allow the SingleValue to be treated like a
    # floating point number
    # =========================================================================

    def _sympy_(self):
        return sympy.Matrix(self._value)

    def __add__(self, num):
        try:
            return self._value + num
        except AttributeError:
            return [self._value + v for v in self._values]

    def __sub__(self, num):
        try:
            return self._value - num
        except AttributeError:
            return [self._value - v for v in self._values]

    def __mul__(self, num):
        try:
            return self._value * num
        except AttributeError:
            return [self._value * v for v in self._values]

    def __truediv__(self, num):
        try:
            return self._value.__truediv__(num)
        except AttributeError:
            return [self._value / v for v in self._values]

    def __div__(self, num):
        try:
            return self.__truediv__(num)
        except AttributeError:
            return [self.__truediv__(v) for v in self._values]

    def __divmod__(self, num):
        try:
            return divmod(self, num)
        except AttributeError:
            return [divmod(self, v) for v in self._values]

    def __pow__(self, power):
        try:
            return self._value ** power
        except AttributeError:
            return [self._value ** v for v in self._values]

    def __floordiv__(self, num):
        try:
            return self._value // num
        except AttributeError:
            return [self._value // v for v in self._values]

    def __mod__(self, num):
        try:
            return self._value % num
        except AttributeError:
            return [self._value % v for v in self._values]

    def __radd__(self, num):
        try:
            return self.__add__(num)
        except AttributeError:
            return [self.__add__(v) for v in self._values]

    def __rsub__(self, num):
        try:
            return num - self._value
        except AttributeError:
            return [num - v for v in self._values]

    def __rmul__(self, num):
        try:
            return num * self._value
        except AttributeError:
            return [num * v for v in self._values]

    def __rtruediv__(self, num):
        try:
            return num.__truediv__(self._value)
        except AttributeError:
            return [num.__truediv__(v) for v in self._values]

    def __rdiv__(self, num):
        try:
            return self.__rtruediv__(num)
        except AttributeError:
            return [self.__rtruediv__(v) for v in self._values]

    def __rdivmod__(self, num):
        try:
            return divmod(num, self)
        except AttributeError:
            return [divmod(v, self) for v in self._values]

    def __rpow__(self, num):
        try:
            return self._values.__rpow__(num)
        except AttributeError:
            return [num ** v for v in self._values]

    def __rfloordiv__(self, num):
        try:
            return self._values.__rfloordiv__()
        except AttributeError:
            return [num // v for v in self._values]

    def __rmod__(self, num):
        try:
            return self._values.__rmod__()
        except AttributeError:
            return [num % v for v in self._values]

    def __neg__(self):
        try:
            return self._values.__neg__()
        except AttributeError:
            return [-v for v in self._values]

    def __abs__(self):
        try:
            return self._values.__abs__()
        except AttributeError:
            return [abs(v) for v in self._values]


class RandomDistributionValue(BaseValue):

    element_name = "RandomDistributionValue"
    defining_attributes = ("_port_name", "distribution")

    def __init__(self, distribution, port_name):
        self._distribution = distribution
        self._port_name = port_name
        self._generator = None

    @property
    def port(self):
        return self._distribution.port(self._port_name)

    @property
    def distribution(self):
        return self._distribution

    def __len__(self):
        return 0

    def __iter__(self):
        if self._generator is None:
            raise NineMLRuntimeError(
                "Generator not set for RandomDistributionValue '{}'"
                .format(self))
        yield self._generator()

    def set_generator(self, generator_cls):
        """
        Generator class can be supplied by the implementing package to allow
        the value to be iterated over in the same manner as the other value
        types
        """
        self._generator = generator_cls(self.distribution)

    def __repr__(self):
        return ("RandomDistributionValue({} port of {} component)"
                .format(self.port_name, self.distribution.name))

    @annotate_xml
    def to_xml(self, document, **kwargs):  # @UnusedVariable
        return E(self.element_name,
                 self.distribution.to_xml(document, **kwargs),
                 port=self.port.name)

    @classmethod
    @read_annotations
    def from_xml(cls, element, document, **kwargs):  # @UnusedVariable
        rd_elem = expect_none_or_single(
            element.findall(NINEML + 'RandomDistributionProperties'))
        if rd_elem is None:
            distribution = Reference.from_xml(
                expect_single(element.findall(NINEML +
                                              'Reference'))).user_object
        else:
            distribution = RandomDistributionProperties.from_xml(
                rd_elem, document)
        return cls(distribution, port_name=element.attrib["port"])


class Quantity(BaseNineMLObject):

    """
    Representation of a numerical- or string-valued parameter.

    A numerical parameter is a (name, value, units) triplet, a string parameter
    is a (name, value) pair.

    Numerical values may either be numbers, or a component_class that generates
    numbers, e.g. a RandomDistribution instance.
    """
    element_name = 'Quantity'

    defining_attributes = ("value", "units")

    def __init__(self, value, units=None):
        super(Quantity, self).__init__()
        if not isinstance(value, (SingleValue, ArrayValue,
                                  RandomDistributionValue)):
            try:
                # Convert value from float
                value = SingleValue(float(value))
            except TypeError:
                # Convert value from iterable
                value = ArrayValue(value)
        if units is None:
            units = unitless
        if not isinstance(units, Unit):
            raise Exception("Units ({}) must of type <Unit>".format(units))
        if isinstance(value, (int, float)):
            value = SingleValue(value)
        self._value = value
        self.units = units

    def __hash__(self):
        if self.is_single():
            hsh = hash(self.value) ^ hash(self.units)
        else:
            hsh = hash(self.units)
        return hsh

    def __iter__(self):
        """For conveniently expanding quantities like a tuple"""
        return (self.value, self.units)

    @property
    def value(self):
        return self._value

    def __getitem__(self, index):
        if self.is_array():
            return self._value.values[index]
        elif self.is_single():
            return self._value.value
        else:
            raise NineMLRuntimeError(
                "Cannot get item from random distribution")

    def set_units(self, units):
        if units.dimension != self.units.dimension:
            raise NineMLRuntimeError(
                "Can't change dimension of quantity from '{}' to '{}'"
                .format(self.units.dimension, units.dimension))
        self.units = units

    def __repr__(self):
        units = self.units.name
        if u"µ" in units:
            units = units.replace(u"µ", "u")
        return ("{}(value={}, units={})"
                .format(self.element_name, self.value, units))

    @annotate_xml
    def to_xml(self, **kwargs):  # @UnusedVariable
        return E(self.element_name,
                 self._value.to_xml(),
                 units=self.units.name)

    @classmethod
    @read_annotations
    def from_xml(cls, element, document, **kwargs):  # @UnusedVariable
        value = BaseValue.from_parent_xml(
            expect_single(element.findall(NINEML, document, **kwargs)))
        try:
            units_str = element.attrib['units']
        except KeyError:
            raise NineMLRuntimeError(
                "{} element '{}' is missing 'units' attribute (found '{}')"
                .format(element.tag, element.get('name', ''),
                        "', '".join(element.attrib.iterkeys())))
        try:
            units = document[units_str]
        except KeyError:
            raise NineMLMissingElementError(
                "Did not find definition of '{}' units in the current "
                "document.".format(units_str))
        return cls(value=value, units=units)

    def __add__(self, qty):
        return Quantity(self.value + self._scaled_value(qty), self.units)

    def __sub__(self, qty):
        return Quantity(self.value - self._scaled_value(qty), self.units)

    def __mul__(self, qty):
        return Quantity(self.value * qty.value, self.units * qty.units)

    def __truediv__(self, qty):
        return Quantity(self.value * qty.value, self.units * qty.units)

    def __div__(self, qty):
        return self.__truediv__(qty)

    def __pow__(self, power):
        return Quantity(self.value ** power, self.units ** power)

    def __radd__(self, qty):
        return self.__add__(qty)

    def __rsub__(self, qty):
        return self._scaled_value(qty) - self._value

    def __rmul__(self, qty):
        return self.__mul__(qty)

    def __rtruediv__(self, qty):
        return qty.__truediv__(self._value)

    def __rdiv__(self, qty):
        return self.__rtruediv__(qty)

    def __neg__(self):
        return Quantity(-self._value, self.units)

    def __abs__(self):
        return Quantity(abs(self._value), self.units)

    def _scaled_value(self, qty):
        try:
            if qty.units.dimension != self.units.dimension:
                raise NineMLDimensionError(
                    "Cannot scale value as dimensions do not match ('{}' and "
                    "'{}')".format(self.units.dimension.name,
                                   qty.units.dimension.name))
            return qty.value * 10 ** (self.units.power - qty.units.power)
        except AttributeError:
            if self.units == unitless:
                return float(qty.value)
            else:
                raise NineMLDimensionError(
                    "Can only add/subtract numbers from dimensionless "
                    "quantities")
