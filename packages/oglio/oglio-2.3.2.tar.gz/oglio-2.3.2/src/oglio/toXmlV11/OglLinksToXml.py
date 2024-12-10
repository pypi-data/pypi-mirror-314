
from logging import Logger
from logging import getLogger
from typing import Tuple

from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement

from codeallyadvanced.ui.AttachmentSide import AttachmentSide

from miniogl.SelectAnchorPoint import SelectAnchorPoint

from ogl.OglAssociation import OglAssociation
from ogl.OglAssociationLabel import OglAssociationLabel
from ogl.OglInterface2 import OglInterface2
from ogl.OglLink import OglLink

from oglio.Types import OglLinks

from oglio.toXmlV11.PyutToXml import PyutToXml
from oglio.toXmlV11.XmlConstants import XmlConstants
from oglio.toXmlV11.BaseOglToXml import BaseOglToXml
from oglio.toXmlV11.InternalTypes import ElementAttributes


class OglLinksToXml(BaseOglToXml):
    def __init__(self):
        super().__init__()
        self.logger: Logger = getLogger(__name__)

        self._pyutToXml: PyutToXml = PyutToXml()

    def serialize(self, documentTop: Element, oglLinks: OglLinks) -> Element:

        for oglLink in oglLinks:
            if isinstance(oglLink, OglInterface2):
                self._oglInterface2ToXml(documentElement=documentTop, oglInterface=oglLink)
            else:
                self._oglLinkToXml(documentElement=documentTop, oglLink=oglLink)

        return documentTop

    def _oglLinkToXml(self, documentElement: Element, oglLink: OglLink) -> Element:

        attributes:        ElementAttributes = self._oglLinkAttributes(oglLink=oglLink)
        oglLinkSubElement: Element           = SubElement(documentElement, XmlConstants.ELEMENT_OGL_LINK, attrib=attributes)

        if isinstance(oglLink, OglAssociation):

            center: OglAssociationLabel = oglLink.centerLabel
            src:    OglAssociationLabel = oglLink.sourceCardinality
            dst:    OglAssociationLabel = oglLink.destinationCardinality
            associationLabels = {
                XmlConstants.ELEMENT_ASSOCIATION_CENTER_LABEL:      center,
                XmlConstants.ELEMENT_ASSOCIATION_SOURCE_LABEL:      src,
                XmlConstants.ELEMENT_ASSOCIATION_DESTINATION_LABEL: dst
            }
            for eltName in associationLabels:
                oglAssociationLabel: OglAssociationLabel = associationLabels[eltName]

                relativePosition: Tuple[int, int] = oglAssociationLabel.GetRelativePosition()
                x: int = relativePosition[0]
                y: int = relativePosition[1]

                labelAttributes: ElementAttributes = ElementAttributes({
                    XmlConstants.ATTR_X: str(x),
                    XmlConstants.ATTR_Y: str(y),
                })
                # noinspection PyUnusedLocal
                labelElement: Element = SubElement(oglLinkSubElement, eltName, attrib=labelAttributes)

        # save control points (not anchors!)
        for x, y in oglLink.segments[1:-1]:
            controlPointAttributes: ElementAttributes = ElementAttributes({
                XmlConstants.ATTR_X: str(x),
                XmlConstants.ATTR_Y: str(y),
            })
            SubElement(oglLinkSubElement, XmlConstants.ELEMENT_MODEL_CONTROL_POINT, attrib=controlPointAttributes)

        self._pyutToXml.pyutLinkToXml(pyutLink=oglLink.pyutObject, oglLinkElement=oglLinkSubElement)

        return oglLinkSubElement

    def _oglInterface2ToXml(self, documentElement: Element, oglInterface: OglInterface2) -> Element:
        """

        Args:
            documentElement:  untangler element for document
            oglInterface:     Lollipop to serialize
        Returns:
            New untangle element
        """
        destAnchor:      SelectAnchorPoint = oglInterface.destinationAnchor
        attachmentPoint: AttachmentSide    = destAnchor.attachmentPoint
        x, y = destAnchor.GetPosition()

        attributes: ElementAttributes = ElementAttributes({
            XmlConstants.ATTR_LOLLIPOP_ATTACHMENT_POINT: attachmentPoint.__str__(),
            XmlConstants.ATTR_X:                         str(x),
            XmlConstants.ATTR_Y:                         str(y),
        })
        oglInterface2: Element = SubElement(documentElement, XmlConstants.ELEMENT_OGL_INTERFACE2, attrib=attributes)

        self._pyutToXml.pyutInterfaceToXml(oglInterface.pyutInterface, oglInterface2)
        return oglInterface2

    def _oglLinkAttributes(self, oglLink: OglLink) -> ElementAttributes:

        srcX, srcY   = oglLink.sourceAnchor.model.GetPosition()
        destX, destY = oglLink.destinationAnchor.model.GetPosition()

        attributes: ElementAttributes = ElementAttributes({
            XmlConstants.ATTR_LINK_SOURCE_ANCHOR_X:      str(srcX),
            XmlConstants.ATTR_LINK_SOURCE_ANCHOR_Y:      str(srcY),
            XmlConstants.ATTR_LINK_DESTINATION_ANCHOR_X: str(destX),
            XmlConstants.ATTR_LINK_DESTINATION_ANCHOR_Y: str(destY),
            XmlConstants.ATTR_SPLINE:                    str(oglLink.spline)   # piecewise polynomial function
        })

        return attributes
