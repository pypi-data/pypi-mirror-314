
from logging import Logger
from logging import getLogger

from xml.dom.minidom import Document
from xml.dom.minidom import Element

from ogl.OglText import OglText

from oglio.Types import OglTexts

from oglio.toXmlV10.BaseOglToDom import BaseOglToDom
from oglio.toXmlV10.PyutToDom import PyutToDom
from oglio.toXmlV10.XmlConstants import XmlConstants


class OglTextsToDom(BaseOglToDom):
    """
    Serialize Ogl Text objects to DOM
    """
    def __init__(self, xmlDocument: Document):

        super().__init__(xmlDocument=xmlDocument)
        self.linksLogger: Logger = getLogger(__name__)

        self._pyutToMiniDom: PyutToDom = PyutToDom()

    def serialize(self, documentNode: Element, oglTexts: OglTexts) -> Element:

        for oglText in oglTexts:
            textElement: Element = self._oglTextToDom(oglText, xmlDoc=self._xmlDocument)
            documentNode.appendChild(textElement)

        return documentNode

    def _oglTextToDom(self, oglText: OglText, xmlDoc: Document) -> Element:

        root: Element = xmlDoc.createElement(XmlConstants.ELEMENT_GRAPHIC_TEXT)

        self._appendOglBase(oglText, root)

        root.setAttribute(XmlConstants.ATTR_TEXT_SIZE, str(oglText.textSize))
        root.setAttribute(XmlConstants.ATTR_IS_BOLD, str(oglText.isBold))
        root.setAttribute(XmlConstants.ATTR_IS_ITALICIZED, str(oglText.isItalicized))
        root.setAttribute(XmlConstants.ATTR_FONT_FAMILY, oglText.textFontFamily.value)

        root.appendChild(self._pyutToMiniDom.pyutTextToDom(oglText.pyutText, xmlDoc))

        return root
