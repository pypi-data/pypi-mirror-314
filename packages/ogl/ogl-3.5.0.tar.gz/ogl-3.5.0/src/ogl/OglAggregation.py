
from logging import Logger
from logging import getLogger

from wx import DC

from ogl.OglAssociation import OglAssociation


class OglAggregation(OglAssociation):
    """
    Graphical link representation of aggregation, (empty diamond, arrow).
    To get a new link, you should use the `OglLinkFactory` and specify
    the kind of link you want, OGL_AGGREGATION for an instance of this class.
    """

    def __init__(self, srcShape, pyutLink, dstShape, srcPos=None, dstPos=None):
        """

        Args:
            srcShape:   Source shape
            pyutLink:   Conceptual links associated with the graphical links.
            dstShape:   Destination shape
            srcPos:     Position of source      Override location of input source
            dstPos:     Position of destination Override location of input destination
        """
        super().__init__(srcShape, pyutLink, dstShape, dstPos=dstPos, srcPos=srcPos)

        self.logger: Logger = getLogger(__name__)
        self.drawArrow = True

    def Draw(self, dc: DC, withChildren: bool = False):
        """
        Called to draw link contents
        Args:
            dc:     The device context
            withChildren:  Should we draw children
        """
        super().Draw(dc, withChildren)

        # Draw diamond
        self.drawDiamond(dc, False)

    def __repr__(self):
        from ogl.OglLink import OglLink
        return f'OglAggregation - {OglLink.__repr__(self)}'
