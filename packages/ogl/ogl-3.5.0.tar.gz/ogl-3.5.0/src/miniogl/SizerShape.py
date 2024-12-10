
from miniogl.PointShape import PointShape


class SizerShape(PointShape):
    """
    A sizer, to resize other shapes.

    """
    def __init__(self, x: int, y: int, parent):
        """

        Args:
            x: x position of the sizer
            y: y position of the sizer
            parent:   Parent Shape
        """
        # PointShape.__init__(self, x, y, parent)
        super().__init__(x, y, parent)

        self.moving = True

    def Draw(self, dc, withChildren=True):
        """
        #  TODO : Remove this. This is for debugging purpose.

        Note : This functions seems to be needed to display anchors
               only on a rectangle when moving it, but not for lines,
               single anchors, ...

        Args:
            dc:
            withChildren:

        Returns:

        """
        super().Draw(dc, withChildren)

    def SetPosition(self, x: int, y: int):
        """
        Change the position of the shape, if it's draggable.
        The position of the sizer is not changed, because it is relative to the parent

        Args:
            x:  The new x position
            y:  The new y position

        """
        self.parent.Resize(self, x, y)

    def SetMoving(self, state: bool):
        """
        Set the moving flag.
        If setting a sizer moving, the parent will also be set moving.

        Args:
            state:
        """
        self.moving = True
        # a sizer is always moving
        self._parent.moving = state

    def __str__(self) -> str:
        return f'SizerShape-{self._id}'

    def __repr__(self) -> str:
        return self.__str__()
