
from typing import cast

from logging import Logger
from logging import getLogger

from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement

from oglio.Types import OglTexts

from ogl.OglText import OglText

from oglio.toXmlV11.PyutToXml import PyutToXml
from oglio.toXmlV11.XmlConstants import XmlConstants
from oglio.toXmlV11.BaseOglToXml import BaseOglToXml


class OglTextsToXml(BaseOglToXml):
    def __init__(self):
        super().__init__()
        self.logger: Logger = getLogger(__name__)

        self._pyutToXml: PyutToXml = PyutToXml()

    def serialize(self, documentTop: Element, oglTexts: OglTexts) -> Element:

        for text in oglTexts:
            oglText: OglText = cast(OglText, text)
            oglTextElement: Element = self._oglTextToXml(documentTop=documentTop, oglText=oglText)
            self._pyutToXml.pyutTextToXml(pyutText=oglText.pyutObject, oglTextElement=oglTextElement)

        return documentTop

    def _oglTextToXml(self, documentTop: Element, oglText: OglText) -> Element:

        attributes = self._oglBaseAttributes(oglObject=oglText)
        oglTextSubElement: Element = SubElement(documentTop, XmlConstants.ELEMENT_OGL_TEXT, attrib=attributes)

        return oglTextSubElement
