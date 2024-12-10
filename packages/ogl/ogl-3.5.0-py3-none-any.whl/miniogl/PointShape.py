
from typing import cast

from wx import Colour
from wx import DC
from wx import Pen

from miniogl.Shape import Shape

POINT_SHAPE_WIDTH: int = 3


class PointShape(Shape):

    SELECTION_ZONE: int = 8     # Make it bigger than in legacy;  It was 5 then
    """
    A point, which is drawn as a little square (3 pixels wide).

    """
    def __init__(self, x: int, y: int, parent=None):
        """

        Args:
            x:  x position of the point
            y:  y position of the point
            parent:  parent shape
        """
        super().__init__(x, y, parent)

        self._selectionZone:       int  = PointShape.SELECTION_ZONE
        self._visibleWhenSelected: bool = True

        self.__penSaveColor: Colour = cast(Colour, None)

    def Draw(self, dc: DC, withChildren=True):
        """
        Draw the point on the dc.

        Args:
            dc:
            withChildren:
        """
        if self._visible or (self._visibleWhenSelected and self._selected):

            self.__penSaveColor = dc.GetPen().GetColour()
            Shape.Draw(self, dc, False)

            self.__resetPenColor(dc)

            x, y = self.GetPosition()
            if not self._selected:
                dc.DrawRectangle(x - 1, y - 1, POINT_SHAPE_WIDTH, POINT_SHAPE_WIDTH)
            else:
                dc.DrawRectangle(x - POINT_SHAPE_WIDTH, y - POINT_SHAPE_WIDTH, 7, 7)
            if withChildren:
                self.DrawChildren(dc)

    @property
    def selectionZone(self) -> int:
        """
        Get the selection tolerance zone, in pixels.
        Returns: Half of the selection zone.
        """
        return self._selectionZone

    @selectionZone.setter
    def selectionZone(self, halfWidth: int):
        """
        Set the selection tolerance zone, in pixels.

        Args:
            halfWidth:  Half of the selection zone.
        """
        self._selectionZone = halfWidth

    @property
    def visibleWhenSelected(self) -> bool:
        """
        Return the "visible when selected flag".

        Returns:  True if the shape is always visible when selected
        """
        return self._visibleWhenSelected

    @visibleWhenSelected.setter
    def visibleWhenSelected(self, state: bool):
        """
        Set to True if you want the point to always be visible when it's selected.

        Args:
            state:
        """
        self._visibleWhenSelected = state

    def Inside(self, x: int, y: int):
        """

        Args:
            x: x coordinate
            y: y coordinate

        Returns:          `True` if (x, y) is inside the shape.

        """
        ax, ay = self.GetPosition()     # GetPosition always returns absolute position
        zone = self._selectionZone
        return (ax - zone < x < ax + zone) and (ay - zone < y < ay + zone)

    def __resetPenColor(self, dc: DC):

        pen: Pen = dc.GetPen()
        pen.SetColour(self.__penSaveColor)
        dc.SetPen(pen)
