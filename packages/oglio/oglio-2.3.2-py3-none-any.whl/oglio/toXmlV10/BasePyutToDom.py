
from xml.dom.minidom import Element

from pyutmodelv2.PyutClassCommon import PyutClassCommon

from oglio.toXmlV10.BaseToDom import BaseToDom
from oglio.toXmlV10.XmlConstants import XmlConstants


class BasePyutToDom(BaseToDom):

    def __init__(self):
        super().__init__()

    def _pyutClassCommonToXml(self, classCommon: PyutClassCommon, root: Element) -> Element:

        root.setAttribute(XmlConstants.ATTR_DESCRIPTION, classCommon.description)
        # root.setAttribute(PyutXmlConstants.ATTR_FILENAME,    pyutInterface.getFilename())

        return root
