
from logging import Logger
from logging import getLogger

from zlib import compress
from zlib import ZLIB_VERSION

from oglio.Types import OglProject

from oglio.toXmlV11.OglToXml import OglToXml


class Writer:
    """
    A shim on top of the OGL serialization layer;
    Allowed me to replace
    the heavy-duty Python core xml minidom implementation
    with Python Xml Element Tree

    The write only writes the latest XML version
    """

    def __init__(self):

        self.logger: Logger = getLogger(__name__)

    def writeFile(self, oglProject: OglProject, fqFileName: str):
        """
        Writes to a compressed Pyut file

        Args:
            oglProject:     The project we have to serialize
            fqFileName:     Where to write the XML;  Should be a full qualified file name
        """
        if fqFileName.endswith('.put') is False:
            fqFileName = f'{fqFileName}.put'

        oglToXml: OglToXml = OglToXml(projectCodePath=oglProject.codePath)

        for oglDocument in oglProject.oglDocuments.values():
            oglToXml.serialize(oglDocument=oglDocument)

        rawXml: str = oglToXml.xml

        self.logger.info(f'{ZLIB_VERSION=}')
        byteText:        bytes  = rawXml.encode()
        compressedBytes: bytes = compress(byteText)

        with open(fqFileName, "wb") as binaryIO:
            binaryIO.write(compressedBytes)

    def writeXmlFile(self, oglProject: OglProject, fqFileName: str, prettyXml: bool = True):
        """
        Writes to an XML file
        Args:
            oglProject:     The project we have to serialize
            fqFileName:     Where to write the XML;  Should be a full qualified file name
            prettyXml:      Format it or not?
        """
        if fqFileName.endswith('.xml') is False:
            fqFileName = f'{fqFileName}.xml'

        oglToXml: OglToXml = OglToXml(projectCodePath=oglProject.codePath)

        for oglDocument in oglProject.oglDocuments.values():
            oglToXml.serialize(oglDocument=oglDocument)

        oglToXml.writeXml(fqFileName=fqFileName)
