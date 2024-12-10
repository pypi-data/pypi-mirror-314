
from typing import cast

from logging import Logger
from logging import getLogger

from untangle import parse
from untangle import Element

from untanglepyut.BaseUnTangle import BaseUnTangle

from untanglepyut.Types import Document
from untanglepyut.Types import DocumentTitle
from untanglepyut.Types import Documents

from untanglepyut.Types import ProjectInformation
from untanglepyut.Types import UntangledOglClasses
from untanglepyut.Types import UntangledOglNotes
from untanglepyut.Types import UntangledOglTexts
from untanglepyut.Types import createLinkableOglObjects

from untanglepyut.UnTangleOglTexts import UnTangleOglTexts

from untanglepyut.UnTangleProjectInformation import UnTangleProjectInformation
from untanglepyut.UnTanglePyut import UnTanglePyut
from untanglepyut.UnTangleUseCaseDiagram import UnTangleUseCaseDiagram
from untanglepyut.UnTangleSequenceDiagram import UnTangleSequenceDiagram
from untanglepyut.UnTangleOglLinks import LinkableOglObjects
from untanglepyut.UnTangleOglLinks import UnTangleOglLinks
from untanglepyut.UnTangleOglClasses import UnTangleOglClasses
from untanglepyut.UnTangleOglNotes import UnTangleOglNotes

from untanglepyut.XmlVersion import XmlVersion


class UnTangler(BaseUnTangle):

    def __init__(self, xmlVersion: XmlVersion):
        """
        """
        super().__init__(xmlVersion)
        self.logger: Logger = getLogger(__name__)

        self._projectInformation: ProjectInformation = cast(ProjectInformation, None)
        self._documents:          Documents          = Documents({})

        self._untanglePyut:     UnTanglePyut     = UnTanglePyut(xmlVersion=xmlVersion)
        self._untangleOglLinks: UnTangleOglLinks = UnTangleOglLinks(xmlVersion=xmlVersion)

    @property
    def projectInformation(self) -> ProjectInformation:
        """
        This property return nothing valid until you untangle the file

        Returns:  The project information of the untangled pyut file
        """
        return self._projectInformation

    @property
    def documents(self) -> Documents:
        return self._documents

    def untangleFile(self, fqFileName: str):
        """
        Read input file and untangle to Ogl
        Args:
            fqFileName:  The file name with the XML

        """
        xmlString:   str     = self.getRawXml(fqFileName=fqFileName)
        self.untangleXml(xmlString=xmlString, fqFileName=fqFileName)

        self._projectInformation.fileName = fqFileName

    def untangleXml(self, xmlString: str, fqFileName: str):
        """
        Untangle the input Xml string to Ogl
        Args:
            fqFileName:  The file name from which the XML came from
            xmlString: The string with the raw XML
        """
        root:        Element = parse(xmlString)
        pyutProject: Element = root.PyutProject

        unTangleProjectInformation: UnTangleProjectInformation = UnTangleProjectInformation(fqFileName=fqFileName)

        self._projectInformation = unTangleProjectInformation.projectInformation

        for pyutDocument in pyutProject.PyutDocument:
            document: Document = self._updateCurrentDocumentInformation(pyutDocument=pyutDocument)

            self._documents[DocumentTitle(document.documentTitle)] = document

            self.logger.debug(f'{document=}')
            if document.documentType == 'CLASS_DIAGRAM':
                document.oglClasses = self._graphicClassesToOglClasses(pyutDocument=pyutDocument)
                document.oglNotes   = self._graphicNotesToOglNotes(pyutDocument=pyutDocument)
                document.oglTexts   = self._graphicalTextToOglTexts(pyutDocument=pyutDocument)

                linkableOglObjects: LinkableOglObjects = self._buildDictionary(document=document)
                document.oglLinks   = self._untangleOglLinks.unTangle(pyutDocument=pyutDocument, linkableOglObjects=linkableOglObjects)
            elif document.documentType == 'SEQUENCE_DIAGRAM':
                untangleSequenceDiagram: UnTangleSequenceDiagram = UnTangleSequenceDiagram(xmlVersion=self._xmlVersion)

                untangleSequenceDiagram.unTangle(pyutDocument=pyutDocument)
                document.oglSDInstances = untangleSequenceDiagram.oglSDInstances
                document.oglSDMessages  = untangleSequenceDiagram.oglSDMessages

            elif document.documentType == 'USECASE_DIAGRAM':

                unTangleUseCaseDiagram: UnTangleUseCaseDiagram = UnTangleUseCaseDiagram(xmlVersion=self._xmlVersion)

                unTangleUseCaseDiagram.unTangle(pyutDocument=pyutDocument)
                document.oglActors   = unTangleUseCaseDiagram.oglActors
                document.oglUseCases = unTangleUseCaseDiagram.oglUseCases
                document.oglNotes    = self._graphicNotesToOglNotes(pyutDocument=pyutDocument)
                document.oglTexts    = self._graphicalTextToOglTexts(pyutDocument=pyutDocument)

                linkableOglObjects = self._buildDictionary(document=document)
                document.oglLinks  = self._untangleOglLinks.unTangle(pyutDocument, linkableOglObjects=linkableOglObjects)
            else:
                assert False, f'Unknown document type: {document.documentType}'

    def _updateCurrentDocumentInformation(self, pyutDocument: Element) -> Document:

        documentInformation: Document = Document()

        documentTitle: DocumentTitle = DocumentTitle(pyutDocument['title'])

        documentInformation.documentType = pyutDocument['type']
        documentInformation.documentTitle = documentTitle

        documentInformation.scrollPositionX = int(pyutDocument['scrollPositionX'])
        documentInformation.scrollPositionY = int(pyutDocument['scrollPositionY'])
        documentInformation.pixelsPerUnitX  = int(pyutDocument['pixelsPerUnitX'])
        documentInformation.pixelsPerUnitY  = int(pyutDocument['pixelsPerUnitY'])

        self.logger.debug(f'{documentInformation=}')

        return documentInformation

    def _graphicClassesToOglClasses(self, pyutDocument: Element) -> UntangledOglClasses:

        unTangleOglClasses: UnTangleOglClasses  = UnTangleOglClasses(xmlVersion=self._xmlVersion)
        oglClasses:         UntangledOglClasses = unTangleOglClasses.unTangle(pyutDocument=pyutDocument)

        return oglClasses

    def _graphicNotesToOglNotes(self, pyutDocument: Element) -> UntangledOglNotes:
        """

        Args:
            pyutDocument:

        Returns: untangled OglNote objects if any exist, else an empty list
        """
        unTangleOglNotes: UnTangleOglNotes  = UnTangleOglNotes(xmlVersion=self._xmlVersion)
        oglNotes:         UntangledOglNotes = unTangleOglNotes.unTangle(pyutDocument=pyutDocument)

        return oglNotes

    def _graphicalTextToOglTexts(self, pyutDocument: Element) -> UntangledOglTexts:
        """
        Yeah, yeah, I know bad English;

        Args:
            pyutDocument:  The Element document

        Returns:  untangled OglText objects if any exist, else an empty list
        """

        unTangleOglTexts: UnTangleOglTexts  = UnTangleOglTexts(xmlVersion=self._xmlVersion)
        oglTexts:         UntangledOglTexts = unTangleOglTexts.unTangle(pyutDocument=pyutDocument)

        return oglTexts

    def _buildDictionary(self, document: Document) -> LinkableOglObjects:
        """

        Args:
            document:   The created document either Use case or class diagram

        Returns:  Linkable Objects Dictionary
        """

        linkableOglObjects: LinkableOglObjects = createLinkableOglObjects()

        for oglClass in document.oglClasses:
            linkableOglObjects[oglClass.pyutObject.id] = oglClass

        for oglNote in document.oglNotes:
            linkableOglObjects[oglNote.pyutObject.id] = oglNote

        for oglUseCase in document.oglUseCases:
            linkableOglObjects[oglUseCase.pyutObject.id] = oglUseCase

        for oglActor in document.oglActors:
            linkableOglObjects[oglActor.pyutObject.id] = oglActor

        return linkableOglObjects
