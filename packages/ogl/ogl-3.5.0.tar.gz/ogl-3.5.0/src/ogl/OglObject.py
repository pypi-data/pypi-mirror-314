
from typing import List

from logging import Logger
from logging import getLogger

from wx import MouseEvent
from wx import Font
from wx import FONTFAMILY_SWISS
from wx import FONTSTYLE_NORMAL
from wx import FONTWEIGHT_NORMAL

from miniogl.RectangleShape import RectangleShape
from miniogl.ShapeEventHandler import ShapeEventHandler

from ogl.EventEngineMixin import EventEngineMixin
from ogl.OglLink import OglLink
from ogl.OglUtils import OglUtils

from ogl.events.OglEvents import OglEventType

from ogl.preferences.OglPreferences import OglPreferences

from pyutmodelv2.PyutObject import PyutObject


DEFAULT_FONT_SIZE = 10


class OglObject(RectangleShape, ShapeEventHandler, EventEngineMixin):
    """
    This is the base class for new OGL objects.
    Every new OGL class must inherit this class and redefine methods if
    necessary. OGL Objects are automatically a RectangleShape for
    global link management.
    """

    clsLogger: Logger = getLogger(__name__)

    def __init__(self, pyutObject=None, width: int = 0, height: int = 0):
        """

        Args:
            pyutObject: Associated PyutObject
            width:      Initial width
            height:     Initial height
        """
        self._pyutObject = pyutObject

        super().__init__(0, 0, width, height)

        EventEngineMixin.__init__(self)

        self._defaultFont: Font           = Font(DEFAULT_FONT_SIZE, FONTFAMILY_SWISS, FONTSTYLE_NORMAL, FONTWEIGHT_NORMAL)
        self._prefs:       OglPreferences = OglPreferences()

        # TODO This is also used by sequence diagrams to store OglSDMessage links
        self._oglLinks: List[OglLink] = []     # Connected links
        self._modifyCommand = None

    @property
    def pyutObject(self):
        return self._pyutObject

    @pyutObject.setter
    def pyutObject(self, pyutObject: PyutObject):
        self._pyutObject = pyutObject

    @property
    def links(self):
        return self._oglLinks

    def addLink(self, link):
        """
        Add a link to an ogl object.

        Args:
            link:  the link to add
        """
        self._oglLinks.append(link)

    def OnLeftDown(self, event: MouseEvent):
        """
        Handle event on left click.
        Note to self.  This method used to call only call event.Skip() if there was an action waiting
        Now I do it regardless;  Seem to be no ill effects

        Args:
            event:  The mouse event
        """
        OglObject.clsLogger.debug(f'OglObject.OnLeftDown  - {event.GetEventObject()=}')

        self.eventEngine.sendEvent(OglEventType.ShapeSelected, selectedShape=self, selectedShapePosition=event.GetPosition())
        event.Skip()

    def OnLeftUp(self, event: MouseEvent):
        """
        Implement this method so we can snap Ogl objects

        Args:
            event:  the mouse event
        """
        gridInterval: int = self._prefs.backgroundGridInterval
        x, y = self.GetPosition()
        if self._prefs.snapToGrid is True:
            snappedX, snappedY = OglUtils.snapCoordinatesToGrid(x=x, y=y, gridInterval=gridInterval)
            self.SetPosition(snappedX, snappedY)

    def autoResize(self):
        """
        Find the right size to see all the content and resize self.

        """
        pass

    def SetPosition(self, x: int, y: int):
        """
        Define new position for the object

        Args:
            x:  The new abscissa
            y:  The new ordinate
        """
        RectangleShape.SetPosition(self, x, y)
        self._indicateDiagramModified()

    def _indicateDiagramModified(self):
        if self.eventEngine is not None:  # we might not be associated with a diagram yet
            self.eventEngine.sendEvent(OglEventType.DiagramFrameModified)
