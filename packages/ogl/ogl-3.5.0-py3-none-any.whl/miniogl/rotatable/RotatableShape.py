
from miniogl.RectangleShape import RectangleShape

from miniogl.rotatable.VShapes import VShape


class RotatableShape(RectangleShape):
    """
    Canvas for shapes that can be rotated.
    The shape is defined for one orientation, using a list of VShapes which
    is a class field named SHAPES. Then, the method Rotate can be called to
    automatically rotate the shape.

    @author Laurent Burgbacher <lb@alawa.ch>
    """
    def __init__(self, x=0, y=0, width=0, height=0, parent=None):
        """

        Args:
            x:  position of the point
            y:  position of the point
            width: size of the rectangle
            height: height of the rectangle
            parent: parent shape
        """
        super().__init__(x=x, y=y, width=width, height=height, parent=parent)

        self._drawFrame = False

        # this is the definition of the shape
        self._defineShape()
        self._angle: int = 0                            # angle is in [0..3], by steps of 90 degrees
        self._vShapes = self._SHAPES[0]                 # currently, used list of shapes
        self._InitRotations()                           # create the other rotations if necessary

        self._scale: int = 1                            # scale of the shape
        self._sox, self._soy = self._ox, self._oy       # ox, oy with scale == 1
        self._sw, self._sh = self._width, self._height  # width and height with scale == 1

    def _defineShape(self):
        """
        This is the definition of the graphical object.
        It uses a list of basic shapes, that support rotation and scaling.
        Define your own shapes in children classes by filling the innermost
        list with `VShape` instances.
        """
        self._SHAPES = [
            [
            ]
        ]

    def GetAngle(self):
        """
        Get the actual angle, in range [0; 3].

        @return int angle
        """
        return self._angle

    def SetAngle(self, angle):
        """
        Set the actual angle, in range [0; 3].
        0 is the initial angle. Each unit is a clockwise 90-degree rotation.

        @param  angle
        """
        while self._angle != angle:
            self.Rotate(True)

    def SetScale(self, scale: float):
        """
        Set the scaling of this shape.

        @param  scale
        """
        self._scale = scale
        self._ox, self._oy = self._sox * scale, self._soy * scale
        self._width, self._height = self._sw * scale, self._sh * scale

    def GetScale(self):
        """
        Get the scaling of this shape.

        @return float
        """
        return self._scale

    def SetOrigin(self, x: int, y: int):
        """
        Set the origin of the shape, from its upper left corner.
        Args:
            x: new origin abscissa
            y: new origin ordinate
        """
        self._ox = x
        self._oy = y
        scale = self._scale
        if scale != 0:
            self._sox, self._soy = x / scale, y / scale
        else:
            self._sox, self._soy = 0, 0

    def _InitRotations(self):
        """
        Init the rotations.
        Will be done just one time, or when the initial shape is changed.
        """
        if len(self._SHAPES) == 1:
            from copy import copy
            for i in range(1, 4):
                nextRotates = []
                for shape in self._SHAPES[0]:
                    n = copy(shape)
                    n.SetAngle(i)
                    nextRotates.append(n)
                self._SHAPES.append(nextRotates)

    def Rotate(self, clockwise: bool):
        """
        Rotate the shape 90 degrees clockwise or counterclockwise.

        @param  clockwise
        """
        if clockwise:
            self._angle += 1
        else:
            self._angle -= 1
        self._angle %= 4
        self._vShapes = self._SHAPES[self._angle]
        for child in self._anchors + self._children:
            lock = False
            x, y = child.GetRelativePosition()
            if not child.IsDraggable():
                child.SetDraggable(True)
                lock = True
            x, y = VShape.convert(1, x, y)
            child.SetRelativePosition(x, y)
            if lock:
                child.SetDraggable(False)
        self._width, self._height = VShape.convert(1, self._width, self._height)
        self._ox, self._oy = VShape.convert(1, self._ox, self._oy)

    def Draw(self, dc, withChildren=True):
        """
        Draw the shape on the dc.

        @param  dc
        @param withChildren
        """
        if self._visible:
            super().Draw(dc, False)
            for shape in self._vShapes:
                shape.Draw(dc, self._x, self._y, self._scale)
            if withChildren:
                self.DrawChildren(dc)
