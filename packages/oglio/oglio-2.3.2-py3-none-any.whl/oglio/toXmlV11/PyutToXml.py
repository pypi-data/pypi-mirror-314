
from logging import Logger
from logging import getLogger

from os import linesep as osLineSep

from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement

from pyutmodelv2.PyutLink import LinkDestination
from pyutmodelv2.PyutLink import LinkSource
from pyutmodelv2.PyutLink import PyutLink

from pyutmodelv2.PyutModelTypes import ClassName
from pyutmodelv2.PyutActor import PyutActor
from pyutmodelv2.PyutClass import PyutClass
from pyutmodelv2.PyutClassCommon import PyutClassCommon
from pyutmodelv2.PyutField import PyutField
from pyutmodelv2.PyutInterface import PyutInterface
from pyutmodelv2.PyutMethod import PyutMethod
from pyutmodelv2.PyutMethod import SourceCode
from pyutmodelv2.PyutNote import PyutNote
from pyutmodelv2.PyutParameter import PyutParameter
from pyutmodelv2.PyutSDInstance import PyutSDInstance
from pyutmodelv2.PyutSDMessage import PyutSDMessage
from pyutmodelv2.PyutText import PyutText
from pyutmodelv2.PyutUseCase import PyutUseCase

from oglio.toXmlV11.InternalTypes import ElementAttributes
from oglio.toXmlV11.XmlConstants import XmlConstants


class PyutToXml:
    """
    Serializes Pyut Models classes to DOM
    """
    # https://www.codetable.net/hex/a
    END_OF_LINE_MARKER: str = '&#xA;'

    def __init__(self):
        super().__init__()
        self.logger: Logger = getLogger(__name__)

    def pyutClassToXml(self, pyutClass: PyutClass, graphicElement: Element) -> Element:
        """
        Exporting a PyutClass to a miniDom Element.

        Args:
            pyutClass:       The pyut class to save
            graphicElement:  The xml element to update

        Returns:
            A new updated element
        """

        commonAttributes = self._pyutClassCommonAttributes(pyutClass)
        attributes = {
            XmlConstants.ATTR_ID:                     str(pyutClass.id),
            XmlConstants.ATTR_NAME:                   pyutClass.name,
            XmlConstants.ATTR_STEREOTYPE:             pyutClass.stereotype.value,
            XmlConstants.ATTR_DISPLAY_METHODS:        str(pyutClass.showMethods),
            XmlConstants.ATTR_DISPLAY_PARAMETERS:     pyutClass.displayParameters.value,
            XmlConstants.ATTR_DISPLAY_CONSTRUCTOR:    pyutClass.displayConstructor.value,
            XmlConstants.ATTR_DISPLAY_DUNDER_METHODS: pyutClass.displayDunderMethods.value,
            XmlConstants.ATTR_DISPLAY_FIELDS:         str(pyutClass.showFields),
            XmlConstants.ATTR_DISPLAY_STEREOTYPE:     str(pyutClass.displayStereoType),
            XmlConstants.ATTR_FILENAME:               pyutClass.fileName,
        }

        attributes = attributes | commonAttributes

        pyutClassElement: Element = SubElement(graphicElement, XmlConstants.ELEMENT_PYUT_CLASS, attrib=attributes)

        for method in pyutClass.methods:
            self._pyutMethodToXml(pyutMethod=method, pyutClassElement=pyutClassElement)

        for pyutField in pyutClass.fields:
            self._pyutFieldToXml(pyutField=pyutField, pyutClassElement=pyutClassElement)
        return pyutClassElement

    def pyutLinkToXml(self, pyutLink: PyutLink, oglLinkElement: Element) -> Element:
        """
        Exporting a PyutLink to an Element.

        Args:
            pyutLink:   Link to save
            oglLinkElement:     xml document

        Returns:
            A new minidom element
        """
        # src   = pyutLink.getSource()
        # dst   = pyutLink.getDestination()
        src: LinkSource      = pyutLink.source
        dst: LinkDestination = pyutLink.destination

        srcLinkId:  int = src.id
        destLinkId: int = dst.id

        attributes: ElementAttributes = ElementAttributes({
            XmlConstants.ATTR_NAME:                    pyutLink.name,
            XmlConstants.ATTR_TYPE:                    pyutLink.linkType.name,
            XmlConstants.ATTR_CARDINALITY_SOURCE:      pyutLink.sourceCardinality,
            XmlConstants.ATTR_CARDINALITY_DESTINATION: pyutLink.destinationCardinality,
            # XmlConstants.ATTR_BIDIRECTIONAL:           str(pyutLink.getBidir()),
            XmlConstants.ATTR_BIDIRECTIONAL:           str(pyutLink.bidirectional),
            XmlConstants.ATTR_SOURCE_ID:               str(srcLinkId),
            XmlConstants.ATTR_DESTINATION_ID:          str(destLinkId),
        })
        pyutLinkElement: Element = SubElement(oglLinkElement, XmlConstants.ELEMENT_PYUT_LINK, attrib=attributes)

        return pyutLinkElement

    def pyutInterfaceToXml(self, pyutInterface: PyutInterface, interface2Element: Element) -> Element:

        classId: int = pyutInterface.id

        attributes: ElementAttributes = ElementAttributes({
            XmlConstants.ATTR_ID:          str(classId),
            XmlConstants.ATTR_NAME:        pyutInterface.name,
            XmlConstants.ATTR_DESCRIPTION: pyutInterface.description
        })
        pyutInterfaceElement: Element = SubElement(interface2Element, XmlConstants.ELEMENT_MODEL_INTERFACE, attrib=attributes)

        for method in pyutInterface.methods:
            self._pyutMethodToXml(pyutMethod=method, pyutClassElement=pyutInterfaceElement)

        for className in pyutInterface.implementors:
            self.logger.debug(f'implementing className: {className}')
            self._pyutImplementorToXml(className, pyutInterfaceElement)

        return pyutInterfaceElement

    def pyutNoteToXml(self, pyutNote: PyutNote, oglNoteElement: Element) -> Element:

        noteId:       int = pyutNote.id
        content:      str = pyutNote.content
        fixedContent: str  = content.replace(osLineSep, PyutToXml.END_OF_LINE_MARKER)
        if pyutNote.fileName is None:
            pyutNote.fileName = ''

        attributes: ElementAttributes = ElementAttributes({
            XmlConstants.ATTR_ID:       str(noteId),
            XmlConstants.ATTR_CONTENT:  fixedContent,
            XmlConstants.ATTR_FILENAME: pyutNote.fileName,
        })
        pyutNoteElement: Element = SubElement(oglNoteElement, XmlConstants.ELEMENT_PYUT_NOTE, attrib=attributes)

        return pyutNoteElement

    def pyutTextToXml(self, pyutText: PyutText, oglTextElement: Element) -> Element:

        textId:       int = pyutText.id
        content:      str = pyutText.content
        fixedContent: str  = content.replace(osLineSep, PyutToXml.END_OF_LINE_MARKER)

        attributes: ElementAttributes = ElementAttributes({
            XmlConstants.ATTR_ID:       str(textId),
            XmlConstants.ATTR_CONTENT:  fixedContent,
        })
        pyutTextElement: Element = SubElement(oglTextElement, XmlConstants.ELEMENT_PYUT_TEXT, attrib=attributes)

        return pyutTextElement

    def pyutActorToXml(self, pyutActor: PyutActor, oglActorElement: Element) -> Element:

        actorId:  int = pyutActor.id
        fileName: str = pyutActor.fileName
        if fileName is None:
            fileName = ''

        attributes: ElementAttributes = ElementAttributes({
            XmlConstants.ATTR_ID:       str(actorId),
            XmlConstants.ATTR_NAME:     pyutActor.name,
            XmlConstants.ATTR_FILENAME: fileName,
        })
        pyutActorElement: Element = SubElement(oglActorElement, XmlConstants.ELEMENT_PYUT_ACTOR, attributes)

        return pyutActorElement

    def pyutUseCaseToXml(self, pyutUseCase: PyutUseCase, oglUseCaseElement: Element) -> Element:

        useCaseId: int = pyutUseCase.id
        fileName:  str = pyutUseCase.fileName
        if fileName is None:
            fileName = ''

        attributes: ElementAttributes = ElementAttributes({
            XmlConstants.ATTR_ID:       str(useCaseId),
            XmlConstants.ATTR_NAME:     pyutUseCase.name,
            XmlConstants.ATTR_FILENAME: fileName
        })
        pyutUseCaseElement: Element = SubElement(oglUseCaseElement, XmlConstants.ELEMENT_PYUT_USE_CASE, attributes)

        return pyutUseCaseElement

    def pyutSDInstanceToXml(self, pyutSDInstance: PyutSDInstance, oglSDInstanceElement: Element) -> Element:

        sdInstanceId: int = pyutSDInstance.id

        attributes: ElementAttributes = ElementAttributes({
            XmlConstants.ATTR_ID:               str(sdInstanceId),
            XmlConstants.ATTR_INSTANCE_NAME:    pyutSDInstance.instanceName,
            XmlConstants.ATTR_LIFE_LINE_LENGTH: str(pyutSDInstance.instanceLifeLineLength),
        })

        pyutSDInstanceElement: Element = SubElement(oglSDInstanceElement, XmlConstants.ELEMENT_PYUT_SD_INSTANCE, attrib=attributes)

        return pyutSDInstanceElement

    def pyutSDMessageToXml(self, pyutSDMessage: PyutSDMessage, oglSDMessageElement: Element) -> Element:

        sdMessageId: int = pyutSDMessage.id

        # srcInstance: PyutSDInstance = pyutSDMessage.getSource()
        # dstInstance: PyutSDInstance = pyutSDMessage.getDestination()
        srcInstance: LinkSource      = pyutSDMessage.source
        dstInstance: LinkDestination = pyutSDMessage.destination

        idSrc: int = srcInstance.id
        idDst: int = dstInstance.id

        attributes: ElementAttributes = ElementAttributes({
            XmlConstants.ATTR_ID:                        str(sdMessageId),
            XmlConstants.ATTR_MESSAGE:                   pyutSDMessage.message,
            XmlConstants.ATTR_SOURCE_TIME:               str(pyutSDMessage.sourceY),
            XmlConstants.ATTR_DESTINATION_TIME:          str(pyutSDMessage.destinationY),
            XmlConstants.ATTR_SD_MESSAGE_SOURCE_ID:      str(idSrc),
            XmlConstants.ATTR_SD_MESSAGE_DESTINATION_ID: str(idDst),
        })

        pyutSDMessageElement: Element = SubElement(oglSDMessageElement, XmlConstants.ELEMENT_PYUT_SD_MESSAGE, attrib=attributes)

        return pyutSDMessageElement

    def _pyutMethodToXml(self, pyutMethod: PyutMethod, pyutClassElement: Element) -> Element:
        """
        Exporting a PyutMethod to an Element

        Args:
            pyutMethod:        Method to serialize
            pyutClassElement:  xml document

        Returns:
            The new updated element
        """
        attributes = {
            XmlConstants.ATTR_NAME:               pyutMethod.name,
            XmlConstants.ATTR_VISIBILITY:         pyutMethod.visibility.name,
            XmlConstants.ATTR_METHOD_RETURN_TYPE: pyutMethod.returnType.value,
        }
        pyutMethodElement: Element = SubElement(pyutClassElement, XmlConstants.ELEMENT_PYUT_METHOD, attrib=attributes)
        for modifier in pyutMethod.modifiers:
            attributes = {
                XmlConstants.ATTR_NAME: modifier.name,
            }
            SubElement(pyutMethodElement, XmlConstants.ELEMENT_MODEL_MODIFIER, attrib=attributes)
        self._pyutSourceCodeToXml(pyutMethod.sourceCode, pyutMethodElement)

        for pyutParameter in pyutMethod.parameters:
            self._pyutParameterToXml(pyutParameter, pyutMethodElement)
        # pyutMethodElement: Element = xmlDoc.createElement(XmlConstants.ELEMENT_MODEL_METHOD)
        #
        # pyutMethodElement.setAttribute(XmlConstants.ATTR_NAME, pyutMethod.name)
        #
        # visibility: PyutVisibilityEnum = pyutMethod.getVisibility()
        # visName:    str                = self.__safeVisibilityToName(visibility)
        #
        # if visibility is not None:
        #     pyutMethodElement.setAttribute(XmlConstants.ATTR_VISIBILITY, visName)
        #
        # for modifier in pyutMethod.modifiers:
        #     xmlModifier: Element = xmlDoc.createElement(XmlConstants.ELEMENT_MODEL_MODIFIER)
        #     xmlModifier.setAttribute(XmlConstants.ATTR_NAME, modifier.name)
        #     pyutMethodElement.appendChild(xmlModifier)
        #
        # if pyutMethod.returnType is not None:
        #     xmlReturnType: Element = xmlDoc.createElement(XmlConstants.ELEMENT_MODEL_RETURN)
        #     xmlReturnType.setAttribute(XmlConstants.ATTR_TYPE, str(pyutMethod.returnType))
        #     pyutMethodElement.appendChild(xmlReturnType)
        #
        # for param in pyutMethod.parameters:
        #     pyutMethodElement.appendChild(self._pyutParamToDom(param, xmlDoc))
        #
        # codeRoot: Element = self._pyutSourceCodeToDom(pyutMethod.sourceCode, xmlDoc)
        # pyutMethodElement.appendChild(codeRoot)
        # return pyutMethodElement
        return pyutMethodElement

    def _pyutClassCommonAttributes(self, classCommon: PyutClassCommon):

        attributes = {
            XmlConstants.ATTR_DESCRIPTION: classCommon.description
        }
        return attributes

    def _pyutSourceCodeToXml(self, sourceCode: SourceCode, pyutMethodElement: Element):

        codeRoot: Element = SubElement(pyutMethodElement, XmlConstants.ELEMENT_MODEL_SOURCE_CODE)

        for code in sourceCode:
            codeElement: Element = SubElement(codeRoot, XmlConstants.ELEMENT_MODEL_CODE)
            codeElement.text = code

        return codeRoot

    def _pyutParameterToXml(self, pyutParameter: PyutParameter, pyutMethodElement: Element) -> Element:

        attributes = {
            XmlConstants.ATTR_NAME:          pyutParameter.name,
            XmlConstants.ATTR_TYPE:          pyutParameter.type.value,
            # XmlConstants.ATTR_DEFAULT_VALUE: pyutParameter.defaultValue,
        }

        defaultValue = pyutParameter.defaultValue
        if defaultValue is not None:
            attributes[XmlConstants.ATTR_DEFAULT_VALUE] = pyutParameter.defaultValue

        pyutParameterElement: Element = SubElement(pyutMethodElement, XmlConstants.ELEMENT_MODEL_PYUT_PARAMETER, attrib=attributes)

        return pyutParameterElement

    def _pyutFieldToXml(self, pyutField: PyutField, pyutClassElement: Element) -> Element:
        """
        Serialize a PyutField to an Element

        Args:
            pyutField:         The PyutField to serialize
            pyutClassElement: The Pyut Class element to update

        Returns:
            The new updated element
        """
        attributes = {
            XmlConstants.ATTR_NAME:          pyutField.name,
            XmlConstants.ATTR_VISIBILITY:    pyutField.visibility.name,
            XmlConstants.ATTR_TYPE:          pyutField.type.value,
            XmlConstants.ATTR_DEFAULT_VALUE: pyutField.defaultValue,
        }
        pyutFieldElement: Element = SubElement(pyutClassElement, XmlConstants.ELEMENT_MODEL_PYUT_FIELD, attrib=attributes)

        return pyutFieldElement

    def _pyutImplementorToXml(self, className: ClassName, xmlDoc: Element) -> Element:

        # root: Element = xmlDoc.createElement(XmlConstants.ELEMENT_IMPLEMENTOR)
        # root.setAttribute()
        attributes: ElementAttributes = ElementAttributes({
            XmlConstants.ATTR_IMPLEMENTING_CLASS_NAME: className,
        })
        implementorElement: Element = SubElement(xmlDoc, XmlConstants.ELEMENT_IMPLEMENTOR, attrib=attributes)
        return implementorElement
