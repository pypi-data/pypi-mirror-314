
from logging import Logger
from logging import getLogger

from wx import Brush
from wx import DC
from wx import Pen

from wx import PENSTYLE_SHORT_DASH
from wx import PENSTYLE_LONG_DASH
from wx import RED_PEN
from wx import BLACK_PEN
from wx import WHITE_BRUSH

from pyutmodelv2.PyutLink import PyutLink

from miniogl.TextShape import TextShape

from ogl.OglLink import OglLink
from ogl.OglClass import OglClass


class OglInterface(OglLink):
    """
    Graphical OGL representation of an interface link.
    This class provide the methods for drawing an interface link between
    two classes of an UML diagram. Add labels to an OglLink.
    """
    clsLogger: Logger = getLogger(__name__)

    def __init__(self, srcShape: OglClass, pyutLink: PyutLink, dstShape: OglClass, srcPos=None, dstPos=None):
        """

        Args:
            srcShape:  Source shape
            pyutLink:  Conceptual links associated with the graphical links.
            dstShape:  Destination shape
            srcPos:    Position of source      Override location of input source
            dstPos:    Position of destination Override location of input destination

        """
        super().__init__(srcShape, pyutLink, dstShape, srcPos=srcPos, dstPos=dstPos)

        self.pen:    Pen       = Pen("BLACK", 1, PENSTYLE_LONG_DASH)
        self.brush:  Brush     = WHITE_BRUSH
        self._label: TextShape = self.AddText(0, 0, "")

        # Initialize label objects
        self.updateLabels()
        self.drawArrow = True

    @property
    def label(self) -> TextShape:
        return self._label

    def updateLabels(self):
        """
        Update the labels according to the link.
        """
        def prepareLabel(textShape: TextShape, text):
            # If label should be drawn
            if text.strip() != "":
                textShape.text = text
                textShape.visible = True
            else:
                textShape.visible = False

        # Prepares labels
        prepareLabel(self._label, self._link.name)

    def Draw(self, dc: DC, withChildren: bool = True):
        """
        Called for drawing of interface links.
        OglLink drew regular lines
        I need dashed lines for an interface

        Args:
            dc: Device context
            withChildren:   Draw the children or not

        """
        self.updateLabels()
        if self._visible:
            line = self.segments
            if self._selected:
                dc.SetPen(RED_PEN)

            if self._spline:
                dc.DrawSpline(line)
            else:
                pen: Pen = dc.GetPen()              #
                pen.SetStyle(PENSTYLE_SHORT_DASH)   # This is what is different from OglLink.Draw(..)
                dc.SetPen(pen)                      #
                dc.DrawLines(line)

            for control in self._controls:
                control.Draw(dc)

            if self._selected:
                self._srcAnchor.Draw(dc)
                self._dstAnchor.Draw(dc)
            dc.SetPen(BLACK_PEN)

            if self._drawArrow:
                u, v = line[-2], line[-1]
                self.DrawArrow(dc, u, v)

            if withChildren is True:
                self.DrawChildren(dc)

    def __repr__(self):
        return f'OglInterface - {super().__repr__()}'
