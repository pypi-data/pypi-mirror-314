from logging import Logger
from logging import getLogger

from wx import DC

from miniogl.TextShape import TextShape

from wx import Font

from ogl.EventEngineMixin import EventEngineMixin
from ogl.events.OglEvents import OglEventType


class OglAssociationLabel(TextShape, EventEngineMixin):

    def __init__(self, x: int, y: int, text: str, parent=None, font: Font = None):

        super().__init__(x=x, y=y, text=text, parent=parent, font=font)

        EventEngineMixin.__init__(self)

        self.labelLogger: Logger = getLogger(__name__)

    def Draw(self, dc: DC, withChildren: bool = True):

        super().Draw(dc=dc, withChildren=withChildren)

        if self.moving is True:
            pos = self.GetPosition()
            rPos = self.GetRelativePosition()
            self.labelLogger.debug(f'{pos=} {rPos=}')

    def SetPosition(self, x: int, y: int):
        super().SetPosition(x=x, y=y)
        if self.eventEngine is not None:        # we might not be associated with a diagram yet
            self.eventEngine.sendEvent(OglEventType.DiagramFrameModified)
