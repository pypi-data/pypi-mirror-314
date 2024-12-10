
from logging import Logger
from logging import getLogger

from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement

from pyutmodelv2.PyutSDMessage import PyutSDMessage

from ogl.sd.OglSDInstance import OglSDInstance
from ogl.sd.OglSDMessage import OglSDMessage

from oglio.Types import OglSDInstances
from oglio.Types import OglSDMessages

from oglio.toXmlV11.InternalTypes import ElementAttributes
from oglio.toXmlV11.XmlConstants import XmlConstants
from oglio.toXmlV11.BaseOglToXml import BaseOglToXml
from oglio.toXmlV11.PyutToXml import PyutToXml


class OglSequenceToXml(BaseOglToXml):
    def __init__(self):
        super().__init__()
        self.logger: Logger = getLogger(__name__)

        self._pyutToXml: PyutToXml = PyutToXml()

    def serialize(self, documentTop: Element, oglSDMessages: OglSDMessages, oglSDInstances: OglSDInstances) -> Element:

        for oglSDInstance in oglSDInstances.values():
            self._oglSDInstanceToXml(documentTop=documentTop, oglSDInstance=oglSDInstance)

        for oglSDMessage in oglSDMessages.values():
            self._oglSDMessageToXml(documentTop=documentTop, oglSDMessage=oglSDMessage)

        return documentTop

    def _oglSDInstanceToXml(self, documentTop: Element, oglSDInstance: OglSDInstance, ) -> Element:
        """
        Export an OglSDInstance to a minidom Element

        Args:
            documentTop:    XML Element
            oglSDInstance:  Instance to convert

        Returns:
            An element
        """
        w, h = oglSDInstance.GetSize()
        x, y = oglSDInstance.GetPosition()

        attributes: ElementAttributes = ElementAttributes({
            XmlConstants.ATTR_WIDTH:  str(w),
            XmlConstants.ATTR_HEIGHT: str(h),
            XmlConstants.ATTR_X:      str(x),
            XmlConstants.ATTR_Y:      str(y),
        })

        oglSDInstanceElement: Element = SubElement(documentTop, XmlConstants.ELEMENT_OGL_SD_INSTANCE, attrib=attributes)

        self._pyutToXml.pyutSDInstanceToXml(pyutSDInstance=oglSDInstance.pyutSDInstance, oglSDInstanceElement=oglSDInstanceElement)

        return oglSDInstanceElement

    def _oglSDMessageToXml(self, documentTop: Element, oglSDMessage: OglSDMessage) -> Element:
        """
        Export an OglSDMessage to a minidom Element.

        Args:
            documentTop:    XML Element
            oglSDMessage:   Message to convert

        Returns:
            An element
        """
        pyutSDMessage: PyutSDMessage = oglSDMessage.pyutSDMessage

        oglSDMessageElement: Element = SubElement(documentTop, XmlConstants.ELEMENT_OGL_SD_MESSAGE)

        self._pyutToXml.pyutSDMessageToXml(pyutSDMessage=pyutSDMessage, oglSDMessageElement=oglSDMessageElement)
        return oglSDMessageElement
