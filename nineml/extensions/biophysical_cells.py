import urllib
from itertools import chain
from lxml import etree
from lxml.builder import E
import nineml.extensions.morphology
import nineml.extensions.biophysics

biophysical_cells_namespace = 'http://www.nineml.org/BiophysicalCells'
BIO_CELL_NINEML = "{%s}" % biophysical_cells_namespace

def parse(url):
    """
    Read a NineML user-layer file and return a Model object.

    If the URL does not have a scheme identifier, it is taken to refer to a
    local file.
    """
    if not isinstance(url, file):
        f = urllib.urlopen(url)
        doc = etree.parse(f)
        f.close()
    else:
        doc = etree.parse(url)
    root = doc.getroot()
    comp_classes = {}
    for element in root.findall(BIO_CELL_NINEML + ComponentClass.element_name):
        comp_class = ComponentClass.from_xml(element, url)
        comp_classes[comp_class.name] = comp_class
    return comp_classes


class ComponentClass(object):

    element_name = 'ComponentClass'

    def __init__(self, name, parameters, mappings, morphology, biophysics, url=None):
        self.name = name
        self.parameters = parameters
        self.mappings = mappings
        self.morphology = morphology
        self.biophysics = biophysics
        self.url = url

    def __repr__(self):
        return ("Biophysical cell class '{}' with parameters: '{}'"
                .format(self.name, "', '".join([p.name for p in self.parameters])))

    def check_consistency(self):
        pass  # Not implemented yet

    def to_xml(self):
        return E(self.element_name,
                 E(nineml.extensions.morphology.Morphology.element_name, self.morphology.to_xml()),
                 E(nineml.extensions.biophysics.BiophysicsModel.element_name, self.biophysics.to_xml()),
                 name=self.name,
                 *[c.to_xml() for c in chain(self.parameters.values(), self.mappings.values())])

    @classmethod
    def from_xml(cls, element):
        assert element.tag == BIO_CELL_NINEML + cls.element_name
        parameters = []
        mappings = []
        for child in element.getchildren():
            if child.tag == BIO_CELL_NINEML + Parameter.element_name:
                parameters.append(Parameter.from_xml(child))
            elif child.tag == BIO_CELL_NINEML + Mapping.element_name:
                mappings.append(Mapping.from_xml(child))
            elif child.tag == (nineml.extensions.morphology.MORPH_NINEML +
                               nineml.extensions.morphology.Morphology.element_name):
                morphology = nineml.extensions.morphology.Morphology.from_xml(child)
            elif child.tag == (nineml.extensions.biophysics.BIO_NINEML +
                               nineml.extensions.biophysics.BiophysicsModel.element_name):
                biophysics = nineml.extensions.biophysics.BiophysicsModel.from_xml(child)
            elif child.tag == etree.Comment:
                pass
            else:
                raise Exception("<{}> elements may not contain <{}> elements"
                                .format(cls.element_name, child.tag))
        return cls(element.attrib['name'], parameters, mappings, morphology, biophysics)


class Parameter(object):

    element_name = 'Parameter'

    component_name = 'Component'
    reference_name = 'Reference'

    def __init__(self, name, component, reference, segments):
        self.name = name
        self.component = component
        self.reference = reference
        self.segments = segments

    def __repr__(self):
        return ("{} parameter '{}' over {} segment divisions"
                .format(self.type_name, self.reference, len(self.segment_classes)))

    def to_xml(self):
        return E(self.element_name,
                 E(self.component_name, self.component),
                 E(self.reference_name, self.reference),
                 self.segments.to_xml(),
                 name=self.name)

    @classmethod
    def from_xml(cls, element):
        assert element.tag == BIO_CELL_NINEML + cls.element_name
        name = element.attrib['name']
        component = element.find(BIO_CELL_NINEML + cls.component_name).text.strip()
        reference = element.find(BIO_CELL_NINEML + cls.reference_name).text.strip()
        segments = Segments.from_xml(element.find(BIO_CELL_NINEML + Segments.element_name))
        return cls(name, component, reference, segments)


class Mapping(object):

    element_name = 'Mapping'

    def __init__(self, name, components, segments):
        self.name = name
        self.components = components
        self.segments = segments

    def __repr__(self):
        return ("'{}' mapping with biophysics(s): '{}'"
                .format(self.name, "', '".join([d.name for d in self.biophysicss])))

    def to_xml(self):
        return E(self.element_name,
                 self.components.to_xml(),
                 self.segments.to_xml(),
                 name=self.name)

    @classmethod
    def from_xml(cls, element):
        assert element.tag == BIO_CELL_NINEML + cls.element_name
        components = BiophysicsList.from_xml(element.find(BIO_CELL_NINEML + 
                                                          BiophysicsList.element_name))
        segments = Segments.from_xml(element.find(BIO_CELL_NINEML + Segments.element_name))
        return cls(element.attrib['name'], components, segments)


class Segments(list):

    element_name = 'Segments'
    classification_attr_name = 'classification'
    segment_class_name = "Class"

    def __init__(self, classification, segments):
        self.classification = classification
        self.extend(segments)

    def to_xml(self):
        return E(self.element_name, *self)

    @classmethod
    def from_xml(cls, element):
        assert element.tag == BIO_CELL_NINEML + cls.element_name
        classification = element.attrib[cls.classification_attr_name]
        segments = [c.text.strip() for c in element.findall(BIO_CELL_NINEML + cls.segment_class_name)]
        return cls(classification, segments)


class BiophysicsList(list):

    element_name = "Biophysics"
    component_name = "Component"

    def __init__(self, components):
        self.extend(components)

    def to_xml(self):
        return E(self.element_name, *self)

    @classmethod
    def from_xml(cls, element):
        assert element.tag == BIO_CELL_NINEML + cls.element_name
        components = [c.text.strip() for c in element.findall(BIO_CELL_NINEML + cls.component_name)]
        return cls(components)
