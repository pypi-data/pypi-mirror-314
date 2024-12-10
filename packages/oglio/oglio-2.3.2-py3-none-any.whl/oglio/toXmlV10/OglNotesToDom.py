
from typing import cast

from logging import Logger
from logging import getLogger

from xml.dom.minidom import Document
from xml.dom.minidom import Element

from pyutmodelv2.PyutNote import PyutNote

from ogl.OglNote import OglNote

from oglio.Types import OglNotes
from oglio.toXmlV10.BaseOglToDom import BaseOglToDom
from oglio.toXmlV10.PyutToDom import PyutToDom
from oglio.toXmlV10.XmlConstants import XmlConstants


class OglNotesToDom(BaseOglToDom):
    """
    Serializes OglNotes to DOM elements
    """

    def __init__(self, xmlDocument: Document):

        super().__init__(xmlDocument=xmlDocument)
        self.linksLogger: Logger = getLogger(__name__)

        self._pyutToMiniDom: PyutToDom = PyutToDom()

    def serialize(self, documentNode: Element, oglNotes: OglNotes) -> Element:

        for oglNote in oglNotes:
            textElement: Element = self._oglNoteToDom(oglNote, xmlDoc=self._xmlDocument)
            documentNode.appendChild(textElement)

        return documentNode

    def _oglNoteToDom(self, oglNote: OglNote, xmlDoc: Document) -> Element:
        """
        Export an OglNote to a minidom Element.

        Args:
            oglNote:    Note to convert
            xmlDoc:     xml document

        Returns:
            New minidom element
        """
        graphicNoteElement: Element = xmlDoc.createElement(XmlConstants.ELEMENT_GRAPHIC_NOTE)

        self._appendOglBase(oglNote, graphicNoteElement)

        graphicNoteElement.appendChild(self._pyutToMiniDom.pyutNoteToDom(cast(PyutNote, oglNote.pyutObject), xmlDoc))

        return graphicNoteElement
