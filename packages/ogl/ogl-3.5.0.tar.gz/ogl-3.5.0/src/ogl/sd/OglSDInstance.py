
from typing import NewType
from typing import TYPE_CHECKING
from typing import Tuple
from typing import cast

from logging import Logger
from logging import getLogger

from wx import BLACK_PEN
from wx import DC
from wx import PENSTYLE_LONG_DASH
from wx import Pen
from wx import RED
from wx import RED_PEN
from wx import LIGHT_GREY
from wx import MouseEvent

from pyutmodelv2.PyutSDInstance import PyutSDInstance

from miniogl.Shape import Shape
from miniogl.MiniOglUtils import sign
from miniogl.AnchorPoint import AnchorPoint
from miniogl.LineShape import LineShape
from miniogl.SizerShape import SizerShape
from miniogl.ShapeEventHandler import ShapeEventHandler

from ogl.EventEngineMixin import EventEngineMixin
from ogl.events.OglEvents import OglEventType

from ogl.preferences.OglPreferences import OglPreferences

from ogl.sd.OglInstanceName import INSTANCE_NAME_HEIGHT
from ogl.sd.OglInstanceName import OglInstanceName

if TYPE_CHECKING:
    from ogl.sd.OglSDMessage import OglSDMessages

InstanceSize = NewType('InstanceSize', Tuple[int, int])


class OglSDInstance(Shape, ShapeEventHandler, EventEngineMixin):

    def __init__(self, pyutSDInstance: PyutSDInstance):

        from ogl.sd.OglSDMessage import OglSDMessages

        self._v2Logger:     Logger         = getLogger(__name__)
        self._preferences:  OglPreferences = OglPreferences()

        self._instanceYPosition: int = self._preferences.instanceYPosition

        super().__init__()
        EventEngineMixin.__init__(self)

        self._pyutSDInstance: PyutSDInstance  = pyutSDInstance
        self._messages:       OglSDMessages   = OglSDMessages([])
        self._instanceName:   OglInstanceName = self._createInstanceName(pyutSDInstance=pyutSDInstance)
        self._lifeLine:       LineShape         = self._createLifeLine()

        self._clickedOnInstanceName: bool         = False
        self._size:                  InstanceSize = InstanceSize((100, 400))

        self.visible = True

        #
        # TODO:  This will move to the mixin;  When I create it !!
        #
        self._topLeftSizer:  SizerShape = cast(SizerShape, None)
        self._topRightSizer: SizerShape = cast(SizerShape, None)
        self._botLeftSizer:  SizerShape = cast(SizerShape, None)
        self._botRightSizer: SizerShape = cast(SizerShape, None)

    @property
    def selected(self) -> bool:
        """
        Override Shape

        Returns: 'True' if selected 'False' otherwise
        """
        return self._selected

    @selected.setter
    def selected(self, state: bool):
        self._selected              = state
        self._instanceName.selected = state
        self._lifeLine.selected     = state
        self.ShowSizers(state)

    @property
    def pyutSDInstance(self):
        return self._pyutSDInstance

    @pyutSDInstance.setter
    def pyutSDInstance(self, pyutSDInstance: PyutSDInstance):
        self._pyutSDInstance = pyutSDInstance
        self._instanceName.instanceName = pyutSDInstance.instanceName

    @property
    def lifeline(self) -> LineShape:
        """
        Parent of an OGLSDMessage instance

        Returns: The lifeline object
        """
        return self._lifeLine

    @property
    def messages(self) -> 'OglSDMessages':
        return self._messages

    def Draw(self, dc: DC, withChildren: bool = True):
        """
        Draw the shape.

        Args:
            dc:             The device context
            withChildren:

        """
        super().Draw(dc=dc, withChildren=False)
        self.DrawChildren(dc)
        if self._selected is True:
            dc.SetPen(RED_PEN)
            self.DrawHandles(dc)

        if self._topLeftSizer is not None:
            self._topLeftSizer.Draw(dc, False)

        self.DrawBorder(dc)

    def DrawBorder(self, dc):
        """
        Draw the border of the shape, for fast rendering.
        """
        super().DrawBorder(dc)
        savePen: Pen = dc.GetPen()

        if self._selected is True:
            drawPen: Pen = Pen(RED, style=PENSTYLE_LONG_DASH)
        else:
            drawPen = Pen(LIGHT_GREY, style=PENSTYLE_LONG_DASH)

        dc.SetPen(drawPen)

        sx, sy = self.GetPosition()
        sx = sx - self._ox
        sy = sy - self._oy
        width, height = self.GetSize()
        dc.DrawRectangle(sx, sy, width, height)

        dc.SetPen(savePen)

    def Inside(self, x, y) -> bool:
        if self._instanceName.Inside(x=x, y=y) is True:
            self._clickedOnInstanceName = True
            return True
        elif self._inside(x=x, y=y) is True:
            return True

        return False

    def SetSize(self, width: int, height: int):
        """

        Args:
            width:  The new width
            height: The new height
        """
        self._size = InstanceSize((width, height))
        self._instanceName.SetSize(width=width, height=INSTANCE_NAME_HEIGHT)

        # Set lifeline
        (myX, myY) = self.GetPosition()
        (w, h) = self.GetSize()

        self._v2Logger.debug(f'{self._size=} myX,myY: ({myX},{myY}) w,h: ({w},{h})')

        lineSrc: AnchorPoint = self._lifeLine.sourceAnchor
        lineDst: AnchorPoint = self._lifeLine.destinationAnchor

        lineSrc.draggable = True
        lineDst.draggable = True
        lineSrc.SetPosition(w // 2 + myX, 0 + myY + INSTANCE_NAME_HEIGHT)
        self._v2Logger.debug(f'{lineSrc.GetPosition()=}')
        lineDst.SetPosition(w // 2 + myX, height + myY)
        lineSrc.draggable = False
        lineDst.draggable = False

        # for anchor in self._anchors:
        #     ax, ay = anchor.GetPosition()
        #     # Reset position to stick the border
        #     anchor.SetPosition(ax, ay)

    def GetSize(self) -> InstanceSize:
        return self._size

    def SetPosition(self, x: int, y: int):
        """
        Force y position
        """
        y = self._instanceYPosition
        super().SetPosition(x, y)

    def ShowSizers(self, state: bool = True):
        """
        Show the four sizer shapes if state is True.

        TODO:  This is duplicated from RectangleShape.  Create a mixin to use for
        both.

        Args:
            state:

        """
        width, height = self.GetSize()
        if state and not self._topLeftSizer:
            self._topLeftSizer  = SizerShape(-self._ox, -self._oy, self)
            self._topRightSizer = SizerShape(-self._ox + width - 1, self._oy, self)
            self._botLeftSizer  = SizerShape(-self._ox, -self._oy + height - 1, self)
            self._botRightSizer = SizerShape(-self._ox + width - 1, -self._oy + height - 1, self)

            self._diagram.AddShape(self._topLeftSizer)
            self._diagram.AddShape(self._topRightSizer)
            self._diagram.AddShape(self._botLeftSizer)
            self._diagram.AddShape(self._botRightSizer)
        elif not state and self._topLeftSizer is not None:
            self._topLeftSizer.Detach()
            self._topRightSizer.Detach()
            self._botLeftSizer.Detach()
            self._botRightSizer.Detach()

            self._topLeftSizer  = cast(SizerShape, None)
            self._topRightSizer = cast(SizerShape, None)
            self._botLeftSizer  = cast(SizerShape, None)
            self._botRightSizer = cast(SizerShape, None)

    def addMessage(self, message):
        """
        Add a message

        Args:
            message:  the message to add
        """
        self._messages.append(message)

    def Resize(self, sizer, x, y):
        """
        Resize the rectangle according to the new position of the sizer.
        Not used to programmatically resize a shape. Use `SetSize` for this.

        TODO:  Copied from RectangleShape;  Needs to be part of a mixin
        Args:
            sizer:
            x:      x position of the sizer
            y:      y position of the sizer

        """
        # self._v2Logger.debug(f'Resize - {sizer=}')

        tlx, tly = self.topLeft
        w, h = self.GetSize()
        sw, sh = sign(w), sign(h)
        w, h = abs(w), abs(h)
        if sizer is self._topLeftSizer:
            nw = sw * (w - x + tlx)
            nh = sh * (h - y + tly)
            self._ox = self._ox * nw // w
            self._oy = self._oy * nh // h
            self.SetSize(nw, nh)
            self.SetTopLeft(x, y)
            self._topRightSizer.SetRelativePosition(nw - 1, 0)
            self._botLeftSizer.SetRelativePosition(0, nh - 1)
            self._botRightSizer.SetRelativePosition(nw - 1, nh - 1)
        elif sizer is self._topRightSizer:
            nw = sw * (x - tlx)
            nh = sh * (tly + h - y)
            self.SetTopLeft(tlx, y)
            self.SetSize(nw + 1, nh)
            self._topRightSizer.SetRelativePosition(nw, 0)
            self._botRightSizer.SetRelativePosition(nw, nh - 1)
            self._botLeftSizer.SetRelativePosition(0, nh - 1)
        elif sizer is self._botLeftSizer:
            nw = sw * (w - x + tlx)
            nh = sh * (y - tly)
            self.SetTopLeft(x, tly)
            self.SetSize(nw, nh + 1)
            self._botLeftSizer.SetRelativePosition(0, nh)
            self._botRightSizer.SetRelativePosition(nw - 1, nh)
            self._topRightSizer.SetRelativePosition(nw - 1, 0)
        elif sizer is self._botRightSizer:
            nw = sw * (x - tlx)
            nh = sh * (y - tly)
            self.SetSize(nw + 1, nh + 1)
            self._botLeftSizer.SetRelativePosition(0, nh)
            self._botRightSizer.SetRelativePosition(nw, nh)
            self._topRightSizer.SetRelativePosition(nw, 0)

    def SetTopLeft(self, x, y):
        """
        TODO: should be part of Resize mixin
        Args:
            x:
            y: new position

        Returns:

        """
        x += self._ox
        y += self._oy
        width, height = self.GetSize()
        if width < 0:
            x -= width
        if height < 0:
            y -= height
        self._x, self._y = x, y

    def OnLeftUp(self, event):
        """
        Callback for left clicks.
        """
        self.SetPosition(self.GetPosition()[0], self._instanceYPosition)

    def OnLeftDown(self, event: MouseEvent):
        """
        Handle event on left click.
        Note to self.  This method used to call only call event.Skip() if there was an action waiting
        Now I do it regardless;  Seem to be no ill effects

        Args:
            event:  The mouse event
        """
        self._v2Logger.debug(f'OglSDInstanceV2.OnLeftDown  - {event.GetEventObject()=}')

        self.eventEngine.sendEvent(OglEventType.ShapeSelected, selectedShape=self, selectedShapePosition=event.GetPosition())
        event.Skip()

    def _createInstanceName(self, pyutSDInstance: PyutSDInstance) -> OglInstanceName:
        """

        Returns:  An OglInstanceName
        """
        oglInstanceName: OglInstanceName = OglInstanceName(instanceName=pyutSDInstance.instanceName, x=0, y=0, parent=self)
        oglInstanceName.SetRelativePosition(0, 0)

        self.AppendChild(oglInstanceName)

        return oglInstanceName

    def _createLifeLine(self) -> LineShape:
        """
        Returns:  The lifeline
        """
        width:  int = self._preferences.instanceDimensions.width
        height: int = self._preferences.instanceDimensions.height
        # (srcX, srcY, dstX, dstY) = (width // 2, 0,
        #                             width // 2, height
        #                             )
        srcX: int = width // 2
        srcY: int = 0
        dstX: int = width // 2
        dstY: int = height

        srcY = srcY + self._instanceName.GetHeight()        # position at bottom
        # (src, dst) = (AnchorPoint(srcX, srcY, self), AnchorPoint(dstX, dstY, self))
        src: AnchorPoint = AnchorPoint(x=srcX, y=srcY, parent=self)
        dst: AnchorPoint = AnchorPoint(x=dstX, y=dstY, parent=self)

        for anchorPoint in [src, dst]:
            anchorPoint.visible   = True
            anchorPoint.draggable = False

        src.SetStayOnBorder(state=False)
        lifeLineShape: LineShape = LineShape(src, dst)

        lifeLineShape.parent    = self._instanceName
        lifeLineShape.drawArrow = False
        lifeLineShape.draggable = True
        lifeLineShape.pen       = BLACK_PEN
        lifeLineShape.visible   = True

        self.AppendChild(lifeLineShape)

        return lifeLineShape

    def _inside(self, x, y) -> bool:
        """
        True if (x, y) is inside the rectangle.

        TODO:  This is duplicated from RectangleShape;  Create a mixin to use for both

        Args:
            x:
            y:

        Returns:

        """
        # this also works if width and/or height is negative.
        sx, sy = self.GetPosition()
        # take a minimum of 4 pixels for the selection
        width, height = self.GetSize()
        width  = sign(width)  * max(abs(width),  4)
        height = sign(height) * max(abs(height), 4)
        topLeftX: int = sx - self._ox
        topLeftY: int = sy - self._oy

        topXLeftIsInside:  bool  = x >= topLeftX
        topXRightIsInside: bool  = x <= topLeftX + width
        topYLeftIsInside:  bool  = y >= topLeftY
        topYRightIsInside: bool  = y <= topLeftY + height
        if topXLeftIsInside and topXRightIsInside and topYLeftIsInside and topYRightIsInside:
            return True
        else:
            return False

    def __str__(self) -> str:
        x, y = self.GetPosition()
        return f'OglSDInstanceV2[{self.id=} position: ({x},{y}])'

    def __repr__(self):
        return self.__str__()
