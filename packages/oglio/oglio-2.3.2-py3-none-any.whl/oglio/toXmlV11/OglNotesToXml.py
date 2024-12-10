
from typing import cast

from logging import Logger
from logging import getLogger

from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement

from ogl.OglNote import OglNote

from oglio.Types import OglNotes

from oglio.toXmlV11.PyutToXml import PyutToXml
from oglio.toXmlV11.XmlConstants import XmlConstants
from oglio.toXmlV11.BaseOglToXml import BaseOglToXml


class OglNotesToXml(BaseOglToXml):
    def __init__(self):
        super().__init__()
        self.logger: Logger = getLogger(__name__)

        self._pyutToXml: PyutToXml = PyutToXml()

    def serialize(self, documentTop: Element, oglNotes: OglNotes) -> Element:

        for note in oglNotes:
            oglNote: OglNote = cast (OglNote, note)
            oglNoteElement: Element = self._oglNoteToXml(documentTop=documentTop, oglNote=oglNote)
            self._pyutToXml.pyutNoteToXml(pyutNote=oglNote.pyutObject, oglNoteElement=oglNoteElement)

        return documentTop

    def _oglNoteToXml(self, documentTop: Element, oglNote: OglNote) -> Element:

        attributes = self._oglBaseAttributes(oglObject=oglNote)
        oglNoteSubElement: Element = SubElement(documentTop, XmlConstants.ELEMENT_OGL_NOTE, attrib=attributes)

        return oglNoteSubElement
