
from logging import Logger
from logging import getLogger
from typing import cast

from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement

from ogl.OglActor import OglActor
from ogl.OglUseCase import OglUseCase

from oglio.Types import OglActors
from oglio.Types import OglUseCases
from oglio.toXmlV11.XmlConstants import XmlConstants

from oglio.toXmlV11.BaseOglToXml import BaseOglToXml
from oglio.toXmlV11.PyutToXml import PyutToXml


class OglUseCasesToXml(BaseOglToXml):
    """
    TODO:  Don't forget the OGL Actors !!

    """
    def __init__(self):
        super().__init__()
        self.logger: Logger = getLogger(__name__)

        self._pyutToXml: PyutToXml = PyutToXml()

    def serialize(self, documentTop: Element, oglUseCases: OglUseCases, oglActors: OglActors) -> Element:

        for actor in oglActors:
            oglActor:        OglActor = cast(OglActor, actor)
            oglActorElement: Element  = self._oglActorToXml(documentTop=documentTop, oglActor=oglActor)
            self._pyutToXml.pyutActorToXml(pyutActor=oglActor.pyutObject, oglActorElement=oglActorElement)

        for useCase in oglUseCases:
            oglUseCase:        OglUseCase = cast(OglUseCase, useCase)
            oglUseCaseElement: Element    = self._oglUseCaseToXml(documentTop=documentTop, oglUseCase=oglUseCase)
            self._pyutToXml.pyutUseCaseToXml(pyutUseCase=oglUseCase.pyutObject, oglUseCaseElement=oglUseCaseElement)

        return documentTop

    def _oglUseCaseToXml(self, documentTop: Element, oglUseCase: OglUseCase) -> Element:

        attributes = self._oglBaseAttributes(oglObject=oglUseCase)
        oglTextSubElement: Element = SubElement(documentTop, XmlConstants.ELEMENT_OGL_USE_CASE, attrib=attributes)

        return oglTextSubElement

    def _oglActorToXml(self, documentTop: Element, oglActor: OglActor) -> Element:

        attributes = self._oglBaseAttributes(oglObject=oglActor)
        pyutActorSubElement: Element = SubElement(documentTop, XmlConstants.ELEMENT_OGL_ACTOR, attrib=attributes)

        return pyutActorSubElement
