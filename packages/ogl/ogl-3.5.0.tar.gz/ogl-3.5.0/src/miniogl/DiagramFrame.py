
from typing import Tuple
from typing import cast
from typing import List

from logging import Logger
from logging import getLogger

from wx import Colour
from wx import Rect
from wx import WHITE

from wx import EVT_LEFT_DCLICK
from wx import EVT_LEFT_DOWN
from wx import EVT_LEFT_UP
from wx import EVT_MIDDLE_DCLICK
from wx import EVT_MIDDLE_DOWN
from wx import EVT_MIDDLE_UP
from wx import EVT_MOTION
from wx import EVT_PAINT
from wx import EVT_RIGHT_DCLICK
from wx import EVT_RIGHT_DOWN
from wx import EVT_RIGHT_UP

from wx import FONTFAMILY_DEFAULT
from wx import FONTSTYLE_NORMAL
from wx import FONTWEIGHT_NORMAL
from wx import ID_ANY
from wx import SUNKEN_BORDER
from wx import TRANSPARENT_BRUSH

from wx import Bitmap
from wx import EmptyBitmap
from wx import Brush
from wx import ClientDC
from wx import DC
from wx import Dialog
from wx import PaintDC
from wx import PaintEvent
from wx import ScrolledWindow
from wx import Size
from wx import MemoryDC
from wx import MouseEvent
from wx import NullBitmap
from wx import Font
from wx import Window
from wx import Pen
from wx import PenInfo

# I know it is there
# noinspection PyUnresolvedReferences
from wx.core import PenStyle

from miniogl.Diagram import Diagram
from miniogl.Shape import Shapes
from miniogl.Shape import Shape
from miniogl.SizerShape import SizerShape
from miniogl.ControlPoint import ControlPoint
from miniogl.RectangleShape import RectangleShape
from miniogl.MiniOglColorEnum import MiniOglColorEnum
from miniogl.MiniOglPenStyle import MiniOglPenStyle
from miniogl.ShapeEventHandler import ShapeEventHandler
from miniogl.DlgDebugDiagramFrame import DlgDebugDiagramFrame

from ogl.events.IOglEventEngine import IOglEventEngine
from ogl.events.OglEventEngine import OglEventEngine

from ogl.preferences.OglPreferences import OglPreferences


class DiagramFrame(ScrolledWindow):
    """
    A frame to draw UML diagrams.
    This frame also manages all mouse events.
    It has a Diagram that is automatically associated.

    Note:  This really seems more like an OGL class rather than a miniogl class; Notice,
    GenericHandler depends on the ShapeEventHandler pseudo interface;  That is one of the
    base classes for OglObject
    """
    DEFAULT_FONT_SIZE: int = 12

    def __init__(self, parent: Window):
        """

        Args:
            parent:  parent window
        """
        super().__init__(parent, style=SUNKEN_BORDER)

        self._dfLogger: Logger = getLogger(__name__)

        self._diagram = Diagram(self)

        self.__keepMoving:    bool        = False
        self._selectedShapes: Shapes = Shapes([])        # The list of selected shapes

        self._lastMousePosition: Tuple[int, int] = cast(Tuple[int, int], None)
        self._selector:          RectangleShape  = cast(RectangleShape, None)     # rectangle selector shape

        self._clickedShape: Shape = cast(Shape, None)      # last clicked shape
        self._moving:       bool  = False     # a drag has been initiated

        self._xOffset:   int       = 0   # abscissa offset between the view and the model
        self._yOffset:   int       = 0   # ordinate offset between the view and the model
        self._zoomStack: List[float] = []    # store all zoom factors applied

        self._minLevelZoom:  int = 0
        self._zoomLevel:     int = 0           # number of zoom factors applied
        self._maxZoomFactor: float = 6         # can zoom in beyond 600%
        self._minZoomFactor: float = 0.2       # can zoom out beyond 20%

        self._defaultZoomFactor: float = 1.5   # used when only a point is selected

        # margins define a perimeter around the work area that must remain
        # blank and hidden. if we scroll beyond the limits, the diagram is
        # resized.
        # self._leftMargin   = DEFAULT_MARGIN_VALUE
        # self._rightMargin  = DEFAULT_MARGIN_VALUE
        # self._topMargin    = DEFAULT_MARGIN_VALUE
        # self._bottomMargin = DEFAULT_MARGIN_VALUE
        self._isInfinite: bool = False    # Indicates if the frame is infinite

        # paint related
        w, h = self.GetSize()
        self.__workingBitmap    = Bitmap(w, h)   # double buffering
        self.__backgroundBitmap = Bitmap(w, h)

        self._defaultFont = Font(DiagramFrame.DEFAULT_FONT_SIZE, FONTFAMILY_DEFAULT, FONTSTYLE_NORMAL, FONTWEIGHT_NORMAL)
        self.SetBackgroundColour(WHITE)

        self._prefs:          OglPreferences  = OglPreferences()
        self._oglEventEngine: IOglEventEngine = OglEventEngine(listeningWindow=self)

        # Mouse events
        self.Bind(EVT_LEFT_DOWN,     self.OnLeftDown)
        self.Bind(EVT_LEFT_UP,       self.OnLeftUp)
        self.Bind(EVT_LEFT_DCLICK,   self.OnLeftDClick)
        self.Bind(EVT_MIDDLE_DOWN,   self.OnMiddleDown)
        self.Bind(EVT_MIDDLE_UP,     self.OnMiddleUp)
        self.Bind(EVT_MIDDLE_DCLICK, self.OnMiddleDClick)
        self.Bind(EVT_RIGHT_DOWN,    self.OnRightDown)
        self.Bind(EVT_RIGHT_UP,      self.OnRightUp)
        self.Bind(EVT_RIGHT_DCLICK,  self.OnRightDClick)
        self.Bind(EVT_PAINT,         self.OnPaint)

        if self._prefs.debugDiagramFrame is True:

            self._debugDialog: DlgDebugDiagramFrame = DlgDebugDiagramFrame(self, ID_ANY)
            self._debugDialog.startMonitor()
            self._debugDialog.Show(True)

    @property
    def diagram(self) -> Diagram:
        """
        Returns:  The diagram associated with this frame
        """
        return self._diagram

    @diagram.setter
    def diagram(self, diagram: Diagram):
        """
        Associates a new diagram with the frame
        Args:
            diagram:
        """
        self._diagram = diagram

    @property
    def currentZoom(self) -> float:
        """
        Returns:  the global current zoom factor.
        """
        zoom = 1.0
        for z in self._zoomStack:
            zoom *= z
        return zoom

    @property
    def xOffSet(self) -> int:
        """
        Returns:          Returns: the x offset between the model and the shapes view (MVC)
        """
        return self._xOffset

    @xOffSet.setter
    def xOffSet(self, newValue: int):
        self._xOffset = newValue

    @property
    def yOffSet(self) -> int:
        """
        Returns:    the y offset between the model and the view of the shapes (MVC)
        """
        return self._yOffset

    @yOffSet.setter
    def yOffSet(self, newValue: int):
        self._yOffset = newValue

    @property
    def defaultZoomFactor(self) -> float:
        return self._defaultZoomFactor

    @defaultZoomFactor.setter
    def defaultZoomFactor(self, newValue: float):
        self._defaultZoomFactor = newValue

    @property
    def minZoomFactor(self) -> float:
        return self._minZoomFactor

    @minZoomFactor.setter
    def minZoomFactor(self, newValue: float):
        self._minZoomFactor = newValue

    @property
    def maxZoomFactor(self) -> float:
        return self._maxZoomFactor

    @maxZoomFactor.setter
    def maxZoomFactor(self, newValue: float):
        self._maxZoomFactor = newValue

    @property
    def eventEngine(self) -> IOglEventEngine:
        return self._oglEventEngine

    @property
    def selectedShapes(self):
        """
        Get the selected shapes.

        Beware, this is the list of the frame, but other shapes could be
        selected and not declared to the frame.

        Returns:  The selected shapes
        """
        return self._selectedShapes

    @selectedShapes.setter
    def selectedShapes(self, shapes: List[Shape]):
        """
        Set the list of selected shapes.

        Args:
            shapes:
        """
        self._selectedShapes = shapes

    def getEventPosition(self, event: MouseEvent):
        """
        Return the position of a click in the diagram.
        Args:
            event:   The mouse event

        Returns: A tuple with x,y coordinates
        """
        x, y = self._ConvertEventCoordinates(event)  # Updated by CD, 20041005
        return x, y

    def GenericHandler(self, event: MouseEvent, methodName: str):
        """
        This handler finds the shape at event coordinates and dispatches the event.
        The handler will receive an event with coordinates already scrolled.

        Args:
            event:      The original event
            methodName: Name of the method to invoke in the event handler of the shape

        Returns:  The clicked shape
        """
        x, y = self.getEventPosition(event)
        shape = self.FindShape(x, y)
        event.m_x, event.m_y = x, y

        # Is the shape found a ShapeEventHandler ?
        if shape is not None and isinstance(shape, ShapeEventHandler):
            self._dfLogger.info(f'GenericHandler - `{shape=}` `{methodName=}` x,y: {x},{y}')
            getattr(shape, methodName)(event)
        else:
            event.Skip()

        return shape

    def OnLeftDown(self, event: MouseEvent):
        """
        Callback for left down events on the diagram.

        Args:
            event:
        """
        self._dfLogger.debug("DiagramFrame.OnLeftDown")

        #
        # First, call the generic handler for OnLeftDown
        #
        shape: ShapeEventHandler = self.GenericHandler(event, "OnLeftDown")

        self._clickedShape = cast(Shape, shape)  # store the last clicked shape
        if not event.GetSkipped():
            self._dfLogger.debug(f'{event.GetSkipped()=}')
            return
        if shape is None:
            self._BeginSelect(event)
            return

        # manage click and drag
        x, y = event.GetX(), event.GetY()
        self._lastMousePosition = (x, y)

        realShape: Shape = cast(Shape, shape)
        if not event.ControlDown() and not realShape.selected:
            shapes = self._diagram.shapes       # Get a copy
            shapes.remove(shape)

            if isinstance(shape, SizerShape):
                # don't deselect the parent of a sizer
                # or the parent sizer is detached
                self._dfLogger.debug(f'Remove parent from copy of shapes')
                shapes.remove(shape.parent)
            elif isinstance(shape, ControlPoint):
                # don't deselect the line of a control point
                self._dfLogger.debug(f'{shape=}')
                for line in shape.lines:
                    shapes.remove(line)
            # do not call DeselectAllShapes, because we must ensure that
            # the sizer won't be deselected (because they are detached when they are deselected)
            # deselect every other shape
            for s in shapes:
                s.selected = False
                s.moving   = False

            self._selectedShapes = [cast(Shape, shape)]
            cast(Shape, shape).selected = True
            cast(Shape, shape).moving   = True
            self._dfLogger.debug(f'{shape} selected')
            self._clickedShape = cast(Shape, None)
            self.Refresh()

        self.Bind(EVT_MOTION, self.OnMove)

    def OnLeftUp(self, event: MouseEvent):
        """
        Callback for left up events.

        Args:
            event:
        """
        if self._selector is not None:
            self.Unbind(EVT_MOTION)
            self._dfLogger.debug(f'{self._selector=}')
            rect = self._selector

            for shape in self._diagram.shapes:
                x0, y0 = shape.topLeft
                w0, h0 = shape.GetSize()

                if shape.parent is None and self._isShapeInRectangle(rect, x0=x0, y0=y0, w0=w0, h0=h0):
                    shape.selected = True
                    shape.moving   = True
                    self._selectedShapes.append(shape)
            rect.Detach()
            self._selector = cast(RectangleShape, None)

        if not self._moving and self._clickedShape:
            self._dfLogger.debug(f'{self._moving} {self._clickedShape}')
            clicked = self._clickedShape
            if not event.ControlDown():
                self.DeselectAllShapes()
                self._selectedShapes = [clicked]
                clicked.selected = True
                clicked.moving   = True
            else:
                sel: bool = not clicked.selected
                clicked.selected = sel
                clicked.moving   = sel
                if sel and clicked not in self._selectedShapes:
                    self._selectedShapes.append(clicked)
                elif not sel and clicked in self._selectedShapes:
                    self._selectedShapes.remove(clicked)
            self._clickedShape = cast(Shape, None)
            self.Refresh()

        self._moving = False

        # normal event management
        self.GenericHandler(event, "OnLeftUp")
        if not self.__keepMoving:
            self.Unbind(EVT_MOTION)
            self.Refresh()

    def OnDrag(self, event: MouseEvent):
        """
        Callback to drag the selected shapes.

        Args:
            event:
        """
        x, y = event.GetX(), event.GetY()
        self._dfLogger.debug(f'dragging: ({x},{y})')

        if not self._moving:
            self.PrepareBackground()
        self._moving = True
        clicked = self._clickedShape
        if clicked and not clicked.selected:
            self._selectedShapes.append(clicked)
            clicked.selected = True
            clicked.moving   = True
        self._clickedShape = cast(Shape, None)
        for shape in self._selectedShapes:
            parent = shape.parent
            if parent is not None and parent.selected is True and not isinstance(shape, SizerShape):
                continue
            ox, oy = self._lastMousePosition
            dx, dy = x - ox, y - oy
            sx, sy = shape.GetPosition()

            self._dfLogger.debug(f'{sx=} {dx=} {sy=} {dy=}')

            shape.SetPosition(sx + dx, sy + dy)

        self.Refresh(False)
        self._lastMousePosition = (x, y)

    def OnMove(self, event: MouseEvent):
        """
        Callback for mouse movements.

        Args:
            event:

        """
        event.m_x, event.m_y = self.getEventPosition(event)
        self._dfLogger.debug(f'{event.m_x=} {event.m_y=}')

        self.OnDrag(event)

    def OnLeftDClick(self, event: MouseEvent):
        """
        Callback for left double clicks.

        Args:
            event:
        """

        self.GenericHandler(event, "OnLeftDClick")
        self._clickedShape = cast(Shape, None)
        if not self.__keepMoving:
            self.Unbind(EVT_MOTION)

    def OnMiddleDown(self, event: MouseEvent):
        """
        Callback.

        @param  event
        """
        self.GenericHandler(event, "OnMiddleDown")

    def OnMiddleUp(self, event: MouseEvent):
        """
        Callback.

        @param  event
        """
        self.GenericHandler(event, "OnMiddleUp")

    def OnMiddleDClick(self, event: MouseEvent):
        """
        Callback.

        @param  event
        """
        self.GenericHandler(event, "OnMiddleDClick")

    def OnRightDown(self, event: MouseEvent):
        """
        Callback.

        @param  event
        """
        self.GenericHandler(event, "OnRightDown")

    def OnRightUp(self, event: MouseEvent):
        """
        Callback.

        @param  event
        """
        self.GenericHandler(event, "OnRightUp")

    def OnRightDClick(self, event: MouseEvent):
        """
        Args:
            event:
        """
        crustWin = Dialog(self, -1, "PyCrust", (0, 0), (640, 480))
        crustWin.Show()
        self.GenericHandler(event, "OnRightDClick")

    def FindShape(self, x: int, y: int):
        """
        Return the shape at (x, y).

        Args:
            x: coordinate
            y: coordinate

        Returns:  The shape that was found under the coordinates or None
        """
        self._dfLogger.debug(f'Find Shape: @ ({x},{y})')
        found = None
        shapes = self._diagram.shapes
        # self.clsLogger.debug(f'{shapes=}')
        shapes.reverse()    # to select the one at the top
        for shape in shapes:
            if shape.Inside(x, y):
                self._dfLogger.debug(f"Found: {shape}")
                found = shape
                break   # only select the first one
        return found

    def DeselectAllShapes(self):
        """
        Deselect all shapes in the frame.
        """
        for shape in self._diagram.shapes:
            shape.selected = False
            shape.moving   = False
        self._selectedShapes = []

    def Refresh(self, eraseBackground: bool = True, rect: Rect = None):
        """
        not used
        Args:
            eraseBackground:    if False, the stored background is used
            rect:               not used
        """
        if eraseBackground:
            self.Redraw()
        else:
            self.RedrawWithBackground()

    def SaveBackground(self, dc: DC):
        """

        Args:
            dc: The DC to save
        """
        w, h = self.GetSize()
        bb = self.__backgroundBitmap
        if (bb.GetWidth(), bb.GetHeight()) != (w, h):
            bb = self.__backgroundBitmap = Bitmap(w, h)
        mem = MemoryDC()
        mem.SelectObject(bb)

        x, y = self.CalcUnscrolledPosition(0, 0)
        mem.Blit(0, 0, w, h, dc, x, y)

        mem.SelectObject(NullBitmap)

    def LoadBackground(self, dc: DC, w: int, h: int):
        """
        Load the background image in the given dc.

        Args:
            dc:
            w:
            h:
        """
        mem = MemoryDC()
        mem.SelectObject(self.__backgroundBitmap)
        dc.Blit(0, 0, w, h, mem, 0, 0)
        mem.SelectObject(NullBitmap)

    def ClearBackground(self):
        """
        Clear the background image.
        """
        dc = MemoryDC()
        bb = self.__backgroundBitmap
        w, h = self.GetSize()
        if (bb.GetWidth(), bb.GetHeight()) != (w, h):
            bb = self.__backgroundBitmap = EmptyBitmap(w, h)
        dc.SelectObject(bb)
        dc.SetBackground(Brush(self.GetBackgroundColour()))
        dc.Clear()
        dc.SelectObject(NullBitmap)

    def CreateDC(self, loadBackground: bool, w: int, h: int) -> DC:
        """
        Create a DC, load the background on demand.

        Args:
            loadBackground:
            w: width of the frame.
            h: height of the frame.

        Returns:  A device context
        """
        dc = MemoryDC()
        bm = self.__workingBitmap
        # cache the bitmap, to avoid creating a new one at each refresh.
        # only recreate it if the size of the window has changed
        if (bm.GetWidth(), bm.GetHeight()) != (w, h):
            bm = self.__workingBitmap = Bitmap(w, h)
        dc.SelectObject(bm)
        if loadBackground:
            self.LoadBackground(dc, w, h)
        else:
            dc.SetBackground(Brush(self.GetBackgroundColour()))
            dc.Clear()
        self.PrepareDC(dc)

        return dc

    def PrepareBackground(self):
        """
        Redraw the screen without movable shapes, store it as the background.
        """
        self.Redraw(cast(DC, None), True, True, False)

    def RedrawWithBackground(self):
        """
        Redraw the screen using the background.
        """
        self.Redraw(cast(DC, None), True, False, True)

    def Redraw(self, dc: DC = None, full: bool = True, saveBackground: bool = False, useBackground: bool = False):
        """
        Refresh the diagram.
        If a DC is given, use it. Otherwise, use a double buffered DC.

        Args:
            dc:     If None, a default dc is created
            full:   If False, only draw the shape borders.
            saveBackground: If True, save the background
            useBackground:  If True, use the background
        """
        needBlit = False
        w, h = self.GetSize()

        if dc is None:
            dc = self.CreateDC(useBackground, w, h)
            needBlit = True

        dc.SetFont(self._defaultFont)

        shapes = self._diagram.shapes
        if full:
            # first time, need to create the background
            if saveBackground:
                # first, draw every non-moving shape
                for shape in shapes:
                    # if not shape.IsMoving():
                    if shape.moving is False:
                        shape.Draw(dc)
                # save the background
                self.SaveBackground(dc)
                # draw every moving shape
                for shape in shapes:
                    # if shape.IsMoving():
                    if shape.moving is True:
                        shape.Draw(dc)

            # x, y = self.CalcUnScrolledPosition(0, 0)
            if useBackground:
                # draw every moving shape
                for shape in shapes:
                    if shape.moving is True:
                        shape.Draw(dc)
                # TODO: This code belongs in OnPaint
                # if self._prefs.backgroundGridEnabled is True:
                #     self._drawGrid(memDC=dc, width=w, height=h, startX=x, startY=y)
            else:  # don't use background
                # draw all shapes
                for shape in shapes:
                    shape.Draw(dc)
                # TODO: This code belongs in OnPaint
                # if self._prefs.backgroundGridEnabled is True:
                #     self._drawGrid(memDC=dc, width=w, height=h, startX=x, startY=y)
        else:  # not full
            for shape in shapes:
                shape.DrawBorder(dc)
                shape.DrawAnchors(dc)

        if needBlit:
            client = ClientDC(self)

            x, y = self.CalcUnscrolledPosition(0, 0)
            client.Blit(0, 0, w, h, dc, x, y)

    # noinspection PyUnusedLocal
    def OnPaint(self, event: PaintEvent):
        """
        Refresh the screen when the system issues a paint event.

        Args:
            event:
        """
        dc = PaintDC(self)
        w, h = self.GetSize()
        mem = self.CreateDC(False, w, h)
        mem.SetBackground(Brush(self.GetBackgroundColour()))
        mem.Clear()

        x, y = self.CalcUnscrolledPosition(0, 0)
        #
        # Paint events don't seem to be generated when Pyut is built for deployment;  So code duplicated in .Redraw()
        #
        if self._prefs.backGroundGridEnabled is True:
            self._drawGrid(memDC=mem, width=w, height=h, startX=x, startY=y)
        self.Redraw(mem)

        dc.Blit(0, 0, w, h, mem, x, y)

    def DoZoomIn(self, ax, ay, width=0, height=0):
        """
        Do the "zoom in" fitted on the selected area or with a default factor
        and the clicked point as central point of the zoom.
        The maximal zoom that can be reached is :

            self.GetMaxLevelZoom() * self.GetDefaultZoomFactor()

        If the maximal zoom level is reached, then the shapes are centered
        on the selected area or on the clicked point.


        Args:
            ax:     abscissa of the upper left corner of the selected
                            area or abscissa of the central point of the zoom
            ay:     ordinate of the upper left corner of the selected
                            area or ordinate of the central point of the zoom
            width:  width of the selected area for the zoom
            height: height of the selected area for the zoom
        """
        # number of pixels per unit of scrolling
        xUnit, yUnit = self.GetScrollPixelsPerUnit()

        # This is the position of the client area upper left corner.
        # (work area that is visible) in scroll units.
        viewStartX, viewStartY = self.GetViewStart()

        # Get the client and virtual work area size.
        # The client size is the size of the work area that is visible.
        # The virtual is the whole work area's size.
        clientWidth, clientHeight = self.GetClientSize()
        virtualWidth, virtualHeight = self.GetVirtualSize()

        # maximal zoom factor that can be applied
        # maxZoomFactor = self.GetMaxLevelZoom() * self.GetDefaultZoomFactor()
        maxZoomFactor = self.maxZoomFactor

        # transform event coordinates to get them relative to the upper left corner of
        # the virtual screen (avoid the case where that corner is on a shape and
        # get its coordinates relative to the client view).
        if ax >= viewStartX * xUnit and ay >= viewStartY * yUnit:
            x = ax
            y = ay
        else:
            x = ax + viewStartX * xUnit
            y = ay + viewStartY * yUnit

        # to get the upper left corner of the zoom selected area in the
        # case where we select first the bottom right corner.
        if width < 0:
            x = x - width
        if height < 0:
            y = y - height

        # init the zoom's offsets and factor
        # zoomFactor = 1
        # dx = 0
        # dy = 0

        # If there is no selected area but a clicked point, a default
        # zoom is performed with the clicked point as its center.
        if width == 0 or height == 0:
            zoomFactor = self.defaultZoomFactor
            # Check if the zoom factor that we are to apply combined with the
            # previous ones won't be beyond the maximal zoom. If it's the case,
            # we proceed to the calculation of the zoom factor that allows to
            # exactly reach the maximal zoom.
            maxZoomReached = maxZoomFactor <= (self.currentZoom * zoomFactor)
            if maxZoomReached:
                zoomFactor = maxZoomFactor / self.currentZoom
            # if the view is reduced, we eliminate the
            # last zoom out performed
            if self._zoomLevel < 0:
                self._zoomStack.pop()
                self._zoomLevel += 1
            else:
                if zoomFactor > 1.0:
                    self._zoomStack.append(zoomFactor)
                    self._zoomLevel += 1

            # Calculate the zoom area upper-left corner.
            # The size is half of the diagram frame.
            # It is centred on the clicked point.
            # This calculation is done in a way to
            # get the zoom area centred in the middle of the virtual screen.
            dx = virtualWidth/2 - x
            dy = virtualHeight/2 - y

        else:
            # to be sure to get all the shapes in the selected zoom area
            if width > height:
                zoomFactor = clientWidth / abs(width)
            else:
                zoomFactor = clientHeight / abs(height)

            # Check if the zoom factor that we are to apply combined with the
            # previous ones won't be beyond the maximal zoom. If it's the case,
            # we proceed to the calculation of the zoom factor that allows to
            # exactly reach the maximal zoom.
            maxZoomReached = maxZoomFactor <= self.currentZoom * zoomFactor
            if maxZoomReached:
                zoomFactor = maxZoomFactor / self.currentZoom

            # Calculate the zoom area upper-left corner.
            # The size is the half of the diagram frame and is centred
            # on the clicked point.
            # This calculation is done in a way to
            # get the zoom area centered in the middle of the virtual screen.
            dx = virtualWidth/2 - x - (clientWidth / zoomFactor / 2.0)
            dy = virtualHeight/2 - y - (clientHeight / zoomFactor / 2.0)

            # We have to check if the "zoom in" on a reduced view produces
            # another less reduced view or an enlarged view. For this, we
            # get the global current zoom, multiply by the zoom factor to
            # obtain only one zoom factor.
            if self._zoomLevel < 0:

                globalFactor = zoomFactor * self.currentZoom
                self._zoomStack = []
                self._zoomStack.append(globalFactor)

                if globalFactor < 1.0:
                    self._zoomLevel = -1    # the view is still reduced
                elif globalFactor > 1.0:
                    self._zoomLevel = 1     # the view is enlarged
                else:
                    self._zoomLevel = 0     # the zoom in is  equal to all the zoom out previously applied
            else:
                if zoomFactor > 1.0:
                    self._zoomStack.append(zoomFactor)
                    self._zoomLevel += 1

        # set the offsets between the model and the view
        self.xOffSet = (self.xOffSet + dx) * zoomFactor
        self.yOffSet = (self.yOffSet + dy) * zoomFactor

        # updates the shapes (view) position and dimensions from
        # their models in the light of the new zoom factor and offsets.
        for shape in self.diagram.shapes:
            shape.UpdateFromModel()

        # resize the virtual screen to match with the zoom
        virtualWidth  = round(virtualWidth * zoomFactor)
        virtualHeight = round(virtualHeight * zoomFactor)

        virtualSize:   Size = Size(virtualWidth, virtualHeight)
        self.SetVirtualSize(virtualSize)

        # perform the scrolling in the way to have the zoom area visible
        # and centred on the virtual screen.
        scrollX = (virtualWidth - clientWidth) / 2 / xUnit
        scrollY = (virtualHeight - clientHeight) / 2 / yUnit
        self.Scroll(round(scrollX), round(scrollY))

    def DoZoomOut(self, ax: int, ay: int):
        """
        Do the 'zoom out' in the way to have the clicked point (ax, ay) as
        the central point of new view.
        If one or many of 'zoom in' operations where performed before, then we suppress the
        last one from the zoom stack.
        Else, we add the default inverted zoom factor to the stack.

        Args:
            ax: abscissa of the clicked point
            ay: ordinate of the clicked point
        """
        # number of pixels per unit of scrolling
        xUnit, yUnit = self.GetScrollPixelsPerUnit()

        # Position of the client area upper-left corner.
        # (work area that is visible) in scroll units.
        viewStartX, viewStartY = self.GetViewStart()

        # Get the work area client and virtual size.
        # The client size is the size of the work area that is visible.
        # The virtual size is the whole work area's size.
        clientWidth, clientHeight = self.GetClientSize()
        virtualWidth, virtualHeight = self.GetVirtualSize()

        # Transform event coordinates to get them relative to the upper left corner of
        # the virtual screen (avoid the case where that corner is on a shape and
        # get its coordinates relative to the shape).
        if ax >= viewStartX * xUnit and ay >= viewStartY * yUnit:
            x = ax
            y = ay
        else:
            x = ax + viewStartX * xUnit
            y = ay + viewStartY * yUnit

        # Calculate the upper-left corner of a zoom area whose
        # size is the half of the diagram frame and which is centred
        # on the clicked point.
        # This calculation is done to
        # get the zoom area centred in the middle of the virtual screen.
        dx: int = virtualWidth // 2 - x
        dy: int = virtualHeight // 2 - y

        # minZoomFactor = self.GetMinZoomFactor()
        minZoomFactor: float = self.minZoomFactor
        # minZoomReached = False        not used

        # If the view is enlarged, then we remove the last
        # zoom-in factor that has been applied.
        # Else, we apply the default one in inverted.
        if self._zoomLevel > 0:
            zoomFactor = 1/self._zoomStack.pop()
            self._zoomLevel -= 1
        else:
            # zoomFactor = 1/self.GetDefaultZoomFactor()
            zoomFactor = 1 / self.defaultZoomFactor
            # check if minimal zoom has been reached
            # minZoomReached = minZoomFactor >= (self.GetCurrentZoom() * zoomFactor)
            minZoomReached = minZoomFactor >= (self.currentZoom * zoomFactor)
            if not minZoomReached:
                self._zoomStack.append(zoomFactor)
                self._zoomLevel -= 1
            else:
                zoomFactor = minZoomFactor / self.currentZoom
                if zoomFactor != 1:
                    self._zoomStack.append(zoomFactor)
                    self._zoomLevel -= 1

        # set the offsets between the view and the model for
        # each shape on this diagram frame.
        # self.SetXOffset((self.GetXOffset() + dx) * zoomFactor)
        # self.SetYOffset((self.GetYOffset() + dy) * zoomFactor)
        self.xOffSet = round((self.xOffSet + dx) * zoomFactor)
        self.yOffSet = round((self.yOffSet + dy) * zoomFactor)

        # updates the shapes (view) position and dimensions from
        # their model in the light of the new zoom factor and offsets.
        # for shape in self.GetDiagram().GetShapes():
        for shape in self.diagram.shapes:
            shape.UpdateFromModel()

        # resize the virtual screen to match with the zoom
        virtualWidth  = round(virtualWidth * zoomFactor)
        virtualHeight = round(virtualHeight * zoomFactor)

        virtualSize:   Size = Size(virtualWidth, virtualHeight)
        self.SetVirtualSize(virtualSize)

        # perform the scrolling in the way to have the zoom area visible
        # and centred on the virtual screen.
        self._dfLogger.info(f'{virtualWidth=} {clientWidth=} {xUnit=}')
        scrollX: int = (virtualWidth - clientWidth) / 2 / xUnit
        scrollY: int = (virtualHeight - clientHeight) / 2 / yUnit

        self.Scroll(round(scrollX), round(scrollY))

    def SetInfinite(self, infinite: bool = False):
        """
        Set this diagram frame as an infinite work area. The result is that the
        virtual size is enlarged when the scrollbar reaches the specified
        margins (see `SetMargins`). When we set this as `True`, the scrollbars
        are moved to the middle of their scale.

        Args:
            infinite:   If `True` the work area is infinite
        """
        self._isInfinite = infinite

        if infinite is True:
            # place all the shapes in an area centered on the infinite work area
            vWidth, vHeight = self.GetVirtualSize()
            cWidth, cHeight = self.GetClientSize()
            # get the number of pixels per scroll unit
            xUnit, yUnit = self.GetScrollPixelsPerUnit()

            # get the scroll units
            noUnitX = (vWidth-cWidth) / xUnit
            noUnitY = (vHeight-cHeight) / yUnit

            if self._prefs.centerDiagram is True:
                self.Scroll(noUnitX / 2, noUnitY / 2)   # set the scrollbars position in the middle of their scale
            else:
                self.Scroll(0, 0)

    def _BeginSelect(self, event: MouseEvent):
        """
        Create a selector box and manage it.

        @param  event
        """
        if not event.ControlDown():
            self.DeselectAllShapes()
        x, y = event.GetX(), event.GetY()   # event position has been modified

        rect: RectangleShape = RectangleShape(x, y, 0, 0)
        self._selector = rect
        rect.SetDrawFrame(True)
        rect.brush  = TRANSPARENT_BRUSH
        rect.moving = True
        self._diagram.AddShape(rect)
        self.PrepareBackground()
        self.Bind(EVT_MOTION, self._OnMoveSelector)

    def _OnMoveSelector(self, event: MouseEvent):
        """
        Callback for the selector box.

        @param  event
        """
        if self._selector is not None:
            x, y = self.getEventPosition(event)
            x0, y0 = self._selector.GetPosition()
            self._selector.SetSize(x - x0, y - y0)
            self.Refresh(False)

    def _ConvertEventCoordinates(self, event):
        xView, yView = self.GetViewStart()
        xDelta, yDelta = self.GetScrollPixelsPerUnit()
        return event.GetX() + (xView * xDelta), event.GetY() + (yView * yDelta)

    def _drawGrid(self, memDC: DC, width: int, height: int, startX: int, startY: int):

        # self.clsLogger.info(f'{width=} {height=} {startX=} {startY=}')
        savePen = memDC.GetPen()

        newPen: Pen = self._getGridPen()
        memDC.SetPen(newPen)

        self._drawHorizontalLines(memDC=memDC, width=width, height=height, startX=startX, startY=startY)
        self._drawVerticalLines(memDC=memDC,   width=width, height=height, startX=startX, startY=startY)
        memDC.SetPen(savePen)

    def _drawHorizontalLines(self, memDC: DC, width: int, height: int, startX: int, startY: int):

        x1:   int = 0
        x2:   int = startX + width
        stop: int = height + startY
        step: int = self._prefs.backgroundGridInterval
        for movingY in range(startY, stop, step):
            memDC.DrawLine(x1, movingY, x2, movingY)

    def _drawVerticalLines(self, memDC: DC, width: int, height: int, startX: int, startY: int):

        y1:   int = 0
        y2:   int = startY + height
        stop: int = width + startX
        step: int = self._prefs.backgroundGridInterval

        for movingX in range(startX, stop, step):
            memDC.DrawLine(movingX, y1, movingX, y2)

    def _getGridPen(self) -> Pen:

        gridLineColor: Colour   = MiniOglColorEnum.toWxColor(self._prefs.gridLineColor)
        gridLineStyle: PenStyle = MiniOglPenStyle.toWxPenStyle(self._prefs.gridLineStyle)

        pen:           Pen    = Pen(PenInfo(gridLineColor).Style(gridLineStyle).Width(1))

        return pen

    def _isShapeInRectangle(self, rect: RectangleShape, x0: float, y0: float, w0: float, h0: float) -> bool:

        ans: bool = False
        if rect.Inside(x0, y0) and rect.Inside(x0 + w0, y0) and rect.Inside(x0, y0 + h0) and rect.Inside(x0 + w0, y0 + h0):
            ans = True

        return ans
