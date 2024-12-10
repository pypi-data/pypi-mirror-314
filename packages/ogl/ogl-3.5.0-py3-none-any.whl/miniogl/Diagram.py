
from typing import Union

from logging import Logger
from logging import getLogger

from miniogl.Shape import Shape
from miniogl.Shape import Shapes
from miniogl.SizerShape import SizerShape


class Diagram:

    """
    A diagram contains shapes and is manages them.

    It knows every shapes that can be clicked, selected, and moved.
    """
    def __init__(self, panel):
        """

        Args:
            panel:  the panel on which to draw
        """
        self.logger: Logger = getLogger(__name__)

        self._panel = panel
        self._shapes:       Shapes = Shapes([])     # all selectable shapes
        self._parentShapes: Shapes = Shapes([])     # all first level shapes

    @property
    def shapes(self) -> Shapes:
        """
        A copy of the originals. You cannot detach or add shapes to the
        diagram this way.

        Returns: A list of the shapes in the diagram.
        """
        return Shapes(self._shapes[:])

    @property
    def parentShapes(self) -> Shapes:
        """
        Copies of the original. You cannot detach or add shapes to the
        diagram this way.

        Returns:  A list of the parent shapes in the diagram.
        """
        return self._parentShapes[:]

    @property
    def panel(self):
        """
        Returns:  The associated DiagramFrame
        """
        return self._panel

    def AddShape(self, shape, withModelUpdate: bool = True):
        """
        Add a shape to the diagram.
        This is the correct way to do it. Don't use Shape.Attach(diagram)!

        Args:
            shape:  the shape to add
            withModelUpdate:
        """
        self.logger.debug(f'AddShape {shape}')
        if shape not in self._shapes:
            self._shapes.append(shape)
        if shape not in self._parentShapes and shape.parent is None:
            self._parentShapes.append(shape)

        shape.Attach(self)

        # makes the shape's model (MVC pattern) have the right values depending on
        # the diagram frame state.
        if withModelUpdate:
            shape.UpdateModel()

    def DeleteAllShapes(self):
        """
        Delete all shapes in the diagram.
        """
        while self._shapes:
            self._shapes[0].Detach()
        self._shapes = []
        self._parentShapes = []

    def RemoveShape(self, shape: Union[Shape, SizerShape]):
        """
        Remove a shape from the diagram. Use Shape.Detach() instead!
        This also works, but it not the better way.

        TODO:  Use a Union for now;  I think the correct type is just Shape.  But,
        I need to see how Pyut uses it

        Args:
            shape:
        """
        self.logger.debug(f'Determine what got passed in: {shape=}')
        if isinstance(shape, SizerShape):
            self.logger.debug(f'Removing SizerShape')
        if shape in self._shapes:
            self._shapes.remove(shape)
        if shape in self._parentShapes:
            self._parentShapes.remove(shape)

    def MoveToFront(self, shape: Shape):
        """
        Move the given shape to the end of the display list => last drawn.

        Args:
            shape: The shape to move
        """
        shapes = [shape] + shape.GetAllChildren()
        for s in shapes:
            self._shapes.remove(s)
        self._shapes = self._shapes + shapes

    def MoveToBack(self, shape: Shape):
        """
        Move the given shape to the start of the display list => first drawn.

        Args:
            shape: The shape to move
        """
        shapes = [shape] + shape.GetAllChildren()
        for s in shapes:
            self._shapes.remove(s)
        self._shapes = shapes + self._shapes
