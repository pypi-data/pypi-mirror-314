
from typing import Union

from logging import Logger
from logging import getLogger

from os import linesep as osLineSep

from xml.dom.minidom import Document
from xml.dom.minidom import Element
from xml.dom.minidom import Text

from pyutmodelv2.enumerations.PyutStereotype import PyutStereotype
from pyutmodelv2.enumerations.PyutVisibility import PyutVisibility

from pyutmodelv2.PyutLink import LinkDestination
from pyutmodelv2.PyutLink import LinkSource
from pyutmodelv2.PyutModelTypes import ClassName
from pyutmodelv2.PyutActor import PyutActor
from pyutmodelv2.PyutClass import PyutClass
from pyutmodelv2.PyutField import PyutField
from pyutmodelv2.PyutInterface import PyutInterface
from pyutmodelv2.PyutLink import PyutLink
from pyutmodelv2.PyutMethod import SourceCode
from pyutmodelv2.PyutNote import PyutNote
from pyutmodelv2.PyutParameter import PyutParameter
from pyutmodelv2.PyutSDInstance import PyutSDInstance
from pyutmodelv2.PyutSDMessage import PyutSDMessage
from pyutmodelv2.PyutText import PyutText
from pyutmodelv2.PyutUseCase import PyutUseCase

from oglio.toXmlV10.BasePyutToDom import BasePyutToDom
from oglio.toXmlV10.XmlConstants import XmlConstants


class PyutToDom(BasePyutToDom):
    """
    Serializes Pyut Models classes to DOM
    """
    # https://www.codetable.net/hex/a
    END_OF_LINE_MARKER: str = '&#xA;'

    def __init__(self):

        super().__init__()
        self.logger: Logger = getLogger(__name__)

    def pyutClassToDom(self, pyutClass: PyutClass, xmlDoc: Document) -> Element:
        """
        Exporting a PyutClass to a miniDom Element.

        Args:
            pyutClass:  The pyut class to save
            xmlDoc:     The xml document to update

        Returns:
            The new updated element
        """
        pyutClassElement: Element = xmlDoc.createElement(XmlConstants.ELEMENT_MODEL_CLASS)

        classId: int = pyutClass.id
        pyutClassElement.setAttribute(XmlConstants.ATTR_ID, str(classId))
        pyutClassElement.setAttribute(XmlConstants.ATTR_NAME, pyutClass.name)

        stereotype: PyutStereotype = pyutClass.stereotype
        if stereotype is not None:
            pyutClassElement.setAttribute(XmlConstants.ATTR_STEREOTYPE, stereotype.value)

        pyutClassElement.setAttribute(XmlConstants.ATTR_FILENAME, pyutClass.fileName)

        pyutClassElement = self._pyutClassCommonToXml(pyutClass, pyutClassElement)

        pyutClassElement.setAttribute(XmlConstants.ATTR_SHOW_METHODS, str(pyutClass.showMethods))
        pyutClassElement.setAttribute(XmlConstants.ATTR_SHOW_FIELDS, str(pyutClass.showFields))
        pyutClassElement.setAttribute(XmlConstants.ATTR_SHOW_STEREOTYPE, str(pyutClass.displayStereoType))
        pyutClassElement.setAttribute(XmlConstants.ATTR_DISPLAY_PARAMETERS, pyutClass.displayParameters.value)

        # methods
        for method in pyutClass.methods:
            pyutClassElement.appendChild(self._pyutMethodToDom(method, xmlDoc))
        # fields
        for field in pyutClass.fields:
            pyutClassElement.appendChild(self._pyutFieldToDom(field, xmlDoc))

        return pyutClassElement

    def pyutInterfaceToDom(self, pyutInterface: PyutInterface, xmlDoc: Document) -> Element:

        pyutInterfaceElement: Element = xmlDoc.createElement(XmlConstants.ELEMENT_MODEL_INTERFACE)

        classId: int = pyutInterface.id
        pyutInterfaceElement.setAttribute(XmlConstants.ATTR_ID, str(classId))
        pyutInterfaceElement.setAttribute(XmlConstants.ATTR_NAME, pyutInterface.name)

        pyutInterfaceElement = self._pyutClassCommonToXml(pyutInterface, pyutInterfaceElement)

        for method in pyutInterface.methods:
            pyutInterfaceElement.appendChild(self._pyutMethodToDom(method, xmlDoc))

        for className in pyutInterface.implementors:
            self.logger.debug(f'implementing className: {className}')
            pyutInterfaceElement.appendChild(self._pyutImplementorToDom(className, xmlDoc))

        return pyutInterfaceElement

    def pyutLinkToDom(self, pyutLink: PyutLink, xmlDoc: Document) -> Element:
        """
        Exporting a PyutLink to a miniDom Element.

        Args:
            pyutLink:   Link to save
            xmlDoc:     xml document

        Returns:
            A new minidom element
        """
        root: Element = xmlDoc.createElement(XmlConstants.ELEMENT_MODEL_LINK)

        root.setAttribute(XmlConstants.ATTR_NAME, pyutLink.name)
        root.setAttribute(XmlConstants.ATTR_TYPE, pyutLink.linkType.name)
        root.setAttribute(XmlConstants.ATTR_CARDINALITY_SOURCE, pyutLink.sourceCardinality)
        root.setAttribute(XmlConstants.ATTR_CARDINALITY_DESTINATION, pyutLink.destinationCardinality)
        root.setAttribute(XmlConstants.ATTR_BIDIRECTIONAL, str(pyutLink.bidirectional))

        srcLinkId:  int = pyutLink.source.id
        destLinkId: int = pyutLink.destination.id

        root.setAttribute(XmlConstants.ATTR_SOURCE_ID, str(srcLinkId))
        root.setAttribute(XmlConstants.ATTR_DESTINATION_ID, str(destLinkId))

        return root

    def pyutNoteToDom(self, pyutNote: PyutNote, xmlDoc: Document) -> Element:
        """
        Export a PyutNote to a miniDom Element.

        Args:
            pyutNote:   Note to convert
            xmlDoc:     xml document

        Returns:
            New miniDom element
        """
        pyutNoteElement: Element = xmlDoc.createElement(XmlConstants.ELEMENT_MODEL_NOTE)

        noteId: int = pyutNote.id
        pyutNoteElement.setAttribute(XmlConstants.ATTR_ID, str(noteId))

        content: str = pyutNote.content
        content = content.replace(osLineSep, PyutToDom.END_OF_LINE_MARKER)
        pyutNoteElement.setAttribute(XmlConstants.ATTR_CONTENT, content)

        pyutNoteElement.setAttribute(XmlConstants.ATTR_FILENAME, pyutNote.fileName)

        return pyutNoteElement

    def pyutTextToDom(self, pyutText: PyutText, xmlDoc: Document) -> Element:

        root:   Element = xmlDoc.createElement(XmlConstants.ELEMENT_MODEL_TEXT)
        textId: int     = pyutText.id

        root.setAttribute(XmlConstants.ATTR_ID, str(textId))
        content: str = pyutText.content
        content = content.replace(osLineSep, PyutToDom.END_OF_LINE_MARKER)

        root.setAttribute(XmlConstants.ATTR_CONTENT, content)

        return root

    def pyutUseCaseToDom(self, pyutUseCase: PyutUseCase, xmlDoc: Document) -> Element:
        """
        Export a PyutUseCase to a minidom Element.

        Args:
            pyutUseCase:    Use case to convert
            xmlDoc:         xml document

        Returns:
            A new minidom element
        """
        pyutUseCaseElement: Element = xmlDoc.createElement(XmlConstants.ELEMENT_MODEL_USE_CASE)

        useCaseId = pyutUseCase.id
        pyutUseCaseElement.setAttribute(XmlConstants.ATTR_ID, str(useCaseId))
        pyutUseCaseElement.setAttribute(XmlConstants.ATTR_NAME, pyutUseCase.name)
        pyutUseCaseElement.setAttribute(XmlConstants.ATTR_FILENAME, pyutUseCase.fileName)

        return pyutUseCaseElement

    def pyutActorToDom(self, pyutActor: PyutActor, xmlDoc: Document) -> Element:
        """
        Export an PyutActor to a minidom Element.
        Args:
            pyutActor:  Actor to convert
            xmlDoc:     xml document

        Returns:
            A new minidom element
        """
        pyutActorElement: Element = xmlDoc.createElement(XmlConstants.ELEMENT_MODEL_ACTOR)

        actorId = pyutActor.id
        pyutActorElement.setAttribute(XmlConstants.ATTR_ID, str(actorId))
        pyutActorElement.setAttribute(XmlConstants.ATTR_NAME, pyutActor.name)
        pyutActorElement.setAttribute(XmlConstants.ATTR_FILENAME, pyutActor.fileName)

        return pyutActorElement

    def pyutSDInstanceToDom(self, pyutSDInstance: PyutSDInstance, xmlDoc: Document) -> Element:
        """
        Exporting a PyutSDInstance to a minidom Element.

        Args:
            pyutSDInstance:     Class to convert
            xmlDoc:             xml document

        Returns:
            A new minidom element
        """
        root:  Element = xmlDoc.createElement(XmlConstants.ELEMENT_MODEL_SD_INSTANCE)
        eltId: int     = pyutSDInstance.id
        # eltId: int = pyutSDInstance.id
        root.setAttribute(XmlConstants.ATTR_ID, str(eltId))
        root.setAttribute(XmlConstants.ATTR_INSTANCE_NAME, pyutSDInstance.instanceName)
        root.setAttribute(XmlConstants.ATTR_LIFE_LINE_LENGTH, str(pyutSDInstance.instanceLifeLineLength))

        return root

    def pyutSDMessageToDom(self, pyutSDMessage: PyutSDMessage, xmlDoc: Document) -> Element:
        """
        Exporting a PyutSDMessage to an minidom Element.
        Args:
            pyutSDMessage:  SDMessage to export
            xmlDoc:         xml document

        Returns:
            A new minidom element
        """
        root: Element = xmlDoc.createElement(XmlConstants.ELEMENT_MODEL_SD_MESSAGE)

        eltId: int = pyutSDMessage.id
        # eltId: int = pyutSDMessage.id
        root.setAttribute(XmlConstants.ATTR_ID, str(eltId))

        # message
        root.setAttribute(XmlConstants.ATTR_MESSAGE, pyutSDMessage.message)

        # time
        srcInstance: LinkSource      = pyutSDMessage.source
        dstInstance: LinkDestination = pyutSDMessage.destination

        idSrc: int = srcInstance.id
        idDst: int = dstInstance.id

        root.setAttribute(XmlConstants.ATTR_SOURCE_TIME_LINE, str(pyutSDMessage.sourceY))
        root.setAttribute(XmlConstants.ATTR_DESTINATION_TIME_LINE, str(pyutSDMessage.destinationY))
        root.setAttribute(XmlConstants.ATTR_SD_MESSAGE_SOURCE_ID, str(idSrc))
        root.setAttribute(XmlConstants.ATTR_SD_MESSAGE_DESTINATION_ID, str(idDst))

        return root

    def _pyutMethodToDom(self, pyutMethod, xmlDoc) -> Element:
        """
        Exporting a PyutMethod to a miniDom Element

        Args:
            pyutMethod: Method to save
            xmlDoc:     xml document

        Returns:
            The new updated element
        """
        pyutMethodElement: Element = xmlDoc.createElement(XmlConstants.ELEMENT_MODEL_METHOD)

        pyutMethodElement.setAttribute(XmlConstants.ATTR_NAME, pyutMethod.name)

        visibility: PyutVisibility = pyutMethod.visibility
        visName:    str            = self.__safeVisibilityToName(visibility)

        if visibility is not None:
            pyutMethodElement.setAttribute(XmlConstants.ATTR_VISIBILITY, visName)

        for modifier in pyutMethod.modifiers:
            xmlModifier: Element = xmlDoc.createElement(XmlConstants.ELEMENT_MODEL_MODIFIER)
            xmlModifier.setAttribute(XmlConstants.ATTR_NAME, modifier.name)
            pyutMethodElement.appendChild(xmlModifier)

        if pyutMethod.returnType is not None:
            xmlReturnType: Element = xmlDoc.createElement(XmlConstants.ELEMENT_MODEL_RETURN)
            xmlReturnType.setAttribute(XmlConstants.ATTR_TYPE, str(pyutMethod.returnType))
            pyutMethodElement.appendChild(xmlReturnType)

        for param in pyutMethod.parameters:
            pyutMethodElement.appendChild(self._pyutParamToDom(param, xmlDoc))

        codeRoot: Element = self._pyutSourceCodeToDom(pyutMethod.sourceCode, xmlDoc)
        pyutMethodElement.appendChild(codeRoot)
        return pyutMethodElement

    def _pyutFieldToDom(self, pyutField: PyutField, xmlDoc: Document) -> Element:
        """
        Export a PyutField to a miniDom Element
        Args:
            pyutField:  The PyutField to save
            xmlDoc:     The xml document to update

        Returns:
            The new updated element
        """
        pyutFieldElement: Element = xmlDoc.createElement(XmlConstants.ELEMENT_MODEL_FIELD)

        pyutFieldElement.appendChild(self._pyutParamToDom(pyutField, xmlDoc))
        visibility: PyutVisibility = pyutField.visibility
        visName:    str            = self.__safeVisibilityToName(visibility)
        pyutFieldElement.setAttribute(XmlConstants.ATTR_VISIBILITY, visName)

        return pyutFieldElement

    def _pyutParamToDom(self, pyutParam: PyutParameter, xmlDoc: Document) -> Element:
        """
        Export a PyutParam to a miniDom Element

        Args:
            pyutParam:  Parameter to save
            xmlDoc:     XML Node

        Returns:
            The new updated element
        """
        pyutParameterElement: Element = xmlDoc.createElement(XmlConstants.ELEMENT_MODEL_PARAM)

        pyutParameterElement.setAttribute(XmlConstants.ATTR_NAME, pyutParam.name)
        pyutParameterElement.setAttribute(XmlConstants.ATTR_TYPE, str(pyutParam.type))

        defaultValue = pyutParam.defaultValue
        if defaultValue is not None:
            pyutParameterElement.setAttribute(XmlConstants.ATTR_DEFAULT_VALUE, defaultValue)

        return pyutParameterElement

    def _pyutSourceCodeToDom(self, sourceCode: SourceCode, xmlDoc: Document) -> Element:

        codeRoot: Element = xmlDoc.createElement(XmlConstants.ELEMENT_MODEL_SOURCE_CODE)
        for code in sourceCode:
            codeElement:  Element = xmlDoc.createElement(XmlConstants.ELEMENT_MODEL_CODE)
            textCodeNode: Text    = xmlDoc.createTextNode(code)
            codeElement.appendChild(textCodeNode)
            codeRoot.appendChild(codeElement)

        return codeRoot

    def _pyutImplementorToDom(self, className: ClassName, xmlDoc: Document) -> Element:

        root: Element = xmlDoc.createElement(XmlConstants.ELEMENT_IMPLEMENTOR)

        root.setAttribute(XmlConstants.ATTR_IMPLEMENTING_CLASS_NAME, className)

        return root

    def __safeVisibilityToName(self, visibility: Union[str, PyutVisibility]) -> str:
        """
        Account for old pre V10 code
        Args:
            visibility:

        Returns:
            The visibility name
        """

        if isinstance(visibility, str):
            visStr: str = PyutVisibility.toEnum(visibility).name
        else:
            visStr = visibility.name

        return visStr
