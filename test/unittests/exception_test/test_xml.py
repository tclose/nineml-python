import unittest
from nineml.xml import (get_element_maker, from_child_xml, from_child_xml, from_child_xml, from_child_xml, from_child_xml, from_child_xml, get_xml_attr, get_xml_attr, get_subblock, get_subblock, unprocessed_xml, unprocessed_xml)
from nineml.utils.testing.comprehensive import instances_of_all_types
from nineml.exceptions import (NineMLXMLAttributeError, NineMLXMLBlockError, NineMLRuntimeError)


class TestExceptions(unittest.TestCase):

    def test_get_element_maker_ninemlruntimeerror(self):
        """
        line #: 39
        message: Unrecognised 9ML version {} (1.0

        context:
        --------
def get_element_maker(version):
    if isinstance(version, int):
        version = float(version)
    version = str(version)
    if str(version) == '1.0':
        element_maker = Ev1
    elif str(version) == '2.0':
        element_maker = E
    else:
        """
        self.assertRaises(
            NineMLRuntimeError,
            get_element_maker,
            version=-1.0)

    @unittest.skip('Skipping autogenerated unittest skeleton')
    def test_from_child_xml_ninemlxmlattributeerror(self):
        """
        line #: 74
        message: {} in '{}' has '{}' attributes when {} are expected

        context:
        --------
def from_child_xml(element, child_classes, document, multiple=False,
                   allow_reference=False, allow_none=False, within=None,
                   unprocessed=None, multiple_within=False,
                   allowed_attrib=[], **kwargs):
    \"\"\"
    Loads a child element from the element, matching the tag name to the
    appropriate class and calling its 'from_xml' method
    \"\"\"
    # Ensure child_classes is an iterable
    if isinstance(child_classes, type):
        child_classes = (child_classes,)
    assert child_classes, "No child classes supplied"
    # Get the namespace of the element (i.e. NineML version)
    xmlns = extract_xmlns(element.tag)
    # Get the parent element of the child elements to parse. For example the
    # in Projection elements where pre and post synaptic population references
    # are enclosed within 'Pre' or 'Post' tags respectively
    if within:
        within_elems = element.findall(xmlns + within)
        if len(within_elems) == 1:
            parent = within_elems[0]
            if any(a not in allowed_attrib for a in parent.attrib):
        """
        self.assertRaises(
            NineMLXMLAttributeError,
            from_child_xml,
            element=None,
            child_classes=None,
            document=None,
            multiple=False,
            allow_reference=False,
            allow_none=False,
            within=None,
            unprocessed=None,
            multiple_within=False,
            allowed_attrib=[])

    @unittest.skip('Skipping autogenerated unittest skeleton')
    def test_from_child_xml_ninemlxmlblockerror(self):
        """
        line #: 82
        message: {} in '{}' is only expected to contain a single child block, found {}

        context:
        --------
def from_child_xml(element, child_classes, document, multiple=False,
                   allow_reference=False, allow_none=False, within=None,
                   unprocessed=None, multiple_within=False,
                   allowed_attrib=[], **kwargs):
    \"\"\"
    Loads a child element from the element, matching the tag name to the
    appropriate class and calling its 'from_xml' method
    \"\"\"
    # Ensure child_classes is an iterable
    if isinstance(child_classes, type):
        child_classes = (child_classes,)
    assert child_classes, "No child classes supplied"
    # Get the namespace of the element (i.e. NineML version)
    xmlns = extract_xmlns(element.tag)
    # Get the parent element of the child elements to parse. For example the
    # in Projection elements where pre and post synaptic population references
    # are enclosed within 'Pre' or 'Post' tags respectively
    if within:
        within_elems = element.findall(xmlns + within)
        if len(within_elems) == 1:
            parent = within_elems[0]
            if any(a not in allowed_attrib for a in parent.attrib):
                raise NineMLXMLAttributeError(
                    "{} in '{}' has '{}' attributes when {} are expected"
                    .format(identify_element(parent), document.url,
                            "', '".join(parent.attrib.iterkeys()),
                            allowed_attrib))
            if not multiple_within and len([
                    c for c in parent.getchildren()
                    if c.tag != xmlns + 'Annotations']) > 1:
        """

        self.assertRaises(
            NineMLXMLBlockError,
            from_child_xml,
            element=None,
            child_classes=None,
            document=None,
            multiple=False,
            allow_reference=False,
            allow_none=False,
            within=None,
            unprocessed=None,
            multiple_within=False,
            allowed_attrib=[])

    @unittest.skip('Skipping autogenerated unittest skeleton')
    def test_from_child_xml_ninemlxmlblockerror2(self):
        """
        line #: 93
        message: Did not find {} block within {} element in '{}'

        context:
        --------
def from_child_xml(element, child_classes, document, multiple=False,
                   allow_reference=False, allow_none=False, within=None,
                   unprocessed=None, multiple_within=False,
                   allowed_attrib=[], **kwargs):
    \"\"\"
    Loads a child element from the element, matching the tag name to the
    appropriate class and calling its 'from_xml' method
    \"\"\"
    # Ensure child_classes is an iterable
    if isinstance(child_classes, type):
        child_classes = (child_classes,)
    assert child_classes, "No child classes supplied"
    # Get the namespace of the element (i.e. NineML version)
    xmlns = extract_xmlns(element.tag)
    # Get the parent element of the child elements to parse. For example the
    # in Projection elements where pre and post synaptic population references
    # are enclosed within 'Pre' or 'Post' tags respectively
    if within:
        within_elems = element.findall(xmlns + within)
        if len(within_elems) == 1:
            parent = within_elems[0]
            if any(a not in allowed_attrib for a in parent.attrib):
                raise NineMLXMLAttributeError(
                    "{} in '{}' has '{}' attributes when {} are expected"
                    .format(identify_element(parent), document.url,
                            "', '".join(parent.attrib.iterkeys()),
                            allowed_attrib))
            if not multiple_within and len([
                    c for c in parent.getchildren()
                    if c.tag != xmlns + 'Annotations']) > 1:
                raise NineMLXMLBlockError(
                    "{} in '{}' is only expected to contain a single child "
                    "block, found {}"
                    .format(identify_element(parent), document.url,
                            ", ".join(e.tag for e in parent.getchildren())))
            if unprocessed:
                unprocessed[0].discard(parent)
        elif not within_elems:
            if allow_none:
                return None
            else:
        """

        self.assertRaises(
            NineMLXMLBlockError,
            from_child_xml,
            element=None,
            child_classes=None,
            document=None,
            multiple=False,
            allow_reference=False,
            allow_none=False,
            within=None,
            unprocessed=None,
            multiple_within=False,
            allowed_attrib=[])

    @unittest.skip('Skipping autogenerated unittest skeleton')
    def test_from_child_xml_ninemlxmlblockerror3(self):
        """
        line #: 97
        message: Found unexpected multiple {} blocks within {} in '{}'

        context:
        --------
def from_child_xml(element, child_classes, document, multiple=False,
                   allow_reference=False, allow_none=False, within=None,
                   unprocessed=None, multiple_within=False,
                   allowed_attrib=[], **kwargs):
    \"\"\"
    Loads a child element from the element, matching the tag name to the
    appropriate class and calling its 'from_xml' method
    \"\"\"
    # Ensure child_classes is an iterable
    if isinstance(child_classes, type):
        child_classes = (child_classes,)
    assert child_classes, "No child classes supplied"
    # Get the namespace of the element (i.e. NineML version)
    xmlns = extract_xmlns(element.tag)
    # Get the parent element of the child elements to parse. For example the
    # in Projection elements where pre and post synaptic population references
    # are enclosed within 'Pre' or 'Post' tags respectively
    if within:
        within_elems = element.findall(xmlns + within)
        if len(within_elems) == 1:
            parent = within_elems[0]
            if any(a not in allowed_attrib for a in parent.attrib):
                raise NineMLXMLAttributeError(
                    "{} in '{}' has '{}' attributes when {} are expected"
                    .format(identify_element(parent), document.url,
                            "', '".join(parent.attrib.iterkeys()),
                            allowed_attrib))
            if not multiple_within and len([
                    c for c in parent.getchildren()
                    if c.tag != xmlns + 'Annotations']) > 1:
                raise NineMLXMLBlockError(
                    "{} in '{}' is only expected to contain a single child "
                    "block, found {}"
                    .format(identify_element(parent), document.url,
                            ", ".join(e.tag for e in parent.getchildren())))
            if unprocessed:
                unprocessed[0].discard(parent)
        elif not within_elems:
            if allow_none:
                return None
            else:
                raise NineMLXMLBlockError(
                    "Did not find {} block within {} element in '{}'"
                    .format(within, identify_element(element), document.url))
        else:
        """

        self.assertRaises(
            NineMLXMLBlockError,
            from_child_xml,
            element=None,
            child_classes=None,
            document=None,
            multiple=False,
            allow_reference=False,
            allow_none=False,
            within=None,
            unprocessed=None,
            multiple_within=False,
            allowed_attrib=[])

    @unittest.skip('Skipping autogenerated unittest skeleton')
    def test_from_child_xml_ninemlxmlblockerror4(self):
        """
        line #: 133
        message: Did not find any child blocks with the tag{s} '{child_cls_names}'in the {parent_name} in '{url}'

        context:
        --------
def from_child_xml(element, child_classes, document, multiple=False,
                   allow_reference=False, allow_none=False, within=None,
                   unprocessed=None, multiple_within=False,
                   allowed_attrib=[], **kwargs):
    \"\"\"
    Loads a child element from the element, matching the tag name to the
    appropriate class and calling its 'from_xml' method
    \"\"\"
    # Ensure child_classes is an iterable
    if isinstance(child_classes, type):
        child_classes = (child_classes,)
    assert child_classes, "No child classes supplied"
    # Get the namespace of the element (i.e. NineML version)
    xmlns = extract_xmlns(element.tag)
    # Get the parent element of the child elements to parse. For example the
    # in Projection elements where pre and post synaptic population references
    # are enclosed within 'Pre' or 'Post' tags respectively
    if within:
        within_elems = element.findall(xmlns + within)
        if len(within_elems) == 1:
            parent = within_elems[0]
            if any(a not in allowed_attrib for a in parent.attrib):
                raise NineMLXMLAttributeError(
                    "{} in '{}' has '{}' attributes when {} are expected"
                    .format(identify_element(parent), document.url,
                            "', '".join(parent.attrib.iterkeys()),
                            allowed_attrib))
            if not multiple_within and len([
                    c for c in parent.getchildren()
                    if c.tag != xmlns + 'Annotations']) > 1:
                raise NineMLXMLBlockError(
                    "{} in '{}' is only expected to contain a single child "
                    "block, found {}"
                    .format(identify_element(parent), document.url,
                            ", ".join(e.tag for e in parent.getchildren())))
            if unprocessed:
                unprocessed[0].discard(parent)
        elif not within_elems:
            if allow_none:
                return None
            else:
                raise NineMLXMLBlockError(
                    "Did not find {} block within {} element in '{}'"
                    .format(within, identify_element(element), document.url))
        else:
            raise NineMLXMLBlockError(
                "Found unexpected multiple {} blocks within {} in '{}'"
                .format(within, identify_element(element), document.url))
    else:
        parent = element
    # Get the list of child class names for error messages
    child_cls_names = "', '".join(c.nineml_type for c in child_classes)
    # Append all child classes
    children = []
    if allow_reference != 'only':
        for child_cls in child_classes:
            if xmlns == NINEMLv1:
                try:
                    tag_name = child_cls.v1_nineml_type
                except AttributeError:
                    tag_name = child_cls.nineml_type
            else:
                tag_name = child_cls.nineml_type
            for child_elem in parent.findall(xmlns + tag_name):
                children.append(child_cls.from_xml(child_elem, document,
                                                   **kwargs))
                if unprocessed and not within:
                    unprocessed[0].discard(child_elem)
    if allow_reference:
        for ref_elem in parent.findall(
                xmlns + nineml.reference.Reference.nineml_type):
            ref = nineml.reference.Reference.from_xml(ref_elem, document,
                                                      **kwargs)
            if isinstance(ref.user_object, child_classes):
                children.append(ref.user_object)
                if unprocessed and not within:
                    unprocessed[0].discard(ref_elem)
    if not children:
        if allow_none:
            result = [] if multiple else None
        else:
        """

        self.assertRaises(
            NineMLXMLBlockError,
            from_child_xml,
            element=None,
            child_classes=None,
            document=None,
            multiple=False,
            allow_reference=False,
            allow_none=False,
            within=None,
            unprocessed=None,
            multiple_within=False,
            allowed_attrib=[])

    @unittest.skip('Skipping autogenerated unittest skeleton')
    def test_from_child_xml_ninemlxmlblockerror5(self):
        """
        line #: 145
        message: Multiple children of types '{}' found within {} in '{}'

        context:
        --------
def from_child_xml(element, child_classes, document, multiple=False,
                   allow_reference=False, allow_none=False, within=None,
                   unprocessed=None, multiple_within=False,
                   allowed_attrib=[], **kwargs):
    \"\"\"
    Loads a child element from the element, matching the tag name to the
    appropriate class and calling its 'from_xml' method
    \"\"\"
    # Ensure child_classes is an iterable
    if isinstance(child_classes, type):
        child_classes = (child_classes,)
    assert child_classes, "No child classes supplied"
    # Get the namespace of the element (i.e. NineML version)
    xmlns = extract_xmlns(element.tag)
    # Get the parent element of the child elements to parse. For example the
    # in Projection elements where pre and post synaptic population references
    # are enclosed within 'Pre' or 'Post' tags respectively
    if within:
        within_elems = element.findall(xmlns + within)
        if len(within_elems) == 1:
            parent = within_elems[0]
            if any(a not in allowed_attrib for a in parent.attrib):
                raise NineMLXMLAttributeError(
                    "{} in '{}' has '{}' attributes when {} are expected"
                    .format(identify_element(parent), document.url,
                            "', '".join(parent.attrib.iterkeys()),
                            allowed_attrib))
            if not multiple_within and len([
                    c for c in parent.getchildren()
                    if c.tag != xmlns + 'Annotations']) > 1:
                raise NineMLXMLBlockError(
                    "{} in '{}' is only expected to contain a single child "
                    "block, found {}"
                    .format(identify_element(parent), document.url,
                            ", ".join(e.tag for e in parent.getchildren())))
            if unprocessed:
                unprocessed[0].discard(parent)
        elif not within_elems:
            if allow_none:
                return None
            else:
                raise NineMLXMLBlockError(
                    "Did not find {} block within {} element in '{}'"
                    .format(within, identify_element(element), document.url))
        else:
            raise NineMLXMLBlockError(
                "Found unexpected multiple {} blocks within {} in '{}'"
                .format(within, identify_element(element), document.url))
    else:
        parent = element
    # Get the list of child class names for error messages
    child_cls_names = "', '".join(c.nineml_type for c in child_classes)
    # Append all child classes
    children = []
    if allow_reference != 'only':
        for child_cls in child_classes:
            if xmlns == NINEMLv1:
                try:
                    tag_name = child_cls.v1_nineml_type
                except AttributeError:
                    tag_name = child_cls.nineml_type
            else:
                tag_name = child_cls.nineml_type
            for child_elem in parent.findall(xmlns + tag_name):
                children.append(child_cls.from_xml(child_elem, document,
                                                   **kwargs))
                if unprocessed and not within:
                    unprocessed[0].discard(child_elem)
    if allow_reference:
        for ref_elem in parent.findall(
                xmlns + nineml.reference.Reference.nineml_type):
            ref = nineml.reference.Reference.from_xml(ref_elem, document,
                                                      **kwargs)
            if isinstance(ref.user_object, child_classes):
                children.append(ref.user_object)
                if unprocessed and not within:
                    unprocessed[0].discard(ref_elem)
    if not children:
        if allow_none:
            result = [] if multiple else None
        else:
            raise NineMLXMLBlockError(
                "Did not find any child blocks with the tag{s} "
                "'{child_cls_names}'in the {parent_name} in '{url}'"
                .format(s=('s' if len(child_classes) else ''),
                        child_cls_names=child_cls_names,
                        parent_name=identify_element(parent),
                        url=document.url))
    elif multiple:
        result = children
    elif len(children) == 1:
        result = children[0]  # Expect single
    else:
        """

        self.assertRaises(
            NineMLXMLBlockError,
            from_child_xml,
            element=None,
            child_classes=None,
            document=None,
            multiple=False,
            allow_reference=False,
            allow_none=False,
            within=None,
            unprocessed=None,
            multiple_within=False,
            allowed_attrib=[])

    @unittest.skip('Skipping autogenerated unittest skeleton')
    def test_get_xml_attr_ninemlxmlattributeerror(self):
        """
        line #: 172
        message: {} in '{}' is missing the {} attribute (found '{}' attributes)

        context:
        --------
def get_xml_attr(element, name, document, unprocessed=None, in_block=False,
                 within=None, dtype=str, **kwargs):  # @UnusedVariable @IgnorePep8
    \"\"\"
    Gets an attribute from an xml element with exception handling
    \"\"\"
    if in_block:
        sub_elem = get_subblock(element, name, unprocessed, document)
        attr_str = sub_elem.text
    else:
        if within is not None:
            elem = get_subblock(element, within, unprocessed, document)
        else:
            elem = element
        try:
            attr_str = elem.attrib[name]
            if unprocessed:
                unprocessed[1].discard(name)
        except KeyError, e:
            try:
                return kwargs['default']
            except KeyError:
        """

        self.assertRaises(
            NineMLXMLAttributeError,
            get_xml_attr,
            element=None,
            name=None,
            document=None,
            unprocessed=None,
            in_block=False,
            within=None,
            dtype=str)

    @unittest.skip('Skipping autogenerated unittest skeleton')
    def test_get_xml_attr_ninemlxmlattributeerror2(self):
        """
        line #: 183
        message: '{}' attribute of {} in '{}', {}, cannot be converted to {} type

        context:
        --------
def get_xml_attr(element, name, document, unprocessed=None, in_block=False,
                 within=None, dtype=str, **kwargs):  # @UnusedVariable @IgnorePep8
    \"\"\"
    Gets an attribute from an xml element with exception handling
    \"\"\"
    if in_block:
        sub_elem = get_subblock(element, name, unprocessed, document)
        attr_str = sub_elem.text
    else:
        if within is not None:
            elem = get_subblock(element, within, unprocessed, document)
        else:
            elem = element
        try:
            attr_str = elem.attrib[name]
            if unprocessed:
                unprocessed[1].discard(name)
        except KeyError, e:
            try:
                return kwargs['default']
            except KeyError:
                raise NineMLXMLAttributeError(
                    "{} in '{}' is missing the {} attribute (found '{}' "
                    "attributes)".format(
                        identify_element(elem), document.url, e,
                        "', '".join(elem.attrib.iterkeys())))
    try:
        attr = dtype(attr_str)
    except ValueError, e:
        if isinstance(e, NineMLRuntimeError):
            raise
        else:
        """

        self.assertRaises(
            NineMLXMLAttributeError,
            get_xml_attr,
            element=None,
            name=None,
            document=None,
            unprocessed=None,
            in_block=False,
            within=None,
            dtype=str)

    @unittest.skip('Skipping autogenerated unittest skeleton')
    def test_get_subblock_ninemlxmlblockerror(self):
        """
        line #: 197
        message: Did not find and child blocks with the tag '{}' within {} in '{url}'

        context:
        --------
def get_subblock(element, name, unprocessed, document, **kwargs):  # @UnusedVariable @IgnorePep8
    xmlns = extract_xmlns(element.tag)
    found = element.findall(xmlns + name)
    if len(found) == 1:
        if unprocessed:
            unprocessed[0].discard(found[0])
    elif not found:
        """

        self.assertRaises(
            NineMLXMLBlockError,
            get_subblock,
            element=None,
            name=None,
            unprocessed=None,
            document=None)

    @unittest.skip('Skipping autogenerated unittest skeleton')
    def test_get_subblock_ninemlxmlblockerror2(self):
        """
        line #: 202
        message: Found multiple child blocks with the tag '{}' within {} in '{url}'

        context:
        --------
def get_subblock(element, name, unprocessed, document, **kwargs):  # @UnusedVariable @IgnorePep8
    xmlns = extract_xmlns(element.tag)
    found = element.findall(xmlns + name)
    if len(found) == 1:
        if unprocessed:
            unprocessed[0].discard(found[0])
    elif not found:
        raise NineMLXMLBlockError(
            "Did not find and child blocks with the tag '{}' within {} in "
            "'{url}'".format(name, identify_element(element),
                             url=document.url))
    else:
        """

        self.assertRaises(
            NineMLXMLBlockError,
            get_subblock,
            element=None,
            name=None,
            unprocessed=None,
            document=None)

    @unittest.skip('Skipping autogenerated unittest skeleton')
    def test_from_xml_with_exception_handling_ninemlxmlblockerror(self):
        """
        line #: 267
        message: Found unrecognised block{s} '{remaining}' within {elem_name} in '{url}'

        context:
        --------
def unprocessed_xml(from_xml):
    def from_xml_with_exception_handling(cls, element, *args, **kwargs):  # @UnusedVariable @IgnorePep8
        # Get the document object for error messages
        if args:  # if UL classmethod
            document = args[0]
            xmlns = extract_xmlns(element.tag)
            if xmlns == NINEMLv1:
                try:
                    nineml_type = cls.v1_nineml_type
                except AttributeError:
                    nineml_type = cls.nineml_type
            else:
                nineml_type = cls.nineml_type
            # Check the tag of the element matches the class names
            assert element.tag in (xmlns + nineml_type), (
                "Found '{}' element, expected '{}'"
                .format(element.tag, cls.nineml_type))
        else:
            document = cls.document  # if AL visitor method
        # Keep track of which blocks and attributes were processed within the
        # element
        unprocessed = (set(e for e in element.getchildren()
                           if not isinstance(e, etree._Comment)),
                       set(element.attrib.iterkeys()))
        # The decorated method
        obj = from_xml(cls, element, *args, unprocessed=unprocessed,
                       **kwargs)
        # Check to see if there were blocks that were unprocessed in the
        # element
        blocks, attrs = unprocessed
        if blocks:
        """

        self.assertRaises(
            NineMLXMLBlockError,
            unprocessed_xml(from_xml=None),
            element=None)

    @unittest.skip('Skipping autogenerated unittest skeleton')
    def test_from_xml_with_exception_handling_ninemlxmlattributeerror(self):
        """
        line #: 274
        message: Found unrecognised attribute{s} '{remaining}' within {elem_name} in '{url}'

        context:
        --------
def unprocessed_xml(from_xml):
    def from_xml_with_exception_handling(cls, element, *args, **kwargs):  # @UnusedVariable @IgnorePep8
        # Get the document object for error messages
        if args:  # if UL classmethod
            document = args[0]
            xmlns = extract_xmlns(element.tag)
            if xmlns == NINEMLv1:
                try:
                    nineml_type = cls.v1_nineml_type
                except AttributeError:
                    nineml_type = cls.nineml_type
            else:
                nineml_type = cls.nineml_type
            # Check the tag of the element matches the class names
            assert element.tag in (xmlns + nineml_type), (
                "Found '{}' element, expected '{}'"
                .format(element.tag, cls.nineml_type))
        else:
            document = cls.document  # if AL visitor method
        # Keep track of which blocks and attributes were processed within the
        # element
        unprocessed = (set(e for e in element.getchildren()
                           if not isinstance(e, etree._Comment)),
                       set(element.attrib.iterkeys()))
        # The decorated method
        obj = from_xml(cls, element, *args, unprocessed=unprocessed,
                       **kwargs)
        # Check to see if there were blocks that were unprocessed in the
        # element
        blocks, attrs = unprocessed
        if blocks:
            raise NineMLXMLBlockError(
                "Found unrecognised block{s} '{remaining}' within "
                "{elem_name} in '{url}'"
                .format(s=('s' if len(blocks) > 1 else ''),
                        remaining="', '".join(str(b.tag) for b in blocks),
                        elem_name=identify_element(element), url=document.url))
        if attrs:
        """

        self.assertRaises(
            NineMLXMLAttributeError,
            unprocessed_xml(from_xml=None),
            element=None)

