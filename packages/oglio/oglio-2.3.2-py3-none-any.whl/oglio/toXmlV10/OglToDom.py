
from typing import Tuple
from typing import cast

from logging import Logger
from logging import getLogger

from xml.dom.minidom import Document
from xml.dom.minidom import Element

from oglio.Types import OglActors
from oglio.Types import OglClasses
from oglio.Types import OglDocument
from oglio.Types import OglLinks
from oglio.Types import OglNotes
from oglio.Types import OglSDInstances
from oglio.Types import OglSDMessages
from oglio.Types import OglTexts
from oglio.Types import OglUseCases

from oglio.toXmlV10.BaseOglToDom import BaseOglToDom
from oglio.toXmlV10.OglClassesToDom import OglClassesToDom
from oglio.toXmlV10.OglLinksToDom import OglLinksToDom
from oglio.toXmlV10.OglNotesToDom import OglNotesToDom
from oglio.toXmlV10.OglSequenceToDom import OglSequenceToDom
from oglio.toXmlV10.OglTextsToDom import OglTextsToDom
from oglio.toXmlV10.OglUseCasesToDom import OglUseCasesToDom
from oglio.toXmlV10.XmlConstants import XmlConstants


class OglToDom(BaseOglToDom):
    """
    The refactored version of the original methods that were part of the monolithic
     PyutXml`xxx` classes.

     This version is
        * renamed for clarity
        * uses typing for developer clarity
        * removes 'magic' strings shared between it and the ToOgl/ToPyutXml classes
        * Updated using google docstrings

    """
    VERSION:             str = '10'
    ORIGINAL_XML_PROLOG: str = '<?xml version="1.0" ?>'
    FIXED_XML_PROLOG:    str = '<?xml version="1.0" encoding="iso-8859-1"?>'

    def __init__(self, projectVersion: str, projectCodePath: str):
        """

        Args:
            projectVersion:
            projectCodePath:
        """

        self.logger:     Logger    = getLogger(__name__)

        xmlDocument, topElement = self._createStarterXmlDocument(projectVersion=projectVersion, projectCodePath=projectCodePath)

        super().__init__(xmlDocument=xmlDocument)

        self._topElement:  Element  = topElement

        self._oglClassesToMiniDom:  OglClassesToDom  = OglClassesToDom(xmlDocument=self._xmlDocument)
        self._oglLinksToMiniDom:    OglLinksToDom    = OglLinksToDom(xmlDocument=self._xmlDocument)
        self._oglUseCasesToMiniDom: OglUseCasesToDom = OglUseCasesToDom(xmlDocument=self._xmlDocument)
        self._oglSequenceToDom:   OglSequenceToDom   = OglSequenceToDom(xmlDocument=self._xmlDocument)
        self._oglNotesToDom:      OglNotesToDom      = OglNotesToDom(xmlDocument=self._xmlDocument)
        self._oglTextsToDom:      OglTextsToDom      = OglTextsToDom(xmlDocument=self._xmlDocument)

    @property
    def xmlDocument(self) -> Document:
        """
        Presumably used to persist the document

        Returns:  The serialized Document
        """
        return self._xmlDocument

    @property
    def xml(self) -> str:
        """

        Returns:  The serialized XML in pretty print format
        """
        updatedXml: str = ''
        try:
            xmlText:    str = self._xmlDocument.toxml()
            updatedXml = OglToDom.setAsISOLatin(xmlText)
        except (ValueError, Exception) as e:
            self.logger.error(f'{e=}')

        return updatedXml

    @property
    def prettyXml(self) -> str:
        updatedXml: str = ''
        try:
            xmlText:    str = self._xmlDocument.toprettyxml()
            updatedXml = OglToDom.setAsISOLatin(xmlText)
        except (ValueError, Exception) as e:
            self.logger.error(f'{e=}')

        return updatedXml

    def serialize(self, oglDocument: OglDocument):

        documentNode: Element = self._oglDocumentToXml(oglDocument=oglDocument)

        self._topElement.appendChild(documentNode)

        oglClasses:     OglClasses     = cast(OglClasses, oglDocument.oglClasses)
        oglLinks:       OglLinks       = cast(OglLinks, oglDocument.oglLinks)
        oglTexts:       OglTexts       = cast(OglTexts, oglDocument.oglTexts)
        oglUseCases:    OglUseCases    = cast(OglUseCases, oglDocument.oglUseCases)
        oglActors:      OglActors      = cast(OglActors, oglDocument.oglActors)
        oglNotes:       OglNotes       = cast(OglNotes,  oglDocument.oglNotes)
        oglSDInstances: OglSDInstances = cast(OglSDInstances, oglDocument.oglSDInstances)
        oglSDMessages:  OglSDMessages  = cast(OglSDMessages,  oglDocument.oglSDMessages)

        documentNode = self._oglClassesToMiniDom.serialize(documentNode=documentNode, oglClasses=oglClasses)
        documentNode = self._oglNotesToDom.serialize(documentNode=documentNode, oglNotes=oglNotes)
        documentNode = self._oglTextsToDom.serialize(documentNode=documentNode, oglTexts=oglTexts)
        documentNode = self._oglUseCasesToMiniDom.serialize(documentNode=documentNode, oglUseCases=oglUseCases, oglActors=oglActors)
        documentNode = self._oglLinksToMiniDom.serialize(documentNode=documentNode, oglLinks=oglLinks)

        # noinspection PyUnusedLocal
        documentNode = self._oglSequenceToDom.serialize(documentNode=documentNode, oglSDMessages=oglSDMessages, oglSDInstances=oglSDInstances)

    def writeXml(self, fqFileName: str, prettyXml: bool = True):
        """
        Persist the XML

        Args:
            fqFileName:  The fully qualified file name
            prettyXml:   Do you Barbie XML?
        """
        if prettyXml is True:
            updatedXml: str = self.prettyXml
        else:
            updatedXml = self.xml

        with open(fqFileName, 'w') as fd:
            fd.write(updatedXml)

    @classmethod
    def setAsISOLatin(cls, xmlTextToUpdate: str) -> str:
        """
        Add attribute encoding = "iso-8859-1" this is not possible with minidom, so we use pattern matching

        Args:
            xmlTextToUpdate:  Old XML

        Returns:  Updated XML
        """
        retText: str = xmlTextToUpdate.replace(OglToDom.ORIGINAL_XML_PROLOG, OglToDom.FIXED_XML_PROLOG)
        return retText

    def _createStarterXmlDocument(self, projectVersion: str, projectCodePath: str) -> Tuple[Document, Element]:

        xmlDocument: Document = Document()

        topElement: Element = xmlDocument.createElement(XmlConstants.TOP_LEVEL_ELEMENT)

        topElement.setAttribute(XmlConstants.ATTR_VERSION, projectVersion)
        topElement.setAttribute(XmlConstants.ATTR_CODE_PATH, projectCodePath)

        xmlDocument.appendChild(topElement)

        return xmlDocument, topElement

    def _oglDocumentToXml(self, oglDocument: OglDocument) -> Element:

        documentNode = self._xmlDocument.createElement(XmlConstants.ELEMENT_DOCUMENT)

        documentNode.setAttribute(XmlConstants.ATTR_TYPE, oglDocument.documentType)
        documentNode.setAttribute(XmlConstants.ATTR_TITLE, oglDocument.documentTitle)

        documentNode.setAttribute(XmlConstants.ATTR_SCROLL_POSITION_X, str(oglDocument.scrollPositionX))
        documentNode.setAttribute(XmlConstants.ATTR_SCROLL_POSITION_Y, str(oglDocument.scrollPositionY))

        documentNode.setAttribute(XmlConstants.ATTR_PIXELS_PER_UNIT_X, str(oglDocument.pixelsPerUnitX))
        documentNode.setAttribute(XmlConstants.ATTR_PIXELS_PER_UNIT_Y, str(oglDocument.pixelsPerUnitY))

        return documentNode
