
from logging import Logger
from logging import getLogger

from xml.etree.ElementTree import Element
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import indent
from xml.etree.ElementTree import SubElement
from xml.etree.ElementTree import tostring
from xml.etree.ElementTree import fromstring

from oglio.Types import OglDocument

from oglio.toXmlV11.OglClassToXml import OglClassToXml
from oglio.toXmlV11.OglLinksToXml import OglLinksToXml
from oglio.toXmlV11.OglNotesToXml import OglNotesToXml
from oglio.toXmlV11.OglSequenceToXml import OglSequenceToXml
from oglio.toXmlV11.OglTextsToXml import OglTextsToXml
from oglio.toXmlV11.OglUseCasesToXml import OglUseCasesToXml

from oglio.toXmlV11.XmlConstants import XmlConstants

XML_VERSION: str = '11'

INDENT_SPACES: str = '    '     # TODO: Make this configurable
PRETTY_PRINT:  bool = True


class OglToXml:
    def __init__(self, projectCodePath: str):

        self.logger: Logger = getLogger(__name__)

        self._projectCodePath: str     = projectCodePath
        topElement:            Element = Element(XmlConstants.TOP_LEVEL_ELEMENT)

        topElement.set(XmlConstants.ATTR_VERSION, XML_VERSION)
        topElement.set(XmlConstants.ATTR_CODE_PATH, projectCodePath)

        tree: ElementTree = ElementTree(topElement)
        indent(tree, space='    ')

        self._topElement:  Element     = topElement
        self._tree:        ElementTree = tree
        self._prettyPrint: bool        = PRETTY_PRINT

    @property
    def prettyPrint(self) -> bool:
        return self._prettyPrint

    @prettyPrint.setter
    def prettyPrint(self, newValue: bool):
        self._prettyPrint = newValue

    @property
    def xml(self) -> str:
        """

        Returns:  The serialized XML in pretty print format
        """
        if self.prettyPrint is True:
            return self._toPrettyString(self._topElement)
        else:
            return self._toString(self._topElement)

    def serialize(self, oglDocument: OglDocument):

        oglClassToXml:    OglClassToXml    = OglClassToXml()
        oglLinksToXml:    OglLinksToXml    = OglLinksToXml()
        oglNotesToXml:    OglNotesToXml    = OglNotesToXml()
        oglTextsToXml:    OglTextsToXml    = OglTextsToXml()
        oglUseCasesToXml: OglUseCasesToXml = OglUseCasesToXml()
        oglSequenceToXml: OglSequenceToXml = OglSequenceToXml()

        documentElement: Element = self._oglDocumentToXml(oglDocument=oglDocument)

        oglClassToXml.serialize(documentTop=documentElement, oglClasses=oglDocument.oglClasses)
        oglLinksToXml.serialize(documentTop=documentElement, oglLinks=oglDocument.oglLinks)
        oglNotesToXml.serialize(documentTop=documentElement, oglNotes=oglDocument.oglNotes)
        oglTextsToXml.serialize(documentTop=documentElement, oglTexts=oglDocument.oglTexts)

        oglUseCasesToXml.serialize(documentTop=documentElement, oglUseCases=oglDocument.oglUseCases, oglActors=oglDocument.oglActors)
        oglSequenceToXml.serialize(documentTop=documentElement, oglSDInstances=oglDocument.oglSDInstances, oglSDMessages=oglDocument.oglSDMessages)

    def writeXml(self, fqFileName):
        """
        Persist the XML

        Args:
            fqFileName:  The fully qualified file name
        """
        with open(fqFileName, 'w') as fd:
            fd.write(self.xml)

    def _oglDocumentToXml(self, oglDocument: OglDocument) -> Element:

        attributes = {
            XmlConstants.ATTR_TYPE:              oglDocument.documentType,
            XmlConstants.ATTR_TITLE:             oglDocument.documentTitle,
            XmlConstants.ATTR_SCROLL_POSITION_X: str(oglDocument.scrollPositionX),
            XmlConstants.ATTR_SCROLL_POSITION_Y: str(oglDocument.scrollPositionY),
            XmlConstants.ATTR_PIXELS_PER_UNIT_X: str(oglDocument.pixelsPerUnitX),
            XmlConstants.ATTR_PIXELS_PER_UNIT_Y: str(oglDocument.pixelsPerUnitY),
        }
        documentTop: Element = SubElement(self._topElement, XmlConstants.ELEMENT_DOCUMENT, attrib=attributes)

        return documentTop

    def _toPrettyString(self, originalElement: Element):
        """
        Create a copy of the input originalElement
        Convert to string, then parse again
        tostring() returns a binary, so we need to decode it to get a string

        Args:
            originalElement:

        Returns:  Pretty printed XML
        """
        elementCopy: Element = fromstring(tostring(originalElement))
        indent(elementCopy, space=INDENT_SPACES, level=0)

        return self._toString(elementCopy)

    def _toString(self, element: Element) -> str:
        return tostring(element, encoding='iso-8859-1', xml_declaration=True).decode('utf-8')
