
from typing import cast

from logging import Logger
from logging import getLogger

from xml.dom.minidom import Document
from xml.dom.minidom import Element

from ogl.sd.OglSDInstance import OglSDInstance
from ogl.sd.OglSDMessage import OglSDMessage

from pyutmodelv2.PyutSDInstance import PyutSDInstance
from pyutmodelv2.PyutSDMessage import PyutSDMessage

from oglio.Types import OglSDInstances
from oglio.Types import OglSDMessages
from oglio.toXmlV10.BaseOglToDom import BaseOglToDom
from oglio.toXmlV10.PyutToDom import PyutToDom
from oglio.toXmlV10.XmlConstants import XmlConstants


class OglSequenceToDom(BaseOglToDom):

    def __init__(self, xmlDocument: Document):

        super().__init__(xmlDocument=xmlDocument)
        self.logger: Logger = getLogger(__name__)

        self._pyutToMiniDom: PyutToDom = PyutToDom()

    def serialize(self, documentNode: Element, oglSDMessages: OglSDMessages, oglSDInstances: OglSDInstances) -> Element:

        for oglSDInstance in oglSDInstances.values():
            sdInstanceElement: Element = self._oglSDInstanceToDom(oglSDInstance, self._xmlDocument)
            documentNode.appendChild(sdInstanceElement)

        for oglSDMessage in oglSDMessages.values():
            sdMessageElement: Element = self._oglSDMessageToDom(oglSDMessage=oglSDMessage, xmlDoc=self._xmlDocument)
            documentNode.appendChild(sdMessageElement)

        return documentNode

    def _oglSDInstanceToDom(self, oglSDInstance: OglSDInstance, xmlDoc: Document) -> Element:
        """
        Export an OglSDInstance to a minidom Element

        Args:
            oglSDInstance:  Instance to convert
            xmlDoc:         xml document

        Returns:
            A new minidom element
        """
        root: Element = self._xmlDocument.createElement(XmlConstants.ELEMENT_GRAPHIC_SD_INSTANCE)

        # noinspection PyTypeChecker
        self._appendOglBase(oglSDInstance, root)    # type: ignore

        root.appendChild(self._pyutToMiniDom.pyutSDInstanceToDom(cast(PyutSDInstance, oglSDInstance.pyutSDInstance), xmlDoc))

        return root

    def _oglSDMessageToDom(self, oglSDMessage: OglSDMessage, xmlDoc: Document) -> Element:
        """
        Export an OglSDMessage to a minidom Element.

        Args:
            oglSDMessage:   Message to convert
            xmlDoc:         xml document

        Returns:
            A new minidom element
        """
        root = self._xmlDocument.createElement(XmlConstants.ELEMENT_GRAPHIC_SD_MESSAGE)

        pyutSDMessage: PyutSDMessage = oglSDMessage.pyutSDMessage
        root.appendChild(self._pyutToMiniDom.pyutSDMessageToDom(pyutSDMessage, xmlDoc))

        return root
