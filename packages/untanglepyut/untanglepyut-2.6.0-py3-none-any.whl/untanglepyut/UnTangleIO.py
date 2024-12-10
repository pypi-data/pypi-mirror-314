
from logging import Logger
from logging import getLogger

from zlib import decompress
from zlib import ZLIB_VERSION


class UnTangleIO:
    def __init__(self):
        self.ioLogger: Logger = getLogger(__name__)

    def getRawXml(self, fqFileName: str) -> str:
        """
        method to read a file.  Assumes the file has XML.
        No check is done to verify this
        Args:
            fqFileName: The file to read

        Returns:  The contents of the file
        """
        try:
            with open(fqFileName, "r") as xmlFile:
                xmlString: str = xmlFile.read()
        except (ValueError, Exception) as e:
            self.ioLogger.error(f'xml open:  {e}')
            raise e

        return xmlString

    def decompressFile(self, fqFileName: str) -> str:
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
            self.ioLogger.error(f'decompress open:  {e}')
            raise e
        else:
            self.ioLogger.info(f'{ZLIB_VERSION=}')
            xmlBytes:  bytes = decompress(compressedData)  # has b'....' around it
            xmlString: str   = xmlBytes.decode()
            self.ioLogger.debug(f'Document read:\n{xmlString}')

        return xmlString
