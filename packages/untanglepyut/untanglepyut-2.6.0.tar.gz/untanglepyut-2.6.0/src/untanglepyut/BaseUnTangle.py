
from logging import Logger
from logging import getLogger

from miniogl.models.ShapeModel import ShapeModel

from ogl.OglObject import OglObject
from ogl.sd.OglSDInstance import OglSDInstance

from untanglepyut.Types import GraphicInformation

from untanglepyut.UnTangleIO import UnTangleIO
from untanglepyut.XmlVersion import XmlVersion


class BaseUnTangle(UnTangleIO):

    def __init__(self, xmlVersion: XmlVersion):
        super().__init__()
        self.baseLogger: Logger = getLogger(__name__)

        self._xmlVersion = xmlVersion

    def _updateModel(self, oglObject: OglObject | OglSDInstance, graphicInformation: GraphicInformation) -> ShapeModel:
        """
        This is necessary if it is never added to a diagram
        and immediately serialized

        Args:
            oglObject:      OglObject with a model
            graphicInformation:   The graphic class graphic information

        Returns:  The updated shape model as a way of documenting that we updated it
        """
        model: ShapeModel = oglObject.model
        model.SetPosition(x=graphicInformation.x, y=graphicInformation.y)

        return model
