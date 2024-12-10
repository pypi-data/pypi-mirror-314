
from logging import Logger
from logging import getLogger

from untangle import Element

from pyutmodelv2.PyutActor import PyutActor
from pyutmodelv2.PyutUseCase import PyutUseCase

from ogl.OglActor import OglActor
from ogl.OglUseCase import OglUseCase

from untanglepyut import XmlConstants

from untanglepyut.BaseUnTangle import BaseUnTangle
from untanglepyut.UnTanglePyut import UnTanglePyut
from untanglepyut.XmlVersion import XmlVersion

from untanglepyut.Types import GraphicInformation
from untanglepyut.Types import UntangledOglActors
from untanglepyut.Types import UntangledOglUseCases
from untanglepyut.Types import createUntangledOglActors
from untanglepyut.Types import createUntangledOglUseCases


class UnTangleUseCaseDiagram(BaseUnTangle):
    """
        <PyutDocument type="USECASE_DIAGRAM" title="Use-Cases" scrollPositionX="0" scrollPositionY="0" pixelsPerUnitX="20" pixelsPerUnitY="20">
            <GraphicActor width="87" height="114" x="293" y="236">
                <Actor id="1" name="BasicActor" filename=""/>
            </GraphicActor>
            <GraphicUseCase width="100" height="60" x="575" y="250">
                <UseCase id="2" name="Basic Use Case" filename=""/>
            </GraphicUseCase>
            <GraphicLink srcX="379" srcY="286" dstX="575" dstY="280" spline="False">
                <LabelCenter x="555" y="281"/>
                <LabelSrc x="555" y="281"/>
                <LabelDst x="555" y="281"/>
                <Link name="Kicks Butt" type="ASSOCIATION" cardSrc="" cardDestination="" bidir="False" sourceId="1" destId="2"/>
            </GraphicLink>
        </PyutDocument>
    """

    def __init__(self, xmlVersion: XmlVersion):

        super().__init__(xmlVersion)
        self.logger: Logger = getLogger(__name__)

        self._untangledOglActors:   UntangledOglActors   = createUntangledOglActors()
        self._untangledOglUseCases: UntangledOglUseCases = createUntangledOglUseCases()
        self._untanglePyut:         UnTanglePyut         = UnTanglePyut(xmlVersion=xmlVersion)

        if xmlVersion == XmlVersion.V10:
            self._elementActor:   str = XmlConstants.V10_ELEMENT_ACTOR
            self._elementUseCase: str = XmlConstants.V10_ELEMENT_USE_CASE
        else:
            self._elementActor   = XmlConstants.V11_ELEMENT_ACTOR
            self._elementUseCase = XmlConstants.V11_ELEMENT_USE_CASE

    def unTangle(self, pyutDocument: Element):
        """

        Args:
            pyutDocument:
        """

        self._untangledOglActors   = self._unTangleOglActors(pyutDocument=pyutDocument)
        self._untangledOglUseCases = self._unTangleOglUseCases(pyutDocument=pyutDocument)

    @property
    def oglActors(self) -> UntangledOglActors:
        return self._untangledOglActors

    @property
    def oglUseCases(self) -> UntangledOglUseCases:
        return self._untangledOglUseCases

    def _unTangleOglActors(self, pyutDocument: Element) -> UntangledOglActors:
        untangledOglActors: UntangledOglActors = createUntangledOglActors()
        graphicActors:      Element            = pyutDocument.get_elements(self._elementActor)

        for graphicActor in graphicActors:
            graphicInfo: GraphicInformation = GraphicInformation.toGraphicInfo(graphicActor)
            oglActor:    OglActor           = OglActor(w=graphicInfo.width, h=graphicInfo.height)
            oglActor.SetPosition(x=graphicInfo.x, y=graphicInfo.y)

            self._updateModel(oglObject=oglActor, graphicInformation=graphicInfo)

            pyutActor: PyutActor = self._untanglePyut.actorToPyutActor(graphicActor=graphicActor)

            oglActor.pyutObject = pyutActor

            untangledOglActors.append(oglActor)

        return untangledOglActors

    def _unTangleOglUseCases(self, pyutDocument: Element) -> UntangledOglUseCases:

        untangledOglUseCases: UntangledOglUseCases = createUntangledOglUseCases()

        graphicUseCases: Element = pyutDocument.get_elements(self._elementUseCase)
        for graphicUseCase in graphicUseCases:
            graphicInfo: GraphicInformation = GraphicInformation.toGraphicInfo(graphicUseCase)
            oglUseCase:  OglUseCase         = OglUseCase(w=graphicInfo.width, h=graphicInfo.height)

            oglUseCase.SetPosition(x=graphicInfo.x, y=graphicInfo.y)

            self._updateModel(oglObject=oglUseCase, graphicInformation=graphicInfo)

            pyutUseCase: PyutUseCase = self._untanglePyut.useCaseToPyutUseCase(graphicUseCase=graphicUseCase)

            oglUseCase.pyutObject = pyutUseCase

            untangledOglUseCases.append(oglUseCase)

        return untangledOglUseCases
