
from typing import Tuple
from typing import cast

from logging import Logger
from logging import getLogger

from math import sqrt

from wx import BLACK_PEN
from wx import EVT_MENU

from wx import CommandEvent
from wx import Menu
from wx import MenuItem
from wx import MouseEvent

from codeallybasic.Position import Position

from codeallyadvanced.ui.Common import Common
from codeallyadvanced.ui.AttachmentSide import AttachmentSide

from pyutmodelv2.PyutLink import PyutLink
from pyutmodelv2.PyutLink import PyutLinks

from miniogl.AnchorPoint import AnchorPoint
from miniogl.ControlPoint import ControlPoint
from miniogl.LinePoint import LinePoint
from miniogl.LineShape import LineShape
from miniogl.Shape import Shape
from miniogl.ShapeEventHandler import ShapeEventHandler

from ogl.EventEngineMixin import EventEngineMixin
from ogl.OglPosition import OglPosition
from ogl.IllegalOperationException import IllegalOperationException

from ogl.OglUtils import OglUtils
from ogl.events.OglEvents import OglEventType

[
    MENU_ADD_BEND,
    MENU_REMOVE_BEND,
    MENU_TOGGLE_SPLINE,
]  = OglUtils.assignID(3)

AVOID_CROSSED_LINES_FEATURE: bool = False   # Make this a feature flag


class OglLink(LineShape, ShapeEventHandler, EventEngineMixin):
    """
    A class that represents a graphical link.
    This class should be the base class for every type of link. It implements
    the following methods:

        - Link between objects
        - Position management
        - Control points (2)
        - Data layer link association
        - Source and destination objects

    You can inherit from this class to implement your favorite type of links
    like `OglAssociation`.

    There is a link factory (See `OglLinkFactory`) you can use to build
    the different types of links that exist.

    """
    clsLogger: Logger = getLogger(__name__)

    def __init__(self, srcShape, pyutLink, dstShape, srcPos=None, dstPos=None):
        """

        Args:
            srcShape: Source shape
            pyutLink: Conceptual links associated with the graphical links.
            dstShape: Destination shape
            srcPos: Position of the source object; Overrides the location of the input source
            dstPos: Position of the destination object; Overrides the location of the input destination
        """
        self._srcShape  = srcShape
        self._destShape = dstShape

        OglLink.clsLogger.debug(f'Input Override positions - srcPos: {srcPos} dstPos: {dstPos}')
        if srcPos is None and dstPos is None:
            srcX, srcY = self._srcShape.GetPosition()
            dstX, dstY = self._destShape.GetPosition()

            sourcePosition:      Position       = Position(x=srcX, y=srcY)
            destinationPosition: Position       = Position(x=dstX, y=dstY)
            orient:              AttachmentSide = Common.whereIsDestination(sourcePosition=sourcePosition, destinationPosition=destinationPosition)

            sw, sh = self._srcShape.GetSize()
            dw, dh = self._destShape.GetSize()
            if orient == AttachmentSide.NORTH:
                srcX, srcY = sw//2, 0
                dstX, dstY = dw//2, dh
            elif orient == AttachmentSide.SOUTH:
                srcX, srcY = sw//2, sh
                dstX, dstY = dw//2, 0
            elif orient == AttachmentSide.EAST:
                srcX, srcY = sw, sh//2
                dstX, dstY = 0, dh//2
            elif orient == AttachmentSide.WEST:
                srcX, srcY = 0, sh//2
                dstX, dstY = dw, dh//2

            dstX, dstY, srcX, srcY = self._avoidCrossedLines(dstShape=dstShape, dstX=dstX, dstY=dstY, orient=orient, srcShape=srcShape, srcX=srcX, srcY=srcY)
        else:
            # Use provided position
            (srcX, srcY) = srcPos
            (dstX, dstY) = dstPos

        srcAnchor: AnchorPoint = self._srcShape.AddAnchor(srcX, srcY)
        dstAnchor: AnchorPoint = self._destShape.AddAnchor(dstX, dstY)
        srcAnchor.SetPosition(srcX, srcY)
        dstAnchor.SetPosition(dstX, dstY)
        srcAnchor.visible = False
        dstAnchor.visible = False
        OglLink.clsLogger.debug(f'src anchor pos: {srcAnchor.GetPosition()} dst anchor pos {dstAnchor.GetPosition()}')
        srcAnchor.draggable = True
        dstAnchor.draggable = True
        #
        # Init
        #
        EventEngineMixin.__init__(self)
        LineShape.__init__(self, srcAnchor, dstAnchor)
        # Set up painting colors
        self.pen = BLACK_PEN
        # Keep reference to the PyutLink for mouse events,
        # Need this to find our way back to the corresponding link
        if pyutLink is not None:
            self._link = pyutLink
        else:
            self._link = PyutLink()

    @property
    def sourceShape(self):
        """
        Returns: The source shape for this link.
        """
        return self._srcShape

    @property
    def destinationShape(self):
        """

        Returns: The destination shape for this link.
        """
        return self._destShape

    @property
    def pyutObject(self) -> PyutLink:
        return self._link

    @pyutObject.setter
    def pyutObject(self, pyutLink: PyutLink):
        self._link = pyutLink

    def getAnchors(self) -> Tuple[AnchorPoint, AnchorPoint]:
        return self.sourceAnchor, self.destinationAnchor

    def Detach(self):
        """
        Detach the line and all its line points, Includes the source and the destination.
        """
        if self._diagram is not None and not self._protected:
            LineShape.Detach(self)
            self._srcAnchor.protected = False
            self._dstAnchor.protected = False
            self._srcAnchor.Detach()
            self._dstAnchor.Detach()
            self._detachFromOglEnds()
            self._detachModel()

    def optimizeLine(self):
        """
        Optimize line, so that the line length is minimized
        """
        # Get elements
        srcAnchor = self.sourceAnchor
        dstAnchor = self.destinationAnchor

        srcX, srcY = self._srcShape.GetPosition()
        dstX, dstY = self._destShape.GetPosition()

        srcSize = self._srcShape.GetSize()
        dstSize = self._destShape.GetSize()

        OglLink.clsLogger.info(f"optimizeLine - ({srcX},{srcY}) / ({dstX},{dstY})")
        # Find new positions
        # Little tips
        optimalSrcX, optimalSrcY, optimalDstX, optimalDstY = dstX, dstY, srcX, srcY

        optimalSrcX += dstSize[0] // 2
        optimalSrcY += dstSize[1] // 2
        optimalDstX += srcSize[0] // 2
        optimalDstY += srcSize[1] // 2

        srcAnchor.SetPosition(optimalSrcX, optimalSrcY)
        dstAnchor.SetPosition(optimalDstX, optimalDstY)
        self._indicateDiagramModified()

    # noinspection PyUnusedLocal
    def OnRightDown(self, event: MouseEvent):
        """
        Handle right-clicks on our UML LineShape; Overrides the base handler; It does nothing

        Args:
            event:
        """
        from ogl.sd.OglSDMessage import OglSDMessage

        if isinstance(self, OglSDMessage) is True:
            return
        menu: Menu = Menu()
        menu.Append(MENU_ADD_BEND,      'Add Bend',      'Add Bend at right click point')
        menu.Append(MENU_REMOVE_BEND,   'Remove Bend',   'Remove Bend closest to click point')
        menu.Append(MENU_TOGGLE_SPLINE, 'Toggle Spline', 'Best with at least one bend')

        if len(self._controls) == 0:
            bendItem: MenuItem = menu.FindItemById(MENU_REMOVE_BEND)
            bendItem.Enable(enable=False)

        x: int = event.GetX()
        y: int = event.GetY()
        clickPoint: Tuple[int, int] = (x, y)

        OglLink.clsLogger.debug(f'OglLink - {clickPoint=}')
        # I hate lambdas -- humberto
        menu.Bind(EVT_MENU, lambda evt, data=clickPoint: self._onMenuItemSelected(evt, data))

        frame = self._diagram.panel
        frame.PopupMenu(menu, x, y)

    # noinspection PyUnusedLocal
    def _onMenuItemSelected(self, event: CommandEvent, data):

        eventId: int = event.GetId()
        if eventId == MENU_ADD_BEND:
            self._addBend(data)
        elif eventId == MENU_REMOVE_BEND:
            self._removeBend(data)
        elif eventId == MENU_TOGGLE_SPLINE:
            self._toggleSpline()

    def _computeLinkLength(self, srcPosition: OglPosition, destPosition: OglPosition) -> int:
        """

        Returns: The length of the link between the source shape and destination shape
        """
        dx, dy = self._computeDxDy(srcPosition, destPosition)
        linkLength = round(sqrt(dx*dx + dy*dy))
        if linkLength == 0:
            linkLength = 1

        return linkLength

    def _computeDxDy(self, srcPosition: OglPosition, destPosition: OglPosition) -> Tuple[int, int]:
        """

        Args:
            srcPosition:    source position
            destPosition:   destination position

        Returns:
            A tuple of deltaX and deltaY of the shape position
        """
        if self._srcShape is None or self._destShape is None:
            raise IllegalOperationException('Either the source or the destination shape is None')

        srcX: int = srcPosition.x
        srcY: int = srcPosition.y
        dstX: int = destPosition.x
        dstY: int = destPosition.y

        dx: int = dstX - srcX
        dy: int = dstY - srcY

        return dx, dy

    def _addBend(self, clickPoint: Tuple[int, int]):

        OglLink.clsLogger.debug(f'Add a bend.  {clickPoint=}')

        x = clickPoint[0]
        y = clickPoint[1]
        cp = ControlPoint(x, y)

        cp.visible = True
        #
        # Add it either before the destinationAnchor or the sourceAnchor
        #
        lp: LinePoint = self.sourceAnchor
        self.AddControl(control=cp, after=lp)

        frame = self._diagram.panel
        frame.diagram.AddShape(cp)
        frame.Refresh()
        self._indicateDiagramModified()

    def _removeBend(self, clickPoint: Tuple[int, int]):

        OglLink.clsLogger.debug(f'Remove a bend.  {clickPoint=}')

        cp: ControlPoint = self._findClosestControlPoint(clickPoint=clickPoint)

        assert cp is not None, 'We should have previously verified there was at least one on the line'

        self._removeControl(control=cp)
        cp.Detach()
        cp.visible = False    # Work around still on screen but not visible and not saved

        frame = self._diagram.panel
        frame.Refresh()
        self._indicateDiagramModified()

    def _toggleSpline(self):

        self.spline = not self.spline

        frame = self._diagram.panel
        frame.Refresh()
        self._indicateDiagramModified()

    def _findClosestControlPoint(self, clickPoint: Tuple[int, int]) -> ControlPoint:

        controlPoints = self.GetControlPoints()

        distance:     float        = 1000.0    # Impossibly long distance
        closestPoint: ControlPoint = cast(ControlPoint, None)
        srcPosition:  OglPosition  = OglPosition(x=clickPoint[0], y=clickPoint[1])

        for controlPoint in controlPoints:
            xy:    Tuple[int, int] = controlPoint.GetPosition()
            destX: int = xy[0]
            destY: int = xy[1]
            destPosition: OglPosition = OglPosition(x=destX, y=destY)

            dx, dy = self._computeDxDy(srcPosition, destPosition)
            currentDistance = sqrt(dx*dx + dy*dy)
            self.clsLogger.debug(f'{currentDistance=}')
            if currentDistance <= distance:
                distance = currentDistance
                closestPoint = cast(ControlPoint, controlPoint)

        return closestPoint

    def _indicateDiagramModified(self):
        if self.eventEngine is not None:  # we might not be associated with a diagram yet
            self.eventEngine.sendEvent(OglEventType.DiagramFrameModified)

    def _detachModel(self):
        """
        From the data model of the source remove the
        data model link
        """
        from typing import Union
        from pyutmodelv2.PyutClass import PyutClass
        from pyutmodelv2.PyutNote import PyutNote
        try:
            # self._link.getSource().links.remove(self._link)
            pyutSrc: Union[PyutClass, PyutNote] = self._link.source
            links: PyutLinks = pyutSrc.links
            links.remove(self._link)
        except ValueError as ve:
            self.clsLogger.warning(f'Ignoring source removal error: {ve}')

    def _detachFromOglEnds(self):
        """
        Remove us (self) from the list of links in each of the ends

        """
        # Do local imports because of these incestuous self-references
        from typing import Union
        from typing import List
        from ogl.OglClass import OglClass
        from ogl.OglNote import OglNote
        try:
            src: Union[OglClass, OglNote] = self.sourceShape
            links: List[OglLink] = src.links
            links.remove(self)
        except ValueError as ve:
            self.clsLogger.warning(f'Ignoring source removal error: {ve}')

        try:
            dest: Union[OglClass, OglNote] = self.destinationShape
            links = dest.links
            links.remove(self)
        except ValueError as ee:
            self.clsLogger.warning(f'Ignoring destination removal error: {ee}')

    def __repr__(self):

        srcShape: Shape = self.sourceShape
        dstShape: Shape = self.destinationShape
        sourceId: int   = srcShape.id
        dstId:    int   = dstShape.id

        return f'from: id: {sourceId} {srcShape} to id: {dstId} {dstShape}'

    def _avoidCrossedLines(self, dstShape, dstX: int, dstY: int, orient, srcShape, srcX: int, srcY: int):
        """
        Avoid over-lining
        (still experimental in 2024

        Args:
            dstShape:
            dstX:
            dstY:
            orient:
            srcShape:
            srcX:
            srcY:

        Returns: Adjust points if feature us turned on
        """
        if AVOID_CROSSED_LINES_FEATURE is True:
            lstAnchorsPoints = [anchor.GetRelativePosition() for anchor in srcShape.GetAnchors()]
            while (srcX, srcY) in lstAnchorsPoints:
                OglLink.clsLogger.warning(f'Over-lining in source shape: {srcShape.pyutObject}')
                if orient == AttachmentSide.NORTH or orient == AttachmentSide.SOUTH:
                    srcX += 10
                else:
                    srcY += 10
            lstAnchorsPoints = [anchor.GetRelativePosition() for anchor in dstShape.GetAnchors()]
            while (dstX, dstY) in lstAnchorsPoints:
                OglLink.clsLogger.warning(f'Over-lining in destination shape: {dstShape.pyutObject}')
                if orient == AttachmentSide.NORTH or orient == AttachmentSide.SOUTH:
                    dstX += 10
                else:
                    dstY += 10

        return dstX, dstY, srcX, srcY
