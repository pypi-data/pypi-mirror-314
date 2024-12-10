
from typing import Callable
from typing import TYPE_CHECKING

from logging import Logger
from logging import getLogger

from wx import Point
from wx import PostEvent
from wx import Window
from wx import PyEventBinder

from ogl.events.InvalidKeywordException import InvalidKeywordException

if TYPE_CHECKING:
    from miniogl.SelectAnchorPoint import SelectAnchorPoint
    from ogl.OglClass import OglClass

from miniogl.Shape import Shape

from ogl.events.IOglEventEngine import IOglEventEngine

from ogl.events.OglEvents import OglEventType
from ogl.events.OglEvents import CreateLollipopInterfaceEvent
from ogl.events.OglEvents import CutOglClassEvent
from ogl.events.OglEvents import DiagramFrameModifiedEvent
from ogl.events.OglEvents import RequestLollipopLocationEvent
from ogl.events.OglEvents import ShapeSelectedEvent

from ogl.events.ShapeSelectedEventData import ShapeSelectedEventData

CUT_OGL_CLASS_PARAMETER:                    str = 'shapeToCut'
REQUEST_LOLLIPOP_LOCATION_PARAMETER:        str = 'requestShape'
SELECTED_SHAPE_PARAMETER:                   str = 'selectedShape'
SELECTED_SHAPE_POSITION_PARAMETER:          str = 'selectedShapePosition'
CREATE_LOLLIPOP_IMPLEMENTOR_PARAMETER:      str = 'implementor'
CREATE_LOLLIPOP_ATTACHMENT_POINT_PARAMETER: str = 'attachmentPoint'


class OglEventEngine(IOglEventEngine):
    """
    The rationale for this class is to isolate the underlying implementation
    of events.  Currently, it depends on the wxPython event loop.  This leaves
    it open to other implementations;

    Get one of these for each Window you want to listen on
    """
    def __init__(self, listeningWindow: Window):

        self._listeningWindow: Window = listeningWindow
        self.logger: Logger = getLogger(__name__)

    def registerListener(self, event: PyEventBinder, callback: Callable):
        self._listeningWindow.Bind(event, callback)

    def sendEvent(self, eventType: OglEventType, **kwargs):
        """
        Args:
            eventType:
            **kwargs:
        """
        try:
            match eventType:
                case OglEventType.DiagramFrameModified:
                    self._sendDiagramFrameModifiedEvent()
                case OglEventType.RequestLollipopLocation:
                    self._sendRequestLollipopLocationEvent(**kwargs)
                case OglEventType.CutOglClass:
                    self._sendCutShapeEvent(**kwargs)
                case OglEventType.ShapeSelected:
                    self._sendSelectedShapeEvent(**kwargs)
                case OglEventType.CreateLollipopInterface:
                    self._sendCreateLollipopInterfaceEvent(**kwargs)
                case _:
                    self.logger.warning(f'Unknown Ogl Event Type: {eventType}')
        except KeyError as ke:
            eMsg: str = f'Invalid keyword parameter. `{ke}`'
            raise InvalidKeywordException(eMsg)

    def _sendSelectedShapeEvent(self, **kwargs):

        shape:    Shape = kwargs[SELECTED_SHAPE_PARAMETER]
        position: Point = kwargs[SELECTED_SHAPE_POSITION_PARAMETER]

        eventData:     ShapeSelectedEventData = ShapeSelectedEventData(shape=shape, position=position)
        selectedEvent: ShapeSelectedEvent     = ShapeSelectedEvent(shapeSelectedData=eventData)

        PostEvent(dest=self._listeningWindow, event=selectedEvent)

    def _sendCutShapeEvent(self, **kwargs):

        shapeToCut = kwargs[CUT_OGL_CLASS_PARAMETER]

        cutOglClassEvent: CutOglClassEvent = CutOglClassEvent(selectedShape=shapeToCut)
        PostEvent(dest=self._listeningWindow, event=cutOglClassEvent)

    def _sendDiagramFrameModifiedEvent(self):
        eventToPost: DiagramFrameModifiedEvent = DiagramFrameModifiedEvent()
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _sendRequestLollipopLocationEvent(self, **kwargs):

        requestShape: Shape                        = kwargs[REQUEST_LOLLIPOP_LOCATION_PARAMETER]
        eventToPost:  RequestLollipopLocationEvent = RequestLollipopLocationEvent(shape=requestShape)
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _sendCreateLollipopInterfaceEvent(self, **kwargs):

        implementor:     OglClass          = kwargs[CREATE_LOLLIPOP_IMPLEMENTOR_PARAMETER]
        attachmentPoint: SelectAnchorPoint = kwargs[CREATE_LOLLIPOP_ATTACHMENT_POINT_PARAMETER]

        eventToPost: CreateLollipopInterfaceEvent = CreateLollipopInterfaceEvent(implementor=implementor, attachmentPoint=attachmentPoint)
        PostEvent(dest=self._listeningWindow, event=eventToPost)
