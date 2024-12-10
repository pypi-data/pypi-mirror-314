

from typing import Tuple

from logging import Logger
from logging import getLogger
from xml.dom.minidom import Document
from xml.dom.minidom import Element

from ogl.OglObject import OglObject

from oglio.toXmlV10.BaseToDom import BaseToDom
from oglio.toXmlV10.XmlConstants import XmlConstants


class BaseOglToDom(BaseToDom):

    def __init__(self, xmlDocument: Document):

        super().__init__()
        self.baseLogger:   Logger   = getLogger(__name__)
        self._xmlDocument: Document = xmlDocument

    def _appendOglBase(self, oglObject: OglObject, root: Element) -> Element:
        """
        Saves the position and size of the OGL object in an ML node.

        Args:
            oglObject:  OGL Object
            root:      XML node to update

        Returns:
            The updated element
        """
        # Saving size
        # w, h = oglObject.model.GetSize()
        w, h = oglObject.GetSize()
        simpleW, simpleH = self._getSimpleDimensions(w, h)
        root.setAttribute(XmlConstants.ATTR_WIDTH, simpleW)
        root.setAttribute(XmlConstants.ATTR_HEIGHT, simpleH)

        # Saving position
        x, y = oglObject.model.GetPosition()
        simpleX, simpleY = self._getSimpleCoordinates(x, y)
        root.setAttribute(XmlConstants.ATTR_X, simpleX)
        root.setAttribute(XmlConstants.ATTR_Y, simpleY)

        return root

    def _getSimpleDimensions(self, w: int, h: int) -> Tuple[str, str]:
        # reuse code but not name
        return self._getSimpleCoordinates(w, h)

    def _getSimpleCoordinates(self, x: int, y: int) -> Tuple[str, str]:
        """

        Args:
            x: coordinate
            y: coordinate

        Returns:
            Simple formatted string versions of the above

        """
        simpleX: str = str(int(x))      # some older files used float
        simpleY: str = str(int(y))      # some older files used float

        return simpleX, simpleY
