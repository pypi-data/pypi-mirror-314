
from logging import Logger
from logging import getLogger

from wx import WHITE_BRUSH

from pyutmodelv2.PyutLink import PyutLink

from miniogl.Shape import Shape

from ogl.OglClass import OglClass
from ogl.OglLink import OglLink


class OglInheritance(OglLink):
    """
    Graphical OGL representation of an inheritance link.
    This class provide the methods for drawing an inheritance link between
    two classes of a UML diagram. Add labels to an OglLink.
    """
    def __init__(self, srcShape: OglClass, pyutLink: PyutLink, dstShape: OglClass, srcPos=None, dstPos=None):
        """

        Args:
            srcShape: Source shape
            pyutLink: Conceptual links associated with the graphical links.
            dstShape: Destination shape
            srcPos:   Position of source      Override location of input source
            dstPos:   Position of destination Override location of input destination
        """
        super().__init__(srcShape, pyutLink, dstShape, srcPos=srcPos, dstPos=dstPos)

        self.logger: Logger = getLogger(__name__)
        # Arrow must be white inside
        self.brush = WHITE_BRUSH
        self.drawArrow = True

    def __repr__(self):
        srcShape:  Shape = self.sourceShape
        dstShape:  Shape = self.destinationShape
        sourceId:  int   = srcShape.id
        dstId:     int   = dstShape.id
        return f'OglInheritance[from: id: {sourceId} {srcShape} to: id: {dstId} {dstShape}]'
