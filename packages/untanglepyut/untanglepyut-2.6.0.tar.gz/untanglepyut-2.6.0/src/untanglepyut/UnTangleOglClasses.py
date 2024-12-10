
from typing import cast

from logging import Logger
from logging import getLogger

from untangle import Element

from pyutmodelv2.PyutClass import PyutClass

from ogl.OglClass import OglClass

from untanglepyut import XmlConstants

from untanglepyut.BaseUnTangle import BaseUnTangle

from untanglepyut.Types import Elements
from untanglepyut.Types import GraphicInformation
from untanglepyut.Types import UntangledOglClasses
from untanglepyut.Types import createUntangledOglClasses

from untanglepyut.UnTanglePyut import UnTanglePyut

from untanglepyut.XmlVersion import XmlVersion


class UnTangleOglClasses(BaseUnTangle):

    def __init__(self, xmlVersion: XmlVersion):

        super().__init__(xmlVersion)
        self.logger: Logger = getLogger(__name__)

        self._untanglePyut: UnTanglePyut = UnTanglePyut(xmlVersion=xmlVersion)

        if xmlVersion == XmlVersion.V10:
            self._elementOglClass: str = XmlConstants.V10_ELEMENT_CLASS
        else:
            self._elementOglClass = XmlConstants.V11_ELEMENT_CLASS

    def unTangle(self, pyutDocument: Element) -> UntangledOglClasses:
        oglClasses:     UntangledOglClasses = createUntangledOglClasses()
        graphicClasses: Elements            = cast(Elements, pyutDocument.get_elements(self._elementOglClass))

        for graphicClass in graphicClasses:
            self.logger.debug(f'{graphicClass=}')

            graphicInformation: GraphicInformation = GraphicInformation.toGraphicInfo(graphicElement=graphicClass)
            oglClass:           OglClass           = OglClass(pyutClass=None, w=graphicInformation.width, h=graphicInformation.height)
            oglClass.SetPosition(x=graphicInformation.x, y=graphicInformation.y)
            #
            # This is necessary if it is never added to a diagram
            # and immediately serialized
            #
            self._updateModel(oglObject=oglClass, graphicInformation=graphicInformation)

            pyutClass: PyutClass = self._untanglePyut.classToPyutClass(graphicClass=graphicClass)
            oglClass.pyutObject = pyutClass
            oglClasses.append(oglClass)

        return oglClasses
