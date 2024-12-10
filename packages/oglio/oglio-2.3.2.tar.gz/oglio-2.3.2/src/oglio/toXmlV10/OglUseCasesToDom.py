
from typing import cast

from logging import Logger
from logging import getLogger

from xml.dom.minidom import Document
from xml.dom.minidom import Element

from pyutmodelv2.PyutActor import PyutActor
from pyutmodelv2.PyutUseCase import PyutUseCase

from ogl.OglActor import OglActor
from ogl.OglUseCase import OglUseCase

from oglio.Types import OglActors
from oglio.Types import OglUseCases
from oglio.toXmlV10.BaseOglToDom import BaseOglToDom
from oglio.toXmlV10.PyutToDom import PyutToDom
from oglio.toXmlV10.XmlConstants import XmlConstants


class OglUseCasesToDom(BaseOglToDom):
    def __init__(self,  xmlDocument: Document):

        super().__init__(xmlDocument)

        self.useCaseLogger: Logger = getLogger(__name__)

        self._pyutToMiniDom: PyutToDom = PyutToDom()

    def serialize(self, documentNode: Element, oglUseCases: OglUseCases, oglActors: OglActors) -> Element:
        """

        Args:
            documentNode:
            oglUseCases:    Ogl Use Case objects
            oglActors:      Ogl Actor objects

        Returns:  The minidom element
        """

        for oglActor in oglActors:
            actorElement: Element = self._oglActorToDom(oglActor=oglActor, xmlDoc=self._xmlDocument)
            documentNode.appendChild(actorElement)

        for oglUseCase in oglUseCases:
            self.useCaseLogger.debug(f'{oglUseCase}')
            useCaseElement: Element = self._oglUseCaseToDom(oglUseCase=oglUseCase, xmlDoc=self._xmlDocument)
            documentNode.appendChild(useCaseElement)

        return documentNode

    def _oglUseCaseToDom(self, oglUseCase: OglUseCase, xmlDoc: Document) -> Element:
        """
        Export an OglUseCase to a minidom Element.

        Args:
            oglUseCase:  UseCase to convert
            xmlDoc:      xml document

        Returns:
            A new use case minidom element
        """
        useCaseElement: Element = xmlDoc.createElement(XmlConstants.ELEMENT_GRAPHIC_USE_CASE)

        self._appendOglBase(oglUseCase, useCaseElement)

        useCaseElement.appendChild(self._pyutToMiniDom.pyutUseCaseToDom(cast(PyutUseCase, oglUseCase.pyutObject), xmlDoc))

        return useCaseElement

    def _oglActorToDom(self, oglActor: OglActor, xmlDoc: Document) -> Element:
        """
        Exporting an OglActor to a minidom Element.

        Args:
            oglActor:   Actor to convert
            xmlDoc:     xml document

        Returns:
            New minidom element
        """
        pyutActorElement: Element = xmlDoc.createElement(XmlConstants.ELEMENT_GRAPHIC_ACTOR)

        self._appendOglBase(oglActor, pyutActorElement)

        pyutActorElement.appendChild(self._pyutToMiniDom.pyutActorToDom(cast(PyutActor, oglActor.pyutObject), xmlDoc))

        return pyutActorElement
