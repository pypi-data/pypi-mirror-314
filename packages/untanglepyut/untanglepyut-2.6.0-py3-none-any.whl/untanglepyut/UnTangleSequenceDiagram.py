
from typing import List

from logging import Logger
from logging import getLogger

from untangle import Element

from pyutmodelv2.PyutSDInstance import PyutSDInstance
from pyutmodelv2.PyutSDMessage import PyutSDMessage

from ogl.sd.OglSDInstance import OglSDInstance
from ogl.sd.OglSDMessage import OglSDMessage

from untanglepyut import XmlConstants
from untanglepyut.Types import GraphicInformation
from untanglepyut.Types import OglSDInstances
from untanglepyut.Types import OglSDMessages

from untanglepyut.BaseUnTangle import BaseUnTangle
from untanglepyut.Types import createOglSDInstances
from untanglepyut.Types import createOglSDMessages
from untanglepyut.UnTanglePyut import ConvolutedPyutSDMessageInformation
from untanglepyut.UnTanglePyut import UnTanglePyut
from untanglepyut.XmlVersion import XmlVersion


class UnTangleSequenceDiagram(BaseUnTangle):

    def __init__(self, xmlVersion: XmlVersion):

        super().__init__(xmlVersion)

        self.logger: Logger = getLogger(__name__)

        self._oglSDInstances: OglSDInstances = createOglSDInstances()
        self._oglSDMessages:  OglSDMessages  = createOglSDMessages()

        self._untanglePyut: UnTanglePyut = UnTanglePyut(xmlVersion=xmlVersion)

        if xmlVersion == XmlVersion.V10:
            self._elementInstance: str = XmlConstants.V10_ELEMENT_INSTANCE
            self._elementMessage:  str = XmlConstants.V10_ELEMENT_MESSAGE
        else:
            self._elementInstance = XmlConstants.V11_ELEMENT_INSTANCE
            self._elementMessage  = XmlConstants.V11_ELEMENT_MESSAGE

    def unTangle(self, pyutDocument: Element):
        """

        Args:
            pyutDocument:  The pyut untangle element that represents a sequence diagram
        """
        self._oglSDInstances = self._untangleSDInstances(pyutDocument=pyutDocument)
        self._oglSDMessages  = self._untangleSDMessages(pyutDocument=pyutDocument)

    @property
    def oglSDInstances(self) -> OglSDInstances:
        return self._oglSDInstances

    @property
    def oglSDMessages(self) -> OglSDMessages:
        return self._oglSDMessages

    def _untangleSDInstances(self, pyutDocument: Element) -> OglSDInstances:

        oglSDInstances:     OglSDInstances = createOglSDInstances()
        graphicSDInstances: List[Element]   = pyutDocument.get_elements(self._elementInstance)

        for graphicSDInstance in graphicSDInstances:
            self.logger.debug(f'{graphicSDInstance=}')
            pyutSDInstance: PyutSDInstance     = self._untanglePyut.sdInstanceToPyutSDInstance(oglSDInstanceElement=graphicSDInstance)

            oglSDInstance:  OglSDInstance      = OglSDInstance(pyutSDInstance)
            graphicInfo:    GraphicInformation = GraphicInformation.toGraphicInfo(graphicElement=graphicSDInstance)

            oglSDInstance.SetSize(width=graphicInfo.width, height=graphicInfo.height)
            oglSDInstance.SetPosition(x=graphicInfo.x, y=graphicInfo.y)

            self._updateModel(oglObject=oglSDInstance, graphicInformation=graphicInfo)

            oglSDInstances[pyutSDInstance.id] = oglSDInstance
        return oglSDInstances

    def _untangleSDMessages(self, pyutDocument: Element) -> OglSDMessages:

        oglSDMessages:     OglSDMessages = createOglSDMessages()
        graphicSDMessages: List[Element] = pyutDocument.get_elements(self._elementMessage)

        for graphicSDMessage in graphicSDMessages:
            bogus: ConvolutedPyutSDMessageInformation = self._untanglePyut.sdMessageToPyutSDMessage(oglSDMessageElement=graphicSDMessage)

            pyutSDMessage: PyutSDMessage = bogus.pyutSDMessage

            srcInstance: OglSDInstance = self._oglSDInstances[bogus.sourceId]
            dstInstance: OglSDInstance = self._oglSDInstances[bogus.destinationId]

            pyutSDMessage.source      = srcInstance.pyutSDInstance         # Ugh, time was set by sdMessageToPyutSDMessage
            pyutSDMessage.destination = dstInstance.pyutSDInstance         # This "split" functionality must be fixed

            oglSDMessage: OglSDMessage = OglSDMessage(srcSDInstance=srcInstance, pyutSDMessage=pyutSDMessage, dstSDInstance=dstInstance)

            oglSDMessages[pyutSDMessage.id] = oglSDMessage

        return oglSDMessages
