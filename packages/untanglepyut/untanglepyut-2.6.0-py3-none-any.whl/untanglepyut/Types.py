
from typing import Dict
from typing import List
from typing import NewType
from typing import Union
from typing import cast

from dataclasses import dataclass
from dataclasses import field

from untangle import Element

from codeallybasic.SecureConversions import SecureConversions

from miniogl.ControlPoint import ControlPoint

from ogl.OglActor import OglActor
from ogl.OglClass import OglClass
from ogl.OglLink import OglLink
from ogl.OglNote import OglNote
from ogl.OglText import OglText
from ogl.OglUseCase import OglUseCase
from ogl.OglInterface2 import OglInterface2
from ogl.sd.OglSDInstance import OglSDInstance
from ogl.sd.OglSDMessage import OglSDMessage

from untanglepyut.XmlVersion import XmlVersion

UntangledControlPoints = NewType('UntangledControlPoints', List[ControlPoint])

Elements = NewType('Elements', List[Element])


@dataclass
class GraphicInformation:
    """
    Internal Class use to move information from a Graphic XML element
    into Python
    """
    x: int = -1
    y: int = -1
    width:  int = -1
    height: int = -1

    @classmethod
    def toGraphicInfo(cls, graphicElement: Element) -> 'GraphicInformation':
        graphicInformation: GraphicInformation = GraphicInformation()

        graphicInformation.x = int(graphicElement['x'])
        graphicInformation.y = int(graphicElement['y'])

        graphicInformation.width  = int(graphicElement['width'])
        graphicInformation.height = int(graphicElement['height'])

        return graphicInformation


UntangledOglClasses    = NewType('UntangledOglClasses', List[OglClass])
UntangledLink          = Union[OglLink, OglInterface2]

UntangledOglLinks      = NewType('UntangledOglLinks',    List[UntangledLink])
UntangledOglNotes      = NewType('UntangledOglNotes',    List[OglNote])
UntangledOglTexts      = NewType('UntangledOglTexts',    List[OglText])
UntangledOglActors     = NewType('UntangledOglActors',   List[OglActor])
UntangledOglUseCases   = NewType('UntangledOglUseCases', List[OglUseCase])

OglSDInstances = NewType('OglSDInstances', Dict[int, OglSDInstance])
OglSDMessages  = NewType('OglSDMessages',  Dict[int, OglSDMessage])

"""
Factory methods for our dataclasses
"""


def createUntangledOglClasses() -> UntangledOglClasses:
    """
    Factory method to create  the UntangledClasses data structure;

    Returns:  A new data structure
    """
    return UntangledOglClasses([])


def createUntangledOglNotes() -> UntangledOglNotes:
    return UntangledOglNotes([])


def createUntangledOglTexts() -> UntangledOglTexts:
    return UntangledOglTexts([])


def createUntangledOglLinks() -> UntangledOglLinks:
    return UntangledOglLinks([])


def createUntangledOglUseCases() -> UntangledOglUseCases:
    return UntangledOglUseCases([])


def createUntangledOglActors() -> UntangledOglActors:
    return UntangledOglActors([])


def createOglSDInstances() -> OglSDInstances:
    return OglSDInstances({})


def createOglSDMessages() -> OglSDMessages:
    return OglSDMessages({})


DocumentTitle = NewType('DocumentTitle', str)


@dataclass
class Document:
    """
    Create a UseCaseDocument and a ClassDiagramDocument
    """
    documentType:    DocumentTitle = DocumentTitle('')
    documentTitle:   str = ''
    scrollPositionX: int = -1
    scrollPositionY: int = -1
    pixelsPerUnitX:  int = -1
    pixelsPerUnitY:  int = -1
    oglClasses:      UntangledOglClasses  = field(default_factory=createUntangledOglClasses)
    oglLinks:        UntangledOglLinks    = field(default_factory=createUntangledOglLinks)
    oglNotes:        UntangledOglNotes    = field(default_factory=createUntangledOglNotes)
    oglTexts:        UntangledOglTexts    = field(default_factory=createUntangledOglTexts)
    oglActors:       UntangledOglActors   = field(default_factory=createUntangledOglActors)
    oglUseCases:     UntangledOglUseCases = field(default_factory=createUntangledOglUseCases)
    oglSDInstances:  OglSDInstances = field(default_factory=createOglSDInstances)
    oglSDMessages:   OglSDMessages  = field(default_factory=createOglSDMessages)


Documents     = NewType('Documents', dict[DocumentTitle, Document])

# @dataclass
# class SDDocument(Document):
#     oglSDInstances:  OglSDInstances = field(default_factory=createOglSDInstances)
#     oglSDMessages:   OGLSDMessages  = field(default_factory=createOGLSDMessages)

LinkableOglObject = Union[OglClass, OglNote, OglActor, OglUseCase]

LinkableOglObjects = NewType('LinkableOglObjects',   Dict[int, LinkableOglObject])


def createLinkableOglObjects() -> LinkableOglObjects:
    return LinkableOglObjects({})


@dataclass
class GraphicLinkAttributes:

    srcX:   int = -1
    srcY:   int = -1
    dstX:   int = -1
    dstY:   int = -1
    spline: bool = False

    @classmethod
    def fromGraphicLink(cls, xmlVersion: XmlVersion, graphicLink: Element) -> 'GraphicLinkAttributes':

        gla: GraphicLinkAttributes = GraphicLinkAttributes()
        if xmlVersion == XmlVersion.V10:
            gla.srcX = int(graphicLink['srcX'])
            gla.srcY = int(graphicLink['srcY'])
            gla.dstX = int(graphicLink['dstX'])
            gla.dstY = int(graphicLink['dstY'])
        else:
            gla.srcX = int(graphicLink['sourceAnchorX'])
            gla.srcY = int(graphicLink['sourceAnchorY'])
            gla.dstX = int(graphicLink['destinationAnchorX'])
            gla.dstY = int(graphicLink['destinationAnchorY'])

        gla.spline = SecureConversions.secureBoolean(graphicLink['spline'])

        return gla


@dataclass
class ProjectInformation:
    fileName: str = cast(str, None)
    version:  str = cast(str, None)
    codePath: str = cast(str, None)
