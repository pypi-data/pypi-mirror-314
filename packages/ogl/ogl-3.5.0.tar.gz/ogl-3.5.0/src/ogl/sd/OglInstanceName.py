
from logging import Logger
from logging import getLogger

from wx import BLACK
from wx import DC
from wx import FONTFAMILY_TELETYPE
from wx import FONTSTYLE_ITALIC
from wx import FONTWEIGHT_NORMAL

from wx import Font
from wx import MouseEvent

from wx import PENSTYLE_SOLID
from wx import Pen

from miniogl.ShapeEventHandler import ShapeEventHandler
from miniogl.TextShape import TextShape

from ogl.EventEngineMixin import EventEngineMixin
from ogl.events.OglEvents import OglEventType

INSTANCE_NAME_WIDTH:  int = 100     # This should be in settings when we allow instance name font size to be configurable
INSTANCE_NAME_HEIGHT: int = 50      # This should be in settings when we allow instance name font size to be configurable


class OglInstanceName(TextShape, ShapeEventHandler, EventEngineMixin):

    TEXT_SHAPE_FONT_SIZE: int = 12
    """
    """
    def __init__(self, instanceName: str, x: int, y: int,  parent=None):
        """

        Args:
            instanceName:
            x:
            y:
            parent:
        """
        self.logger:        Logger = getLogger(__name__)
        self._defaultFont:  Font   = Font(OglInstanceName.TEXT_SHAPE_FONT_SIZE, FONTFAMILY_TELETYPE, FONTSTYLE_ITALIC, FONTWEIGHT_NORMAL)

        super().__init__(x, y, instanceName, parent=parent, font=self._defaultFont)
        EventEngineMixin.__init__(self)

        self.drawFrame = True
        self.resizable = True
        self.draggable = False

        #
        # These should be preferences
        #
        self.SetSize(width=INSTANCE_NAME_WIDTH, height=INSTANCE_NAME_HEIGHT)

    @property
    def instanceName(self) -> str:
        return self.text

    @instanceName.setter
    def instanceName(self, newName: str):
        self.text = newName

    @property
    def selected(self) -> bool:
        """
        Override TextShape

        Returns: 'True' if selected 'False' otherwise
        """
        return self._selected

    @selected.setter
    def selected(self, state: bool):
        """
        Force OglSDInstanceV2 to treat us as a unit

        Args:
            state:

        """
        self._selected = state

    def Draw(self, dc: DC, withChildren: bool = True):
        """
        Draw the text on the dc.

        Args:
            dc
            withChildren
        """
        if self._visible:
            if self._selected:
                dc.SetPen(self._selectedPen)
                dc.SetTextForeground(self._redColor)
                self.DrawBorder(dc=dc)
            else:
                dc.SetTextForeground(self._textColor)
                pen: Pen = Pen(colour=BLACK, width=1, style=PENSTYLE_SOLID)

                dc.SetPen(pen)
                self.DrawBorder(dc=dc)

            self._drawText(dc)

            if withChildren:
                self.DrawChildren(dc)

    def DrawBorder(self, dc):
        """
        Draw the border of the shape, for fast rendering.
        """

        sx, sy = self.GetPosition()
        sx, sy = sx - self._ox, sy - self._oy
        width, height = self.GetSize()
        dc.DrawRectangle(sx, sy, width, height)

    def OnLeftDown(self, event: MouseEvent):
        """
        Handle event on left click.
        Note to self.  This method used to call only call event.Skip() if there was an action waiting
        Now I do it regardless;  Seem to be no ill effects

        Args:
            event:  The mouse event
        """
        self.logger.debug(f'OglInstanceNameV2.OnLeftDown  - {event.GetEventObject()=}')

        self.eventEngine.sendEvent(OglEventType.ShapeSelected, selectedShape=self, selectedShapePosition=event.GetPosition())
        event.Skip()
