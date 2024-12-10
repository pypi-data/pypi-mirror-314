
from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from untangle import Element

from codeallyadvanced.ui.AttachmentSide import AttachmentSide

from miniogl.ControlPoint import ControlPoint
from miniogl.SelectAnchorPoint import SelectAnchorPoint

from pyutmodelv2.PyutClass import PyutClass
from pyutmodelv2.PyutInterface import PyutInterface
from pyutmodelv2.PyutLink import PyutLink

from pyutmodelv2.enumerations.PyutLinkType import PyutLinkType

from ogl.OglPosition import OglPosition
from ogl.OglAggregation import OglAggregation
from ogl.OglAssociation import OglAssociation
from ogl.OglComposition import OglComposition
from ogl.OglInheritance import OglInheritance
from ogl.OglInterface import OglInterface
from ogl.OglNoteLink import OglNoteLink
from ogl.OglClass import OglClass
from ogl.OglLink import OglLink
from ogl.OglInterface2 import OglInterface2
from ogl.OglAssociationLabel import OglAssociationLabel

from untanglepyut import XmlConstants

from untanglepyut.Types import Elements
from untanglepyut.Types import GraphicLinkAttributes
from untanglepyut.Types import LinkableOglObject
from untanglepyut.Types import LinkableOglObjects
from untanglepyut.Types import UntangledControlPoints
from untanglepyut.Types import UntangledOglLinks
from untanglepyut.Types import createUntangledOglLinks

from untanglepyut.UnTanglePyut import UnTanglePyut
from untanglepyut.XmlVersion import XmlVersion


class UnTangleOglLinks:
    """
    """

    def __init__(self, xmlVersion: XmlVersion):

        self.logger: Logger = getLogger(__name__)

        self._untanglePyut:  UnTanglePyut = UnTanglePyut(xmlVersion=xmlVersion)
        self._xmlVersion:    XmlVersion   = xmlVersion
        if xmlVersion == XmlVersion.V10:
            self._elementOglLink:       str = XmlConstants.V10_ELEMENT_OGL_LINK
            self._elementOglInterface2: str = XmlConstants.V10_ELEMENT_OGL_INTERFACE2
            self._elementInterface2:    str = XmlConstants.V10_ELEMENT_INTERFACE2
            self._elementLink:          str = XmlConstants.V10_ELEMENT_LINK
            self._elementCenter:        str = XmlConstants.V10_ELEMENT_LABEL_CENTER
            self._elementSource:        str = XmlConstants.V10_ELEMENT_LABEL_SOURCE
            self._elementDestination:   str = XmlConstants.V10_ELEMENT_LABEL_DESTINATION
            self._attrSourceId:         str = XmlConstants.V10_ATTR_SOURCE_ID
            self._attrDestinationId:    str = XmlConstants.V10_ATTR_DESTINATION_ID
        else:
            self._elementOglLink       = XmlConstants.V11_ELEMENT_OGL_LINK
            self._elementOglInterface2 = XmlConstants.V11_ELEMENT_OGL_INTERFACE2
            self._elementInterface2    = XmlConstants.V11_ELEMENT_INTERFACE2
            self._elementLink          = XmlConstants.V11_ELEMENT_LINK
            self._elementCenter        = XmlConstants.V11_ELEMENT_LABEL_CENTER
            self._elementSource        = XmlConstants.V11_ELEMENT_LABEL_SOURCE
            self._elementDestination   = XmlConstants.V11_ELEMENT_LABEL_DESTINATION
            self._attrSourceId         = XmlConstants.V11_ATTR_SOURCE_ID
            self._attrDestinationId    = XmlConstants.V11_ATTR_DESTINATION_ID

    def unTangle(self, pyutDocument: Element, linkableOglObjects: LinkableOglObjects) -> UntangledOglLinks:
        """
        Convert from XML to Ogl Links

        Args:
            pyutDocument:  The Element that represents the Class Diagram XML
            linkableOglObjects:    OGL objects that can have links

        Returns:  The links between any of the above objects.  Also returns the graphic lollipop links
        """

        oglLinks: UntangledOglLinks = createUntangledOglLinks()

        graphicLinks: Elements = cast(Elements, pyutDocument.get_elements(self._elementOglLink))
        for graphicLink in graphicLinks:
            oglLink: OglLink = self._graphicLinkToOglLink(graphicLink, linkableOglObjects=linkableOglObjects)
            oglLinks.append(oglLink)

        graphicLollipops: Elements = cast(Elements, pyutDocument.get_elements(self._elementOglInterface2))
        for graphicLollipop in graphicLollipops:
            oglInterface2: OglInterface2 = self._graphicLollipopToOglInterface(graphicLollipop, linkableOglObjects)
            oglLinks.append(oglInterface2)

        return oglLinks

    def _graphicLinkToOglLink(self, graphicLink: Element, linkableOglObjects: LinkableOglObjects) -> OglLink:
        """
        This code is way too convoluted.  Failing to do any of these step in this code leads to BAD
        visual representations.
        TODO:  Figure out how to simplify this code and/or make it more readable and obvious on how to create
        links (of whatever kind) between 2 OglClass'es

        Args:
            graphicLink:        The XML `GraphicClass` element
            linkableOglObjects:    OGL objects that can have links

        Returns:  A fully formed OglLink including control points
        """

        assert len(linkableOglObjects) != 0, 'Developer forgot to create dictionary'
        gla: GraphicLinkAttributes = GraphicLinkAttributes.fromGraphicLink(xmlVersion=self._xmlVersion, graphicLink=graphicLink)

        links: Elements = cast(Elements, graphicLink.get_elements(self._elementLink))
        assert len(links) == 1, 'Should only ever be one'

        singleLink:  Element = links[0]
        sourceId:    int = int(singleLink[self._attrSourceId])
        dstId:       int = int(singleLink[self._attrDestinationId])
        self.logger.debug(f'graphicLink= {gla.srcX=} {gla.srcY=} {gla.dstX=} {gla.dstY=} {gla.spline=}')

        try:
            srcShape: LinkableOglObject = linkableOglObjects[sourceId]
            dstShape: LinkableOglObject = linkableOglObjects[dstId]
        except KeyError as ke:
            self.logger.error(f'{linkableOglObjects=}')
            self.logger.error(f'Developer Error -- {singleLink=}')
            self.logger.error(f'Developer Error -- {sourceId=} {dstId=}  KeyError index: {ke}')
            return cast(OglLink, None)

        pyutLink: PyutLink = self._untanglePyut.linkToPyutLink(singleLink, source=srcShape.pyutObject, destination=dstShape.pyutObject)
        oglLink:  OglLink  = self._oglLinkFactory(srcShape=srcShape, pyutLink=pyutLink, destShape=dstShape,
                                                  linkType=pyutLink.linkType,
                                                  srcPos=(gla.srcX, gla.srcY),
                                                  dstPos=(gla.dstX, gla.dstY)
                                                  )
        oglLink.spline = gla.spline
        srcShape.addLink(oglLink)
        dstShape.addLink(oglLink)

        # put the anchors at the right position
        srcAnchor = oglLink.sourceAnchor
        dstAnchor = oglLink.destinationAnchor
        srcAnchor.SetPosition(gla.srcX, gla.srcY)
        dstAnchor.SetPosition(gla.dstX, gla.dstY)

        srcModel = srcAnchor.model
        srcModel.SetPosition(x=gla.srcX, y=gla.srcY)
        dstModel = dstAnchor.model
        dstModel.SetPosition(x=gla.dstX, y=gla.dstY)

        # add the control points to the line
        line   = srcAnchor.lines[0]     # only 1 line per anchor in Pyut
        parent = line.sourceAnchor.parent
        selfLink: bool = parent is oglLink.destinationAnchor.parent

        controlPoints: UntangledControlPoints = self._generateControlPoints(graphicLink=graphicLink)
        for controlPoint in controlPoints:
            oglLink.AddControl(control=controlPoint, after=None)
            if selfLink:
                x, y = controlPoint.GetPosition()
                controlPoint.parent = parent
                controlPoint.SetPosition(x, y)

        if isinstance(oglLink, OglAssociation):
            self._addAssociationLabels(graphicLink, oglLink)

        self._reconstituteLinkDataModel(oglLink)

        return oglLink

    def _oglLinkFactory(self, srcShape, pyutLink, destShape, linkType: PyutLinkType, srcPos=None, dstPos=None):
        """
        Used to get an OglLink of the given linkType.

        Args:
            srcShape:   Source shape
            pyutLink:   Conceptual links associated with the graphical links.
            destShape:  Destination shape
            linkType:   The linkType of the link (OGL_INHERITANCE, ...)
            srcPos:     source position
            dstPos:     destination position

        Returns:  The requested link
        """
        if linkType == PyutLinkType.AGGREGATION:
            return OglAggregation(srcShape, pyutLink, destShape, srcPos=srcPos, dstPos=dstPos)

        elif linkType == PyutLinkType.COMPOSITION:
            return OglComposition(srcShape, pyutLink, destShape, srcPos=srcPos, dstPos=dstPos)

        elif linkType == PyutLinkType.INHERITANCE:
            return OglInheritance(srcShape, pyutLink, destShape)

        elif linkType == PyutLinkType.ASSOCIATION:
            return OglAssociation(srcShape, pyutLink, destShape, srcPos=srcPos, dstPos=dstPos)

        elif linkType == PyutLinkType.INTERFACE:
            return OglInterface(srcShape, pyutLink, destShape, srcPos=srcPos, dstPos=dstPos)

        elif linkType == PyutLinkType.NOTELINK:
            return OglNoteLink(srcShape, pyutLink, destShape)

        elif linkType == PyutLinkType.SD_MESSAGE:
            assert False, 'Sequence Diagram Messages not supported'
            # return OglSDMessage(srcShape=srcShape, pyutSDMessage=pyutLink, dstShape=destShape)
        else:
            self.logger.error(f"Unknown OglLinkType: {linkType}")
            return None

    def _graphicLollipopToOglInterface(self, graphicLollipop: Element, linkableOglObjects: LinkableOglObjects) -> OglInterface2:

        assert len(linkableOglObjects) != 0, 'Developer forgot to create dictionary'

        x: int = int(graphicLollipop['x'])
        y: int = int(graphicLollipop['y'])
        attachmentLocationStr: str            = graphicLollipop['attachmentPoint']
        attachmentSide:        AttachmentSide = AttachmentSide.toEnum(attachmentLocationStr)

        elements: Elements = cast(Elements, graphicLollipop.get_elements(self._elementInterface2))
        assert len(elements) == 1, 'If more than one interface tag the XML is invalid'

        pyutInterface:    PyutInterface = self._untanglePyut.interfaceToPyutInterface(oglInterface2=graphicLollipop)

        self.logger.debug(f'{pyutInterface.name} {pyutInterface.id=} {pyutInterface.implementors=}')

        # oglClass:    OglClass    = self._getOglClassFromName(pyutInterface.implementors[0], linkableOglObjects)

        oglClass:    OglClass    = self._determineAttachedToClass(x=x, y=y, linkableOglObjects=linkableOglObjects)
        oglPosition: OglPosition = self._determineAttachmentPoint(attachmentSide, oglClass)

        self.logger.debug(f'{oglClass.id=} {oglPosition.x=} {oglPosition.y=}')

        anchorPoint:      SelectAnchorPoint = SelectAnchorPoint(x=oglPosition.x, y=oglPosition.y, attachmentSide=attachmentSide, parent=oglClass)
        oglInterface2:    OglInterface2     = OglInterface2(pyutInterface=pyutInterface, destinationAnchor=anchorPoint)

        self.logger.debug(f'{oglInterface2.id=} {oglInterface2.destinationAnchor=}')
        return oglInterface2

    def _getOglClassFromName(self, className: str, linkableOglObjects: LinkableOglObjects) -> OglClass:
        """
        Looks up a name in the linkable objects dictionary and return the associated class
        TODO: Make a simple lookup and catch any Key errors

        Args:
            className:
            linkableOglObjects:

        Returns:
        """

        foundClass: OglClass = cast(OglClass, None)
        for oglClass in linkableOglObjects.values():
            if oglClass.pyutObject.name == className:
                foundClass = cast(OglClass, oglClass)
                break
        assert foundClass is not None, 'XML must be in error'
        return foundClass

    def _determineAttachmentPoint(self, attachmentPoint: AttachmentSide, oglClass: OglClass) -> OglPosition:
        """
        Even though we serialize the attachment point location that position is relative to the diagram.
        When we recreate the attachment point position we have to create it relative to its parent
        TODO: When the Pyut serializer makes the positions relative to the implementor we will not need this code

        Args:
            attachmentPoint:    Where on the parent
            oglClass:           The implementor

        Returns:  An OglPosition with coordinates relative to the implementor
        """

        oglPosition: OglPosition = OglPosition()

        dw, dh     = oglClass.GetSize()

        if attachmentPoint == AttachmentSide.NORTH:
            northX: int = dw // 2
            northY: int = 0
            oglPosition.x = northX
            oglPosition.y = northY
        elif attachmentPoint == AttachmentSide.SOUTH:
            southX = dw // 2
            southY = dh
            oglPosition.x = southX
            oglPosition.y = southY
        elif attachmentPoint == AttachmentSide.WEST:
            westX: int = 0
            westY: int = dh // 2
            oglPosition.x = westX
            oglPosition.y = westY
        elif attachmentPoint == AttachmentSide.EAST:
            eastX: int = dw
            eastY: int = dh // 2
            oglPosition.x = eastX
            oglPosition.y = eastY
        else:
            self.logger.warning(f'Unknown attachment point: {attachmentPoint}')
            assert False, 'Unknown attachment point'

        return oglPosition

    def _generateControlPoints(self, graphicLink: Element) -> UntangledControlPoints:

        controlPoints: UntangledControlPoints = UntangledControlPoints([])

        controlPointElements: Elements = cast(Elements, graphicLink.get_elements('ControlPoint'))
        for controlPointElement in controlPointElements:
            x: int = int(controlPointElement['x'])
            y: int = int(controlPointElement['y'])
            controlPoint: ControlPoint = ControlPoint(x=x, y=y)
            controlPoints.append(controlPoint)

        return controlPoints

    def _reconstituteLinkDataModel(self, oglLink: OglLink):
        """
        Updates one of the following lists in a PyutLinkedObject:

        ._parents   for Inheritance links
        ._links     for all other link types

        Args:
            oglLink:       An OglLink
        """
        srcShape:  OglClass = oglLink.sourceShape
        destShape: OglClass = oglLink.destinationShape
        self.logger.debug(f'source ID: {srcShape.id} - destination ID: {destShape.id}')

        pyutLink: PyutLink = oglLink.pyutObject

        if pyutLink.linkType == PyutLinkType.INHERITANCE:
            childPyutClass:  PyutClass = cast(PyutClass, srcShape.pyutObject)
            parentPyutClass: PyutClass = cast(PyutClass, destShape.pyutObject)
            childPyutClass.addParent(parentPyutClass)
        else:
            srcPyutClass:  PyutClass = cast(PyutClass, srcShape.pyutObject)
            srcPyutClass.addLink(pyutLink)

    def _addAssociationLabels(self, graphicLink: Element, oglAssociation: OglAssociation):
        """
        The association labels are now separate components;  We need to handle that

        Args:
            graphicLink:    The top level GraphicLink Element
            oglAssociation: The current OGL representation of the graphicLink

        Returns:  The updated association link
        """

        pyutLink:         PyutLink            = oglAssociation.pyutObject

        oglAssociation.centerLabel            = self._createALabel(oglAssociation, graphicLink, text=pyutLink.name,
                                                                   tagName=self._elementCenter)
        oglAssociation.sourceCardinality      = self._createALabel(oglAssociation, graphicLink, text=pyutLink.sourceCardinality,
                                                                   tagName=self._elementSource)
        oglAssociation.destinationCardinality = self._createALabel(oglAssociation, graphicLink, text=pyutLink.destinationCardinality,
                                                                   tagName=self._elementDestination)

    def _createALabel(self, parentAssociation: OglAssociation, graphicLink: Element, text: str, tagName: str) -> OglAssociationLabel:

        labels:  List[Element]   = graphicLink.get_elements(tagName)
        assert len(labels) == 1, 'There can be only one'

        label: Element = labels[0]
        x:     int     = int(label['x'])
        y:     int     = int(label['y'])

        self.logger.debug(f'{tagName=} `{text=}` pos: ({x},{y})')

        updatedLabelText: str = text
        if updatedLabelText is None:
            updatedLabelText = ''
        oglAssociationLabel: OglAssociationLabel = OglAssociationLabel(x=x, y=y, text=updatedLabelText, parent=parentAssociation)

        return oglAssociationLabel

    def _determineAttachedToClass(self, x: int, y: int, linkableOglObjects: LinkableOglObjects) -> OglClass:
        """
        I cannot store a pointer to the class the lollipop is attached to.  However, I need to know the lollipop's
        parent because of
        Args:
            x:
            y:
            linkableOglObjects:

        Returns: The OglClass that the lollipop is attached to
        """

        foundClass: OglClass = cast(OglClass, None)

        for linkableObject in linkableOglObjects.values():
            oglClass: OglClass = cast(OglClass, linkableObject)
            if oglClass.Inside(x=x, y=y) is True:
                foundClass = oglClass
                break

        assert foundClass is not None, 'XML must be in error'
        return foundClass
