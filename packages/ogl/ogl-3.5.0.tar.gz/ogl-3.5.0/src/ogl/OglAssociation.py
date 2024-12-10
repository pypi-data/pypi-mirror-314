
from typing import Callable
from typing import cast
from typing import List
from typing import NewType
from typing import Tuple

from logging import Logger
from logging import getLogger
from logging import DEBUG

from math import pi
from math import atan
from math import cos
from math import sin

from wx import BLACK_BRUSH
from wx import BLACK_PEN
from wx import DC
from wx import FONTFAMILY_DEFAULT
from wx import FONTSTYLE_NORMAL
from wx import FONTWEIGHT_NORMAL
from wx import WHITE_BRUSH

from wx import Font

from pyutmodelv2.PyutLink import PyutLink

from miniogl.LineShape import Segments

from ogl.OglAssociationLabel import OglAssociationLabel
from ogl.OglLink import OglLink
from ogl.OglPosition import OglPosition

from ogl.preferences.OglPreferences import OglPreferences

DiamondPoint    = NewType('DiamondPoint', Tuple[int, int])
DiamondPoints   = NewType('DiamondPoints', List[DiamondPoint])
"""
The compute function calculates a position for a cardinality label
The parameters are the dx,dy of the source and anchor points and the link length
returns OglPosition
"""
ComputeFunction = Callable[[int, int, int], OglPosition]

PI_6:         float = pi / 6


class OglAssociation(OglLink):

    clsDiamondSize: int = OglPreferences().diamondSize
    """
    Graphical link representation of an association, (simple line, no arrow).
    To get a new link,  use the `OglLinkFactory` and specify
    the link type.  .e.g. OGL_ASSOCIATION for an instance of this class.
    """
    def __init__(self, srcShape, pyutLink, dstShape, srcPos=None, dstPos=None):
        """

        Args:
            srcShape:   Source shape
            pyutLink:   Conceptual links associated with the graphical links.
            dstShape:   Destination shape
            srcPos:     Source position  Override location of input source
            dstPos:     Destination position Override location of input destination
        """
        self.oglAssociationLogger: Logger         = getLogger(__name__)
        self._preferences:         OglPreferences = OglPreferences()

        super().__init__(srcShape, pyutLink, dstShape, srcPos=srcPos, dstPos=dstPos)

        self._defaultFont: Font = Font(self._preferences.associationTextFontSize, FONTFAMILY_DEFAULT, FONTSTYLE_NORMAL, FONTWEIGHT_NORMAL)

        self._associationName:        OglAssociationLabel = cast(OglAssociationLabel, None)
        self._sourceCardinality:      OglAssociationLabel = cast(OglAssociationLabel, None)
        self._destinationCardinality: OglAssociationLabel = cast(OglAssociationLabel, None)

        self.drawArrow = False

    @property
    def pyutObject(self) -> PyutLink:
        """
        Override
        Returns:  The data model
        """
        return self._link

    @pyutObject.setter
    def pyutObject(self, pyutLink: PyutLink):
        """

        Args:
            pyutLink:
        """
        self.oglAssociationLogger.debug(f'{pyutLink=}')
        self._link = pyutLink
        self.centerLabel.text            = pyutLink.name
        self.sourceCardinality.text      = pyutLink.sourceCardinality
        self.destinationCardinality.text = pyutLink.destinationCardinality

        self.oglAssociationLogger.debug(f'{self.centerLabel=}')

    @property
    def centerLabel(self) -> OglAssociationLabel:
        return self._associationName

    @centerLabel.setter
    def centerLabel(self, newValue: OglAssociationLabel):
        self._associationName = newValue

    @property
    def sourceCardinality(self) -> OglAssociationLabel:
        return self._sourceCardinality

    @sourceCardinality.setter
    def sourceCardinality(self, newValue: OglAssociationLabel):
        self._sourceCardinality = newValue

    @property
    def destinationCardinality(self) -> OglAssociationLabel:
        return self._destinationCardinality

    @destinationCardinality.setter
    def destinationCardinality(self, newValue: OglAssociationLabel):
        self._destinationCardinality = newValue

    def Draw(self, dc: DC, withChildren: bool = True):
        """
        Called to draw the link content.
        We are going to draw all of our stuff, cardinality, Link name, etc.

        Args:
            dc:     Device context
            withChildren:   draw the children or not
        """
        OglLink.Draw(self, dc, withChildren)

        if self._associationName is not None:
            self._associationName.text = self._link.name

        if self._sourceCardinality is not None:
            self._sourceCardinality.text = self._link.sourceCardinality
            self.oglAssociationLogger.debug(f'{self._sourceCardinality.GetPosition()=}')

        if self._destinationCardinality is not None:
            self._destinationCardinality.text = self._link.destinationCardinality
            self.oglAssociationLogger.debug(f'{self._destinationCardinality.GetPosition()=}')

    def createDefaultAssociationLabels(self):
        sp: Tuple[int, int] = self._srcAnchor.GetPosition()
        dp: Tuple[int, int] = self._dstAnchor.GetPosition()
        oglDp: OglPosition = self._computeDestinationPosition(sp=OglPosition.tupleToOglPosition(sp), dp=OglPosition.tupleToOglPosition(dp))

        oglSp: OglPosition = OglPosition(x=sp[0], y=sp[1])

        self._createAssociationName()
        self._createSourceCardinality(sp=oglSp)
        self._createDestinationCardinality(dp=oglDp)

    def drawDiamond(self, dc: DC, filled: bool = False):
        """
        Draw an arrow at the beginning of the line.

        Args:
            dc:         The device context
            filled:     True if the diamond must be filled, False otherwise
        """
        #
        line: Segments = self.segments

        # self.oglAssociationLogger.debug(f'{line=}')
        points: DiamondPoints = OglAssociation.calculateDiamondPoints(lineSegments=line)
        # self.oglAssociationLogger.debug(f'{points:}')

        dc.SetPen(BLACK_PEN)
        if filled:
            dc.SetBrush(BLACK_BRUSH)
        else:
            dc.SetBrush(WHITE_BRUSH)
        dc.DrawPolygon(points)
        dc.SetBrush(WHITE_BRUSH)

    def _createAssociationName(self):
        """
        Create association name text shape;
        """
        if self._link.name is None:
            self._link.name = ''
        self._associationName = self._createAssociationLabel(x=0, y=0, text=self._link.name, font=self._defaultFont)

    def _createSourceCardinality(self, sp: OglPosition):

        if self._link.sourceCardinality is None:
            self._link.sourceCardinality = ''
        self._sourceCardinality = self._createAssociationLabel(x=sp.x, y=sp.y, text=self._link.sourceCardinality, font=self._defaultFont)

        srcX, srcY = self._sourceCardinality.ConvertCoordToRelative(x=sp.x, y=sp.y)
        self._sourceCardinality.SetRelativePosition(x=srcX, y=srcY)

    def _createDestinationCardinality(self, dp: OglPosition):
        if self._link.destinationCardinality is None:
            self._link.destinationCardinality = ''
        self._destinationCardinality = self._createAssociationLabel(x=dp.x, y=dp.y, text=self._link.destinationCardinality, font=self._defaultFont)

        dstX, dstY = self._destinationCardinality.ConvertCoordToRelative(x=dp.x, y=dp.y)
        self._destinationCardinality.SetRelativePosition(x=dstX, y=dstY)

    def _computeDestinationPosition(self, sp: OglPosition, dp: OglPosition) -> OglPosition:

        def computeDestination(dx, dy, linkLength) -> OglPosition:
            x: int = round((-20 * dx / linkLength + dx * 5 / linkLength) + dp.x)
            y: int = round((-20 * dy / linkLength - dy * 5 / linkLength) + dp.y)

            return OglPosition(x=x, y=y)

        return self._computePosition(sp=sp, dp=dp, computeFunction=computeDestination)

    def _computeSourcePosition(self, sp: OglPosition, dp: OglPosition) -> OglPosition:

        def computeSource(dx, dy, linkLength):
            x: int = round((20 * dx / linkLength - dx * 5 / linkLength) + sp.x)
            y: int = round((20 * dy / linkLength + dy * 5 / linkLength) + sp.y)

            return OglPosition(x=x, y=y)

        return self._computePosition(sp=sp, dp=dp, computeFunction=computeSource)

    def _computePosition(self, sp: OglPosition, dp: OglPosition, computeFunction: ComputeFunction) -> OglPosition:

        dx, dy          = self._computeDxDy(srcPosition=sp, destPosition=dp)
        linkLength: int = self._computeLinkLength(srcPosition=sp, destPosition=dp)

        oglPosition: OglPosition = computeFunction(dx, dy, linkLength)

        if self.oglAssociationLogger.isEnabledFor(DEBUG):
            info = (
                f'{sp=} '
                f'{dp=} '
                f'{dx=} '
                f'{dy=} '
                f'linkLength={linkLength:.2f} '
                f'{oglPosition=}'
            )
            self.oglAssociationLogger.debug(info)
        return oglPosition

    def _createAssociationLabel(self, x: int, y: int, text: str, font: Font = None) -> OglAssociationLabel:
        """
        Create an association label and add it to the diagram.

        Args:
            x,: position of the text, relative to the origin of the shape
            y : position of the text, relative to the origin of the shape
            text: text to add
            font: font to use

        Returns:  AssociationLabel : the created shape
        """
        oglAssociationLabel: OglAssociationLabel = OglAssociationLabel(x, y, text, parent=self, font=font)
        if self._diagram is not None:
            self._diagram.AddShape(oglAssociationLabel)
        self.oglAssociationLogger.info(f'_createAssociationLabel - {oglAssociationLabel=} added at {x=} {y=}')

        oglAssociationLabel.draggable = True
        return oglAssociationLabel

    @staticmethod
    def calculateDiamondPoints(lineSegments: Segments) -> DiamondPoints:
        """
        Made static so that we can unit test it;  Only instance variables needed
        are passed in

        Args:
            lineSegments:  The line where we are putting the diamondPoints

        Returns:  The diamond points that define the diamond polygon
        """
        x1, y1 = lineSegments[1]
        x2, y2 = lineSegments[0]
        a: int = x2 - x1
        b: int = y2 - y1
        if abs(a) < 0.01:  # vertical segment
            if b > 0:
                alpha: float = -pi / 2
            else:
                alpha = pi / 2
        else:
            if a == 0:
                if b > 0:
                    alpha = pi / 2
                else:
                    alpha = 3 * pi / 2
            else:
                alpha = atan(b/a)
        if a > 0:
            alpha += pi
        alpha1: float = alpha + PI_6
        alpha2: float = alpha - PI_6

        diamondPoints: DiamondPoints = DiamondPoints([])

        dp0: DiamondPoint = OglAssociation.calculateDiamondPoint0(x2=x2, y2=y2, alpha1=alpha1)
        diamondPoints.append(dp0)

        diamondPoints.append(DiamondPoint((x2, y2)))

        dp2: DiamondPoint = OglAssociation.calculateDiamondPoint2(x2=x2, y2=y2, alpha2=alpha2)
        diamondPoints.append(dp2)

        dp3: DiamondPoint = OglAssociation.calculateDiamondPoint3(x2=x2, y2=y2, alpha=alpha)
        diamondPoints.append(dp3)

        return diamondPoints

    @classmethod
    def calculateDiamondPoint0(cls, x2: float, y2: float, alpha1: float) -> DiamondPoint:

        dpx0: float = x2 + OglAssociation.clsDiamondSize * cos(alpha1)
        dpy0: float = y2 + OglAssociation.clsDiamondSize * sin(alpha1)

        return DiamondPoint((round(dpx0), round(dpy0)))

    @classmethod
    def calculateDiamondPoint2(cls, x2: float, y2: float, alpha2: float) -> DiamondPoint:

        dpx2: float = x2 + OglAssociation.clsDiamondSize * cos(alpha2)
        dpy2: float = y2 + OglAssociation.clsDiamondSize * sin(alpha2)

        return DiamondPoint((round(dpx2), round(dpy2)))

    @classmethod
    def calculateDiamondPoint3(cls, x2: float, y2: float, alpha: float) -> DiamondPoint:

        dpx3: float = x2 + 2 * OglAssociation.clsDiamondSize * cos(alpha)
        dpy3: float = y2 + 2 * OglAssociation.clsDiamondSize * sin(alpha)

        return DiamondPoint((round(dpx3), round(dpy3)))

    def __repr__(self):
        return f'OglAssociation - {super().__repr__()}'
