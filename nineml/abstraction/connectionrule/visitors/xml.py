"""
docstring needed

:copyright: Copyright 2010-2013 by the Python lib9ML team, see AUTHORS.
:license: BSD-3, see LICENSE for details.
"""
from nineml.annotations import annotate
from nineml.utils import expect_single
from nineml.exceptions import NineMLXMLBlockError
from nineml.serialize import (
    get_elem_attr, unprocessed, NINEMLv1, extract_ns)
from nineml.annotations import read_annotations
from ...componentclass.visitors.xml import (
    ComponentClassXMLLoader, ComponentClassXMLWriter)
from .base import ConnectionRuleVisitor


class ConnectionRuleXMLLoader(ComponentClassXMLLoader, ConnectionRuleVisitor):

    """This class is used by XMLReader interny.

    This class loads a NineML XML tree, and stores
    the components in ``components``. It o records which file each XML node
    was loaded in from, and stores this in ``component_srcs``.

    """

    @read_annotations
    @unprocessed
    def load_connectionruleclass(self, element, **kwargs):  # @UnusedVariable
        ns = extract_ns(element.tag)
        if ns == NINEMLv1:
            lib_elem = expect_single(element.findall(NINEMLv1 +
                                                     'ConnectionRule'))
            if lib_elem.getchildren():
                raise NineMLXMLBlockError(
                    "Not expecting {} blocks within 'ConnectionRule' block"
                    .format(', '.join(e.tag for e in lib_elem.getchildren())))
        else:
            lib_elem = element
        std_lib = get_elem_attr(lib_elem, 'standard_library', self.document,
                               **kwargs)
        blocks = self._load_blocks(
            element, block_names=('Parameter',),
            ignore=[(NINEMLv1, 'ConnectionRule')], **kwargs)
        return ConnectionRule(
            name=get_elem_attr(element, 'name', self.document, **kwargs),
            standard_library=std_lib,
            parameters=blocks["Parameter"],
            document=self.document)

    tag_to_loader = dict(
        tuple(ComponentClassXMLLoader.tag_to_loader.iteritems()) +
        (("ConnectionRule", load_connectionruleclass),))


class ConnectionRuleXMLWriter(ComponentClassXMLWriter):

    @annotate
    def visit_componentclass(self, component_class, **kwargs):  # @UnusedVariable @IgnorePep8
        if self.ns == NINEMLv1:
            elems = [e.accept_visitor(self)
                        for e in component_class.sorted_elements()]
            elems.append(
                self.E('ConnectionRule',
                       standard_library=component_class.standard_library))
            xml = self.E('ComponentClass', *elems, name=component_class.name)
        else:
            xml = self.E(component_class.nineml_type,
                         *(e.accept_visitor(self)
                           for e in component_class.sorted_elements()),
                         name=component_class.name,
                         standard_library=component_class.standard_library)
        return xml


from ..base import ConnectionRule  # @IgnorePep8
