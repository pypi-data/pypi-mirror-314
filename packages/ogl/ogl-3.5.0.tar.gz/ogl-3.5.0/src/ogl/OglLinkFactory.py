
from typing import cast

from logging import Logger
from logging import getLogger

from codeallybasic.SingletonV3 import SingletonV3

from pyutmodelv2.enumerations.PyutLinkType import PyutLinkType

from ogl.OglAssociation import OglAssociation
from ogl.OglAggregation import OglAggregation
from ogl.OglComposition import OglComposition
from ogl.OglInheritance import OglInheritance
from ogl.OglInterface import OglInterface
from ogl.OglNoteLink import OglNoteLink

from ogl.sd.OglSDMessage import OglSDMessage


def getOglLinkFactory():
    """
    Function to get the unique OglLinkFactory instance (singleton).
    """
    return OglLinkFactory()


def getLinkType(link: OglAssociation) -> PyutLinkType:
    """

    Args:
        link:   The OglLink object

    Returns:  The OglLinkType

    """
    match link:
        case OglAggregation():
            return PyutLinkType.AGGREGATION
        case OglComposition():
            return PyutLinkType.COMPOSITION
        case OglInheritance():
            return PyutLinkType.INHERITANCE
        case OglAssociation():
            return PyutLinkType.ASSOCIATION
        case OglInterface():
            return PyutLinkType.INTERFACE
        case OglNoteLink():
            return PyutLinkType.NOTELINK
        case _:
            print(f"Unknown OglLink: {link}")
            return cast(PyutLinkType, None)


class OglLinkFactory(metaclass=SingletonV3):
    """
    This class is a factory to produce `OglLink` objects.
    It works under the Factory Design Pattern model. Ask for a link
    from this object, and it will return an instance of request link.
    """
    def __init__(self):

        self.logger: Logger = getLogger(__name__)

    def getOglLink(self, srcShape, pyutLink, destShape, linkType: PyutLinkType):
        """
        Used to get an OglLink of the given linkType.

        Args:
            srcShape:   Source shape
            pyutLink:   Conceptual links associated with the graphical links.
            destShape:  Destination shape
            linkType:   The linkType of the link (OGL_INHERITANCE, ...)

        Returns:  The requested link
        """
        match linkType:
            case PyutLinkType.AGGREGATION:
                oglAggregation: OglAggregation = OglAggregation(srcShape, pyutLink, destShape)
                oglAggregation.createDefaultAssociationLabels()
                return oglAggregation

            case PyutLinkType.COMPOSITION:
                oglComposition: OglComposition = OglComposition(srcShape, pyutLink, destShape)
                oglComposition.createDefaultAssociationLabels()
                return oglComposition

            case PyutLinkType.INHERITANCE:
                return OglInheritance(srcShape, pyutLink, destShape)

            case PyutLinkType.ASSOCIATION:
                oglAssociation: OglAssociation = OglAssociation(srcShape, pyutLink, destShape)
                oglAssociation.createDefaultAssociationLabels()
                return oglAssociation

            case PyutLinkType.INTERFACE:
                return OglInterface(srcShape, pyutLink, destShape)

            case PyutLinkType.NOTELINK:
                return OglNoteLink(srcShape, pyutLink, destShape)

            case PyutLinkType.SD_MESSAGE:
                return OglSDMessage(srcSDInstance=srcShape, pyutSDMessage=pyutLink, dstSDInstance=destShape)
            case _:
                self.logger.error(f"Unknown PyutLinkType: {linkType}")
                return None
