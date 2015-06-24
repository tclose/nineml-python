from copy import copy
from collections import defaultdict
from nineml.xmlns import E, NINEML
from nineml import DocumentLevelObject
from itertools import chain


class Annotations(defaultdict, DocumentLevelObject):
    """
    Defines the dimension used for quantity units
    """

    element_name = 'Annotations'

    @classmethod
    def _dict_tree(cls):
        return defaultdict(cls._dict_tree)

    def __init__(self, *args, **kwargs):
        # Create an infinite (on request) tree of defaultdicts
        super(Annotations, self).__init__(self._dict_tree, *args, **kwargs)

    def __repr__(self):
        return ("Annotations({})"
                .format(', '.join('{}={}'.format(k, v)
                                  for k, v in self.iteritems())))

    def to_xml(self):
        return E(self.element_name,
                 *chain(*[[E(k, str(v)) for k, v in dct.iteritems()]
                          for dct in self.itervalues()]))

    @classmethod
    def from_xml(cls, element):
        children = {}
        for child in element.getchildren():
            children[child.tag] = child.text
        kwargs = {NINEML: children}
        return cls(**kwargs)


def read_annotations(from_xml):
    def annotate_from_xml(cls, element, *args, **kwargs):
        annot_elem = expect_none_or_single(
            element.findall(NINEML + Annotations.element_name))
        if annot_elem is not None:
            # Extract the annotations
            annotations = Annotations.from_xml(annot_elem)
            # Get a copy of the element with the annotations stripped
            element = copy(element)
            element.remove(element.find(NINEML + Annotations.element_name))
        else:
            annotations = Annotations()
        kwargs['annotations'] = annotations
        nineml_object = from_xml(cls, element, *args, **kwargs)
        nineml_object.annotations.update(annotations.iteritems())
        return nineml_object
    return annotate_from_xml


def annotate_xml(to_xml):
    def annotate_to_xml(self, *args, **kwargs):
        elem = to_xml(self, *args, **kwargs)
        # If User Layer class
        if hasattr(self, 'annotations') and self.annotations:
            elem.append(self.annotations.to_xml())
        # If Abstraction Layer class
        elif (len(args) and hasattr(args[0], 'annotations') and
              args[0].annotations):
            elem.append(args[0].annotations.to_xml())
        return elem
    return annotate_to_xml


NO_DIMENSION_CHECK = 'NoDimensionCheck'

from nineml.utils import expect_none_or_single
