import h5py
from . import NINEML_BASE_NS
import nineml
from nineml.exceptions import (NineMLSerializationError,
                               NineMLSerializationNotSupportedError)
from .base import BaseSerializer, BaseUnserializer, BODY_ATTR, NS_ATTR
from nineml.exceptions import NineMLNameError


class HDF5Serializer(BaseSerializer):
    """
    A Serializer class that serializes to the HDF5 format
    """

    def __init__(self, fname, **kwargs):  # @UnusedVariable @IgnorePep8 @ReservedAssignment
        super(HDF5Serializer, self).__init__(**kwargs)
        self._file = h5py.File(fname, 'w')
        self._root = self.create_root()

    def create_elem(self, name, parent, namespace=None, **options):  # @UnusedVariable @IgnorePep8
        elem = parent.create_group(name)
        if namespace is not None:
            self.set_attr(elem, NS_ATTR, namespace, **options)

    def create_root(self, **options):  # @UnusedVariable
        return self._file.create_group(nineml.Document.nineml_type)

    def set_attr(self, serial_elem, name, value, **options):  # @UnusedVariable
        serial_elem.attrs[name] = value

    def set_body(self, serial_elem, value, sole=False, **options):  # @UnusedVariable @IgnorePep8
        self.set_attr(serial_elem, BODY_ATTR, value, **options)

    def to_file(self, serial_elem, file, **options):  # @UnusedVariable  @IgnorePep8 @ReservedAssignment
        if file is not self._file:
            raise NineMLSerializationError(
                "Can only write elem to file that is named in the __init__ "
                "method.")
        # Don't do anything as elements are written to file as they are
        # serialized

    def to_str(self, serial_elem, **options):  # @UnusedVariable  @IgnorePep8
        raise NineMLSerializationNotSupportedError(
            "'HDF5' format cannot be converted to a string")


class HDF5Unserializer(BaseUnserializer):
    """
    A Unserializer class unserializes the HDF5 format.
    """

    def get_children(self, serial_elem, **options):  # @UnusedVariable
        return serial_elem.iteritems()

    def get_attr(self, serial_elem, name, **options):  # @UnusedVariable
        return serial_elem.attrs[name]

    def get_body(self, serial_elem, sole=True, **options):  # @UnusedVariable
        return serial_elem.attrs[BODY_ATTR]

    def get_attr_keys(self, serial_elem, **options):  # @UnusedVariable
        return serial_elem.attrs.iterkeys()

    def get_namespace(self, serial_elem, **options):  # @UnusedVariable
        try:
            ns = self.get_attr(serial_elem, NS_ATTR, **options)
        except NineMLNameError:
            ns = NINEML_BASE_NS + self.version
        return ns

    def from_file(self, fname, **options):  # @UnusedVariable
        return h5py.File(fname)[nineml.Document.nineml_type]

    def from_str(self, string, **options):
        raise NineMLSerializationNotSupportedError(
            "'HDF5' format cannot be read from a string")