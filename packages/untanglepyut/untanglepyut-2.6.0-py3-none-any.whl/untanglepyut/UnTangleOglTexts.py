
from logging import Logger
from logging import getLogger

from untangle import Element

from pyutmodelv2.PyutText import PyutText

from ogl.OglText import OglText

from untanglepyut import XmlConstants

from untanglepyut.BaseUnTangle import BaseUnTangle
from untanglepyut.Types import GraphicInformation
from untanglepyut.UnTanglePyut import UnTanglePyut

from untanglepyut.XmlVersion import XmlVersion

from untanglepyut.Types import Elements
from untanglepyut.Types import UntangledOglTexts
from untanglepyut.Types import createUntangledOglTexts


class UnTangleOglTexts(BaseUnTangle):
    """
    Yes, I know bad English
    """
    def __init__(self, xmlVersion: XmlVersion):

        super().__init__(xmlVersion=xmlVersion)

        self.logger: Logger = getLogger(__name__)

        self._untanglePyut: UnTanglePyut = UnTanglePyut(xmlVersion=xmlVersion)

        if xmlVersion == XmlVersion.V10:
            self._elementOglText: str = XmlConstants.V10_ELEMENT_TEXT
        else:
            self._elementOglText = XmlConstants.V11_ELEMENT_TEXT

    def unTangle(self, pyutDocument: Element) -> UntangledOglTexts:
        """

        Args:
            pyutDocument:  The Element document

        Returns:  untangled OglText objects if any exist, else an empty list
        """

        oglTexts:     UntangledOglTexts = createUntangledOglTexts()
        graphicTexts: Elements          = pyutDocument.get_elements(self._elementOglText)

        for graphicText in graphicTexts:
            self.logger.debug(f'{graphicText}')

            graphicInformation: GraphicInformation = GraphicInformation.toGraphicInfo(graphicElement=graphicText)
            pyutText:           PyutText           = self._untanglePyut.textToPyutText(graphicText=graphicText)
            oglText:            OglText            = OglText(pyutText=pyutText, width=graphicInformation.width, height=graphicInformation.height)
            oglText.SetPosition(x=graphicInformation.x, y=graphicInformation.y)
            #
            # This is necessary if it is never added to a diagram
            # and immediately serialized
            #
            self._updateModel(oglObject=oglText, graphicInformation=graphicInformation)
            oglText.pyutText = pyutText
            oglTexts.append(oglText)

        return oglTexts
