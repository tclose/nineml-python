"""
docstring needed

:copyright: Copyright 2010-2013 by the Python lib9ML team, see AUTHORS.
:license: BSD-3, see LICENSE for details.
"""
from nineml.annotations import annotate
from nineml.utils import expect_single
from nineml.serialize import (
    get_elem_attr, unprocessed, NINEMLv1, extract_ns)
from nineml.exceptions import NineMLXMLBlockError
from nineml.annotations import read_annotations
from ...componentclass.visitors.xml import (
    ComponentClassXMLLoader, ComponentClassXMLWriter)
from .base import RandomDistributionVisitor


class RandomDistributionXMLLoader(ComponentClassXMLLoader,
                                  RandomDistributionVisitor):

    """This class is used by XMLReader interny.

    This class loads a NineML XML tree, and stores
    the components in ``components``. It o records which file each XML node
    was loaded in from, and stores this in ``component_srcs``.

    """

    @read_annotations
    @unprocessed
    def load_randomdistributionclass(self, element, **kwargs):
        ns = extract_ns(element.tag)
        if ns == NINEMLv1:
            lib_elem = expect_single(element.findall(NINEMLv1 +
                                                     'RandomDistribution'))
            if lib_elem.getchildren():
                raise NineMLXMLBlockError(
                    "Not expecting {} blocks within 'RandomDistribution' block"
                    .format(', '.join(e.tag for e in lib_elem.getchildren())))
        else:
            lib_elem = element
        blocks = self._load_blocks(
            element, block_names=('Parameter',),
            ignore=[(NINEMLv1, 'RandomDistribution')], **kwargs)
        return RandomDistribution(
            name=get_elem_attr(element, 'name', self.document, **kwargs),
            standard_library=get_elem_attr(lib_elem, 'standard_library',
                                          self.document, **kwargs),
            parameters=blocks["Parameter"],
            document=self.document)

    tag_to_loader = dict(
        tuple(ComponentClassXMLLoader.tag_to_loader.iteritems()) +
        (("RandomDistribution", load_randomdistributionclass),))


class RandomDistributionXMLWriter(ComponentClassXMLWriter,
                                  RandomDistributionVisitor):

    @annotate
    def visit_componentclass(self, component_class, **kwargs):  # @UnusedVariable @IgnorePep8
        if self.ns == NINEMLv1:
            elems = [e.accept_visitor(self)
                        for e in component_class.sorted_elements()]
            elems.append(
                self.E('RandomDistribution',
                       standard_library=component_class.standard_library))
            xml = self.E('ComponentClass', *elems, name=component_class.name)
        else:
            xml = self.E(component_class.nineml_type,
                         *(e.accept_visitor(self)
                           for e in component_class.sorted_elements()),
                         standard_library=component_class.standard_library,
                         name=component_class.name)
        return xml

from ..base import RandomDistribution
