
from typing import cast

from logging import Logger
from logging import getLogger

from zlib import decompress
from zlib import ZLIB_VERSION

from untanglepyut.Types import Documents
from untanglepyut.Types import ProjectInformation

from untanglepyut.UnTangleProjectInformation import UnTangleProjectInformation

from untanglepyut.UnTangler import UnTangler
from untanglepyut.XmlVersion import XmlVersion

from oglio.Types import OglActors
from oglio.Types import OglClasses
from oglio.Types import OglDocument
from oglio.Types import OglLinks
from oglio.Types import OglNotes
from oglio.Types import OglProject
from oglio.Types import OglTexts
from oglio.Types import OglUseCases
from oglio.Types import OglSDInstances
from oglio.Types import OglSDMessages

from oglio.UnsupportedFileTypeException import UnsupportedFileTypeException
from oglio.UnsupportedVersion import UnsupportedVersion


class Reader:
    """
    This is a simple translation layer on top of the PyutUntangler library.  This
    layer simply hides that implementation detail and provides a more usable
    interface to Pyut.  Additionally, it serves as a common piece of code
    that allows and IOPlugin implementations
    See https://github.com/hasii2011/pyutplugincore
    """
    def __init__(self):

        self.logger: Logger = getLogger(__name__)

    def readFile(self, fqFileName: str) -> OglProject:
        """
        Parse the input .put file

        Args:
            fqFileName: The fully qualified file name
        """
        if fqFileName.endswith('.put') is False:
            raise UnsupportedFileTypeException(message=f'File does not end with .put suffix')

        rawXmlString:       str                = self._decompressFile(fqFileName=fqFileName)
        projectInformation: ProjectInformation = self._extractProjectInformation(fqFileName)

        if projectInformation.version == XmlVersion.V10.value:
            untangler: UnTangler = UnTangler(xmlVersion=XmlVersion.V10)
        else:
            untangler = UnTangler(xmlVersion=XmlVersion.V11)

        untangler.untangleXml(xmlString=rawXmlString, fqFileName=fqFileName)

        oglProject: OglProject = self._makeOglProject(untangler=untangler)

        return oglProject

    def readXmlFile(self, fqFileName: str) -> OglProject:
        """
        Parse the input XML file;

        Args:
            fqFileName: Fully qualified file name
        """
        if fqFileName.endswith('.xml') is False:
            raise UnsupportedFileTypeException(message=f'File does not end with .xml suffix')

        projectInformation: ProjectInformation = self._extractProjectInformation(fqFileName)

        if projectInformation.version == '10':
            untangler: UnTangler = UnTangler(xmlVersion=XmlVersion.V10)
        elif projectInformation.version == '11':
            untangler = UnTangler(xmlVersion=XmlVersion.V11)
        else:
            raise UnsupportedVersion(message=f'Unsupported version: {projectInformation.version}')

        untangler.untangleFile(fqFileName=fqFileName)

        oglProject: OglProject = self._makeOglProject(untangler=untangler)

        return oglProject

    def _decompressFile(self, fqFileName: str) -> str:
        """
        Decompresses a previously Pyut compressed file
        Args:
            fqFileName: Fully qualified file name with a .put suffix

        Returns:  A raw XML String
        """
        try:
            with open(fqFileName, "rb") as compressedFile:
                compressedData: bytes = compressedFile.read()
        except (ValueError, Exception) as e:
            self.logger.error(f'decompress open:  {e}')
            raise e
        else:
            self.logger.info(f'{ZLIB_VERSION=}')
            xmlBytes:  bytes = decompress(compressedData)  # has b'....' around it
            xmlString: str   = xmlBytes.decode()
            self.logger.debug(f'Document read:\n{xmlString}')

        return xmlString

    def _makeOglProject(self, untangler: UnTangler) -> OglProject:
        """
        Syntactic sugar

        Args:
            untangler:

        Returns:  A populated  OglProject
        """
        oglProject: OglProject = OglProject()

        oglProject.toOglProject(untangler.projectInformation)

        assert oglProject.version == XmlVersion.V10.value or oglProject.version == XmlVersion.V11.value, 'We have mismatched XML versions'
        documents: Documents = untangler.documents
        for document in documents.values():
            self.logger.debug(f'Untangled - {document.documentTitle}')
            oglDocument: OglDocument = OglDocument()
            oglDocument.toOglDocument(document)
            #
            # Cheat by just type casting
            #
            oglDocument.oglClasses  = cast(OglClasses,  document.oglClasses)
            oglDocument.oglLinks    = cast(OglLinks,    document.oglLinks)
            oglDocument.oglNotes    = cast(OglNotes,    document.oglNotes)
            oglDocument.oglTexts    = cast(OglTexts,    document.oglTexts)
            oglDocument.oglActors   = cast(OglActors,   document.oglActors)
            oglDocument.oglUseCases = cast(OglUseCases, document.oglUseCases)
            oglDocument.oglSDInstances = cast(OglSDInstances, document.oglSDInstances)
            oglDocument.oglSDMessages  = cast(OglSDMessages,  document.oglSDMessages)

            self.logger.debug(f'OglDocument - {oglDocument}')
            oglProject.oglDocuments[oglDocument.documentTitle] = oglDocument

        return oglProject

    def _extractProjectInformation(self, fqFileName: str) -> ProjectInformation:

        unTangleProjectInformation: UnTangleProjectInformation = UnTangleProjectInformation(fqFileName=fqFileName)

        return unTangleProjectInformation.projectInformation
