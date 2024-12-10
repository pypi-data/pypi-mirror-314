
from typing import cast

from logging import Logger
from logging import getLogger

from abc import ABC
from abc import abstractmethod

from miniogl.Diagram import Diagram
from miniogl.DiagramFrame import DiagramFrame

from ogl.events.IOglEventEngine import IOglEventEngine


class EventEngineMixin(ABC):
    """
    Some of the graphic components needs to send messages when they do significant UI
    actions
    """
    def __init__(self):

        self.logger:       Logger          = getLogger(__name__)
        self._eventEngine: IOglEventEngine = cast(IOglEventEngine, None)

    @property
    def eventEngine(self) -> IOglEventEngine:
        """
        This property necessary because the diagram is not added to the OglObject until the
        object is' attached';
        TODO:  I do not like this 'legacy' behavior, it is not SOLID;  This will be fixed
        when I re-implement the Ogl layer to NOT depend on the internal miniogl layer

        Returns:  A reference to the Ogl Event Engine
        """
        if self.HasDiagramFrame() is True:

            diagramFrame: DiagramFrame = self.diagram.panel

            if diagramFrame is not None:
                if self._eventEngine is None:
                    self._eventEngine = diagramFrame.eventEngine

        return self._eventEngine

    @property
    @abstractmethod
    def diagram(self) -> Diagram:
        pass

    @abstractmethod
    def HasDiagramFrame(self):
        pass
