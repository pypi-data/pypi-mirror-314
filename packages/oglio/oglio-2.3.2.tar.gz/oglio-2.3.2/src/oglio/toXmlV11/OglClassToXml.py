
from logging import Logger
from logging import getLogger

from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement

from ogl.OglClass import OglClass

from oglio.Types import OglClasses
from oglio.toXmlV11.BaseOglToXml import BaseOglToXml
from oglio.toXmlV11.PyutToXml import PyutToXml

from oglio.toXmlV11.XmlConstants import XmlConstants


class OglClassToXml(BaseOglToXml):

    def __init__(self):
        super().__init__()
        self.logger: Logger = getLogger(__name__)
        self._pyutToXml: PyutToXml = PyutToXml()

    def serialize(self, documentTop: Element, oglClasses: OglClasses) -> Element:

        for oglClass in oglClasses:
            self._oglClassToXml(documentTop=documentTop, oglClass=oglClass)

        return documentTop

    def _oglClassToXml(self, documentTop: Element, oglClass: OglClass) -> Element:
        """
        Exports an OglClass to a minidom Element.

        Args:
            documentTop:     The document to append to
            oglClass:   Ogl Class to serialize

        Returns:
            The newly created `OglClass` Element
        """
        attributes = self._oglBaseAttributes(oglObject=oglClass)
        oglClassSubElement: Element = SubElement(documentTop, XmlConstants.ELEMENT_OGL_CLASS, attrib=attributes)

        self._pyutToXml.pyutClassToXml(graphicElement=oglClassSubElement, pyutClass=oglClass.pyutObject)

        return oglClassSubElement

