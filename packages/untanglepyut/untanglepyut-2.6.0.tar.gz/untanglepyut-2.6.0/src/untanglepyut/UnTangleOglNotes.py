
from logging import Logger
from logging import getLogger

from untangle import Element

from pyutmodelv2.PyutNote import PyutNote

from ogl.OglNote import OglNote

from untanglepyut.BaseUnTangle import BaseUnTangle

from untanglepyut.Types import Elements
from untanglepyut.Types import GraphicInformation
from untanglepyut.Types import UntangledOglNotes
from untanglepyut.Types import createUntangledOglNotes
from untanglepyut.UnTanglePyut import UnTanglePyut

from untanglepyut import XmlConstants

from untanglepyut.XmlVersion import XmlVersion


class UnTangleOglNotes(BaseUnTangle):
    def __init__(self, xmlVersion: XmlVersion):

        super().__init__(xmlVersion=xmlVersion)

        self.logger: Logger = getLogger(__name__)

        self._untanglePyut: UnTanglePyut = UnTanglePyut(xmlVersion=xmlVersion)

        if xmlVersion == XmlVersion.V10:
            self._elementOglNote: str = XmlConstants.V10_ELEMENT_NOTE
        else:
            self._elementOglNote = XmlConstants.V11_ELEMENT_NOTE

    def unTangle(self, pyutDocument: Element) -> UntangledOglNotes:
        """

        Args:
            pyutDocument:

        Returns: untangled OglNote objects if any exist, else an empty list
        """

        oglNotes:     UntangledOglNotes = createUntangledOglNotes()
        graphicNotes: Elements          = pyutDocument.get_elements(self._elementOglNote)

        for graphicNote in graphicNotes:
            self.logger.debug(f'{graphicNote}')

            graphicInformation: GraphicInformation = GraphicInformation.toGraphicInfo(graphicElement=graphicNote)
            oglNote:            OglNote            = OglNote(w=graphicInformation.width, h=graphicInformation.height)
            oglNote.SetPosition(x=graphicInformation.x, y=graphicInformation.y)
            self._updateModel(oglObject=oglNote, graphicInformation=graphicInformation)

            pyutNote: PyutNote = self._untanglePyut.noteToPyutNote(graphicNote=graphicNote)
            oglNote.pyutObject = pyutNote
            oglNotes.append(oglNote)

        return oglNotes
