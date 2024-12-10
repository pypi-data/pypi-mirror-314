
from logging import Logger
from logging import getLogger

from xml.dom.minidom import Document
from xml.dom.minidom import Element

from codeallyadvanced.ui.AttachmentSide import AttachmentSide

from miniogl.SelectAnchorPoint import SelectAnchorPoint

from ogl.OglAssociation import OglAssociation
from ogl.OglAssociationLabel import OglAssociationLabel
from ogl.OglInterface2 import OglInterface2
from ogl.OglLink import OglLink

from oglio.Types import OglLinks
from oglio.toXmlV10.BaseOglToDom import BaseOglToDom
from oglio.toXmlV10.PyutToDom import PyutToDom
from oglio.toXmlV10.XmlConstants import XmlConstants


class OglLinksToDom(BaseOglToDom):

    def __init__(self, xmlDocument: Document):

        super().__init__(xmlDocument=xmlDocument)
        self.linksLogger: Logger = getLogger(__name__)

        self._pyutToMiniDom: PyutToDom = PyutToDom()

    def serialize(self, documentNode: Element, oglLinks: OglLinks) -> Element:

        for oglLink in oglLinks:
            if isinstance(oglLink, OglInterface2):
                lollipopElement: Element = self._oglInterface2ToDom(oglLink, self._xmlDocument)
                documentNode.appendChild(lollipopElement)
            else:
                linkElement: Element = self._oglLinkToDom(oglLink=oglLink, xmlDoc=self._xmlDocument)
                documentNode.appendChild(linkElement)

        return documentNode

    def _oglInterface2ToDom(self, oglInterface: OglInterface2, xmlDoc: Document) -> Element:
        """

        Args:
            oglInterface:   Lollipop to convert
            xmlDoc:         xml document

        Returns:
            New minidom element
        """
        root: Element = xmlDoc.createElement(XmlConstants.ELEMENT_GRAPHIC_LOLLIPOP)

        destAnchor:      SelectAnchorPoint = oglInterface.destinationAnchor
        attachmentPoint: AttachmentSide   = destAnchor.attachmentPoint
        x, y = destAnchor.GetPosition()

        root.setAttribute(XmlConstants.ATTR_LOLLIPOP_ATTACHMENT_POINT, attachmentPoint.__str__())
        root.setAttribute(XmlConstants.ATTR_X, str(x))
        root.setAttribute(XmlConstants.ATTR_Y, str(y))

        # parentUmlClass: OglClass = destAnchor.GetParent()
        # parentId:       int      = self._idFactory.getID(parentUmlClass.getPyutObject())
        # self.logger.info(f'Interface implemented by class id: {parentId}')

        # root.setAttribute(PyutXmlConstants.ATTR_IMPLEMENTED_BY_CLASS_ID, str(parentId))
        root.appendChild(self._pyutToMiniDom.pyutInterfaceToDom(oglInterface.pyutInterface, xmlDoc))

        return root

    def _oglLinkToDom(self, oglLink: OglLink, xmlDoc: Document):
        """
        Export an OgLink to a minidom element
        Args:
            oglLink:    OglLink to convert
            xmlDoc:     xml document

        Returns:
            A new minidom element
        """
        root = xmlDoc.createElement(XmlConstants.ELEMENT_GRAPHIC_LINK)

        # save source and destination anchor points
        x, y = oglLink.sourceAnchor.model.GetPosition()
        simpleX, simpleY = self._getSimpleCoordinates(x, y)
        root.setAttribute(XmlConstants.ATTR_LINK_SOURCE_ANCHOR_X, simpleX)
        root.setAttribute(XmlConstants.ATTR_LINK_SOURCE_ANCHOR_Y, simpleY)

        x, y = oglLink.destinationAnchor.model.GetPosition()
        simpleX, simpleY = self._getSimpleCoordinates(x, y)

        root.setAttribute(XmlConstants.ATTR_LINK_DESTINATION_ANCHOR_X, simpleX)
        root.setAttribute(XmlConstants.ATTR_LINK_DESTINATION_ANCHOR_Y, simpleY)

        root.setAttribute(XmlConstants.ATTR_SPLINE, str(oglLink.spline))

        if isinstance(oglLink, OglAssociation):

            center: OglAssociationLabel = oglLink.centerLabel
            src:    OglAssociationLabel = oglLink.sourceCardinality
            dst:    OglAssociationLabel = oglLink.destinationCardinality

            assocLabels = {
                XmlConstants.ELEMENT_ASSOC_CENTER_LABEL:      center,
                XmlConstants.ELEMENT_ASSOC_SOURCE_LABEL:      src,
                XmlConstants.ELEMENT_ASSOC_DESTINATION_LABEL: dst
            }
            for eltName in assocLabels:
                elt: Element = self._createAssocLabelElement(eltName, xmlDoc, assocLabels[eltName])
                root.appendChild(elt)

        # save control points (not anchors!)
        for x, y in oglLink.segments[1:-1]:
            item = xmlDoc.createElement(XmlConstants.ELEMENT_MODEL_CONTROL_POINT)
            item.setAttribute(XmlConstants.ATTR_X, str(x))
            item.setAttribute(XmlConstants.ATTR_Y, str(y))
            root.appendChild(item)

        # adding the data layer object

        root.appendChild(self._pyutToMiniDom.pyutLinkToDom(oglLink.pyutObject, xmlDoc))

        return root

    # noinspection SpellCheckingInspection
    def _createAssocLabelElement(self, eltText: str, xmlDoc: Document, oglLabel: OglAssociationLabel) -> Element:
        """
        Creates an element of the form:

        ```html
        `<eltText x="nnnn" y="nnnn"/>`
        ```

        e.g.

        ```html
            `<LabelCenter x="1811" y="1137"/>`
        ```

        Args:
            eltText:    The element name
            xmlDoc:     The minidom document
            oglLabel:   A description of a label includes text and position

        Returns:
            A new minidom element
        """
        label: Element = xmlDoc.createElement(eltText)

        x, y = oglLabel.GetPosition()

        relativeX, relativeY = oglLabel.ConvertCoordToRelative(x=x, y=y)
        self.linksLogger.debug(f'x,y = ({x},{y})   relativeX,relativeY = ({relativeX},{relativeY})')
        label.setAttribute(XmlConstants.ATTR_X, str(relativeX))
        label.setAttribute(XmlConstants.ATTR_Y, str(relativeY))

        return label
