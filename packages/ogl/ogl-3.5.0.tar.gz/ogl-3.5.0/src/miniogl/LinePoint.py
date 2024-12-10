from typing import List
from typing import NewType
from typing import cast

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from miniogl.LineShape import LineShapes

from miniogl.PointShape import PointShape


class LinePoint(PointShape):
    """
    This is a point guiding a line.
    """
    def __init__(self, x: int, y: int, parent=None):
        """

        Args:
            x:  abscissa of point
            y:  ordinate of point
            parent:     parent shape
        """
        from miniogl.LineShape import LineShapes

        super().__init__(x, y, parent)
        self._lines: LineShapes = LineShapes([])    # LineShape(s) passing through this point

    def AddLine(self, line):
        """
        Add a line to this point.

        @param  line
        """
        self._lines.append(line)

    def Detach(self):
        """
        Detach the point from the diagram
        This also removes the point from all the lines it belongs to.
        """
        PointShape.Detach(self)
        for line in self._lines:
            line.Remove(self)
        self._lines = []

    @property
    def lines(self) -> 'LineShapes':
        """
        Return the lines passing through this point.
        Modifying the returned list won't modify the point itself.

        Returns:  A copy
        """
        return self._lines[:]

    def RemoveLine(self, line):
        """
        Remove a line from this point.

        @param line
        """
        if line in self._lines:
            self._lines.remove(line)

    @property
    def moving(self) -> bool:
        return super().moving

    @moving.setter
    def moving(self, state: moving):
        """
        A non-moving shape will be redrawn faster when others are moved.
        See DiagramFrame.Refresh for more information.

        Args:
            state:
        """
        from miniogl.LineShape import LineShape

        self._moving = state
        for ll in self._lines:
            line: LineShape = cast(LineShape, ll)
            line.moving = state


ControlPoints = NewType('ControlPoints', List[LinePoint])
