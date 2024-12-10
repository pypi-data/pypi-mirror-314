
from typing import ClassVar
from typing import Generator
from typing import List
from typing import NewType
from typing import cast
from typing import Tuple

from logging import Logger
from logging import getLogger

from wx import BLACK_PEN
from wx import Brush
from wx import DC
from wx import Font
from wx import Pen
from wx import RED
from wx import RED_PEN
from wx import WHITE_BRUSH

from miniogl.models.ShapeModel import ShapeModel

from ogl.preferences.OglPreferences import OglPreferences


def infiniteSequence() -> Generator[int, None, None]:
    num = 0
    while True:
        yield num
        num += 1


class Shape:
    """
    Shape is the basic graphical block. It is also the view in
    an MVC pattern, so it has a relative model (ShapeModel).
    """

    idGenerator: ClassVar = infiniteSequence()

    def __init__(self, x: int = 0, y: int = 0, parent=None):
        """
        If a parent is given, the position is relative to the parent's origin.

        Args:
            x: position of the shape on the diagram
            y: position of the shape on the diagram
            parent:
        """
        self._shapeLogger: Logger = getLogger(__name__)

        self._x: int = x    # shape position (view)
        self._y: int = y    # shape position (view)
        self._ox: int = 0   # origin position (view)
        self._oy: int = 0   # origin position (view)

        self._parent:    Shape = parent     # parent shape
        self._selected:  bool  = False      # is the shape selected ?
        self._visible:   bool  = True       # is the shape visible ?
        self._draggable: bool  = True       # can the shape be dragged ?
        self._moving:    bool  = False      # is this shape moving now ?
        self._protected: bool  = False      # to protect against deletion

        self._anchors:         List = []   # anchors of the shape
        self._children:        List = []   # child shapes
        self._privateChildren: List = []   # private children, not saved

        self._pen:   Pen   = BLACK_PEN    # pen to use
        self._brush: Brush = WHITE_BRUSH  # brush to use

        self._model: ShapeModel = ShapeModel(self)  # model of the shape (MVC pattern)

        from miniogl.Diagram import Diagram

        self._diagram: Diagram = cast(Diagram, None)       # associated diagram

        self._id = next(Shape.idGenerator)     # unique ID number

        if OglPreferences().debugBasicShape is True:
            from miniogl.TextShape import TextShape
            from miniogl.LineShape import LineShape
            if isinstance(self, (TextShape, LineShape)) is False:
                t: TextShape = self.AddText(0, -10, str(self._id))
                t.color = RED

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, newValue: int):
        self._id = newValue

    @property
    def draggable(self) -> bool:
        """
        Returns:  `True` if shape is draggable else `False`
        """
        return self._draggable

    @draggable.setter
    def draggable(self, draggable: bool):
        """

        Args:
            draggable:  If `False`, the shape will not be movable.
        """
        self._draggable = draggable

    @property
    def selected(self) -> bool:
        """
        `True` if the shape is selected else `False`
        """
        return self._selected

    @selected.setter
    def selected(self, state: bool):
        """

        Args:
            state: `True` if it is selected else `False`
        """
        self._selected = state

    @property
    def model(self):
        """
        Returns:  The shape model (MVC pattern)
        """
        return self._model

    @model.setter
    def model(self, value: ShapeModel):
        """
        Associate a new model with this shape (MVC pattern)

        Args:
            value: New model

        """
        self._model = value

    @property
    def moving(self) -> bool:
        """

        Returns: `True` if the shape is moving else `False`
        """
        return self._moving

    @moving.setter
    def moving(self, state: bool):
        """
        A non-moving shape will be redrawn faster when others are moved.
        See DiagramFrame.Refresh for more information.

        Args:
            state:
        """
        self._moving = state
        for shape in self._children:
            shape.moving = state
        for anchor in self._anchors:
            anchor.moving = state

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value: bool):
        self._visible = value

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent: 'Shape'):
        self._parent = parent

    @property
    def protected(self) -> bool:
        """
        Determines if the shape is protected against deletion (Detach).

        Returns:
        """
        return self._protected

    @protected.setter
    def protected(self, newValue: bool):
        self._protected = newValue

    @property
    def brush(self) -> Brush:
        """

        Returns: The brush used to draw the shape.
        """
        return self._brush

    @brush.setter
    def brush(self, newBrush: Brush):
        """

        Args:
            newBrush: The brush used to draw the shape.
        """
        self._brush = newBrush

    @property
    def pen(self):
        """
        Returns:  The pen used to draw the shape.
        """
        return self._pen

    @pen.setter
    def pen(self, pen: Pen):
        """
        Args:
            pen: The pen used to draw the shape.
        """
        self._pen = pen

    @property
    def anchors(self):
        """

        Returns: The list of shape anchors
        """
        return self._anchors[:]     # Funky Python notation that creates a copy

    @property
    def topLeft(self) -> Tuple[int, int]:
        """
        The coordinates of the top left point in diagram coordinates.

        Returns:  The top left shape position as a tuple
        """

        x, y = self.GetPosition()
        x -= self._ox
        y -= self._oy
        return x, y

    @property
    def children(self) -> List:
        """
        Does not return the list recursively, only get first level children.
        It's a copy of the original list, modifying it won't modify the
        original.

        Returns: The shape children
        """
        return self._children[:]

    @property
    def diagram(self):
        """

        Returns: the diagram associated with this shape.
        """
        return self._diagram

    def SetOrigin(self, x: int, y: int):
        """
        Set the origin of the shape, from its upper left corner.

        Args:
            x:  new origin
            y:  new origin

        """
        self._ox, self._oy = x, y

    def GetOrigin(self):
        """
        Get the origin of the shape, from its upper left corner.

        @return double x, y : origin
        """
        return self._ox, self._oy

    def AppendChild(self, child: 'Shape'):
        """
        Append a child to this shape.
        This doesn't add it to the diagram, but it will be drawn by the parent.

        Args:
            child:
        """
        child.parent = self
        self._children.append(child)

    def GetAllChildren(self):
        """
        Get all the children of this shape, recursively.

        @return Shape []
        """
        shapes = []
        for child in self._children:
            shapes.append(child.GetAllChildren())
        return shapes

    def AddAnchor(self, x: int, y: int, anchorType=None):
        """
        Add an anchor point to the shape.
        A line can be linked to it. The anchor point will stay bound to the
        shape and move with it. It is protected against deletion (by default)
        and not movable by itself.

        Args:
            x: position of the new point, relative to the origin of the shape
            y: position of the new point, relative to the origin of the shape
            anchorType:  class to use as anchor point, or None for default (AnchorPoint)

        Returns:    the created anchor
        """
        from miniogl.AnchorPoint import AnchorPoint     # I don't like in module imports but there is a cyclical dependency somewhere

        if anchorType is None:
            anchorType = AnchorPoint
        p = anchorType(x, y, self)
        p.protected = True
        self._anchors.append(p)
        if self._diagram is not None:
            self._diagram.AddShape(p)
        # if the shape is not yet attached to a diagram, the anchor points
        # will be attached when Attach is called on the shape.
        return p

    def AddAnchorPoint(self, anchor):
        """
        Add an anchor point directly.

        Args:
            anchor:
        """
        self._anchors.append(anchor)

    def RemoveAllAnchors(self):
        """
        Remove all anchors of the shape.
        """
        while self._anchors:
            self.RemoveAnchor(self._anchors[0])

    def RemoveAnchor(self, anchor):
        """
        Remove an anchor.

        Args:
            anchor:   The anchor to remove
        """
        if anchor in self._anchors:
            self._anchors.remove(anchor)

    def AddText(self, x: int, y: int, text: str, font: Font = None):
        """
        Add a text shape to the shape.
        Args:
            x : position of the text, relative to the origin of the shape
            y : position of the text, relative to the origin of the shape
            text : text to add
            font: font to use

        Returns:
            The created shape
        """
        # Shape.clsLogger.debug(f'AddText - {text=} @ ({x}, {y})')
        t = self._createTextShape(x, y, text, font=font)
        self._children.append(t)

        return t

    def Attach(self, diagram):
        """
        Don't use this method, use Diagram.AddShape instead !!!
        Attach the shape to a diagram.
        When you create a new shape, you must attach it to a diagram before
        you can see it. This method is used internally by Diagram.AddShape.

        Args:
            diagram:
        """
        self._diagram = diagram
        # add the anchors and the children
        # map(lambda x: diagram.AddShape(x), self._anchors + self._children + self._privateChildren)

        def hasDiagram(kid) -> bool:
            if kid.diagram is not None:
                return True
            else:
                return False

        children: List[Shape] = self._anchors + self._children + self._privateChildren
        for child in children:
            diagram.AddShape(child)
            self._shapeLogger.debug(f'Attach: {child} has diagram {hasDiagram(child)}')

    def Detach(self):
        """
        Detach the shape from its diagram.
        This is the way to delete a shape. All anchor points are also
        removed, and link lines too.
        """
        # do not detach a protected shape
        from miniogl.Diagram import Diagram

        if self._diagram is not None and not self._protected:
            # noinspection PyProtectedMember
            self.model._views.remove(self)

            diagram = self._diagram
            self._diagram = cast(Diagram, None)
            diagram.RemoveShape(self)
            # detach the anchors + children
            while self._anchors:
                child = self._anchors[0]
                child.protected = False
                child.Detach()
                child.protected = True
            for child in self._children + self._privateChildren:
                child.protected = False
                child.Detach()
                child.protected = True

            # Shape.clsLogger.debug("now, the shapes are", diagram.GetShapes())

    def Draw(self, dc: DC, withChildren: bool = True):
        """
        Draw the shape.
        For a shape, only the anchors are drawn. Nothing is drawn if the
        shape is set invisible.
        For children classes, the main classes would normally call its
        parent's Draw method, passing withChildren = False, and finally
        calling itself the DrawChildren method.

        Args:
            dc:             wxPython device context
            withChildren:   draw the children or not
        """

        if self._visible:
            dc.SetPen(self._pen)
            dc.SetBrush(self._brush)
            if withChildren is True:
                self.DrawChildren(dc)

        if self._selected is True:
            dc.SetPen(RED_PEN)
            self.DrawHandles(dc)

    def DrawChildren(self, dc: DC):
        """
        Draw the children of this shape.

        Args:
            dc:
        """
        if self._visible:
            for child in self._children + self._anchors + self._privateChildren:
                child.Draw(dc)

    def DrawBorder(self, dc: DC):
        """
        Draw the shape border
        Args:
            dc:
        """
        pass

    def DrawAnchors(self, dc: DC):
        """
        Draw the shape anchors
        Args:
            dc:
        """
        map(lambda x: x.Draw(dc), self._anchors)

    def DrawHandles(self, dc: DC):
        """
        Draw the shape handles (selection points)
        Args:
            dc:
        """
        pass

    def GetPosition(self) -> Tuple[int, int]:
        """
        Return the absolute position of the shape.
        It is in the diagram's coordinate system.

        Returns: An x,y tuple

        """
        if self._parent is not None:
            x, y = self._parent.GetPosition()
            return self._x + x, self._y + y
        else:
            return self._x, self._y

    def GetSize(self) -> Tuple[int, int]:
        """
        Get the size of the shape.

        Returns:  a width, height tuple

        """
        return 0, 0

    def ConvertCoordToRelative(self, x, y):
        """
        Convert absolute coordinates to relative ones.
        Relative coordinates are coordinates relative to the origin of the
        shape.

        @return (double, double)
        """
        if self._parent is not None:
            ox, oy = self._parent.GetPosition()
            x -= ox
            y -= oy
        return x, y

    def GetRelativePosition(self):
        """
        Return the position of the shape, relative to its parent.

        @return (double, double)
        """
        return self._x, self._y

    def Inside(self, x, y) -> bool:
        """

        Args:
            x: x coordinate
            y: y coordinate

        Returns:          `True` if (x, y) is inside the shape.
        """
        return False

    def SetPosition(self, x: int, y: int):
        """
        If it's draggable; change the position of the shape;  Upper left corner

        Args:
            x:  x position to move shape to
            y:  y position to move shape to
        """
        if self._draggable:
            if self._parent is None:
                self._x = x
                self._y = y
                # Shape.clsLogger.debug(f'{self._id=} Position: ({self._x},{self._y})')
            else:
                # Shape.clsLogger.debug(f'_parent: {self._parent}')
                self._x, self._y = self.ConvertCoordToRelative(x, y)
            #  if the shape is attached to a diagramFrame, it means that
            #  the model will be initialized correctly.
            # (Avoid a null pointer error).
            if self.HasDiagramFrame():
                self.UpdateModel()

    def SetRelativePosition(self, x: int, y: int):
        """
        Set the position of the shape, relative to the parent.
        Only works if the shape is draggable.

        Args:
            x:
            y:
        """
        if self._draggable:
            self._x = x
            self._y = y

    def SetSize(self, w: int, h: int):
        """
        Set the size of the shape.

        Args:
            w: width
            h: height of the shape
        """
        pass

    def UpdateFromModel(self):
        """
        Updates the shape position from the model in the light of a
        change of state of the diagram frame (here it's only for the zoom)
        """

        # Get the coordinates of the model (ShapeModel)
        mx, my = self.model.GetPosition()

        # Get the offsets and the ratio between the shape (view) and the
        # shape model (ShapeModel) given by the frame where the shape
        # is displayed.
        ratio = self.diagram.panel.currentZoom
        dx: int = round(self.diagram.panel.xOffSet)
        dy: int = round(self.diagram.panel.yOffSet)

        # calculation of the shape (view) coordinates in the light of the offsets and ratio
        x: int = round(ratio * mx) + dx
        y: int = round(ratio * my) + dy

        # assign the new coordinates to the shape (view). DON'T USE SetPosition(),
        # because there is a call to UpdateModel() in that method.
        if self._parent is not None:
            self._x, self._y = self.ConvertCoordToRelative(x, y)
        else:
            self._x = x
            self._y = y

    def UpdateModel(self):
        """
        Updates the coordinates of the model (ShapeModel) when the Shape (view)
        is moved.
        """

        #  get the associated model (ShapeModel)
        model = self.model

        # Get the offsets and the ratio between the shape (view) and the
        # shape model (ShapeModel) given by the frame where the shape
        # is displayed.
        from miniogl.DiagramFrame import DiagramFrame
        diagram = self.diagram
        panel: DiagramFrame   = diagram.panel   # to enable debugging and unit tests

        ratio = panel.currentZoom
        dx    = panel.xOffSet
        dy    = panel.yOffSet

        #  get the coordinates of this shape
        x, y = self.GetPosition()

        # calculation of the model coordinates in the light of the
        # offsets and ratio and assignment.
        mx = round((x - dx) // ratio)
        my = round((y - dy) // ratio)
        model.SetPosition(mx, my)

        # change also the position of the model of the children,
        # because when we move the parent children set position is not called
        # and so their update model is not called
        for child in self._anchors:
            cx, cy = child.GetPosition()
            cmx = round((cx - dx) // ratio)
            cmy = round((cy - dy) // ratio)
            child.model.SetPosition(cmx, cmy)

    def HasDiagramFrame(self):
        """

        Returns: `True` if the shape has a diagram and if this diagram has
        a diagram frame.
        """
        if self.diagram is not None:
            return self.diagram.panel is not None
        else:
            return False

    def _addPrivateText(self, x: int, y: int, text: str, font: Font = None):
        """
        Add a text shape, putting it in the private children of the shape.
        It won't be saved !!! This is used in constructor of child classes.

        Args:
            x,: position of the text, relative to the origin of the shape
            y : position of the text, relative to the origin of the shape
            text: text to add
            font: font to use

        Returns:  TextShape : the created shape
        """
        from miniogl.TextShape import TextShape

        t: TextShape = self._createTextShape(x, y, text, font=font)
        self._privateChildren.append(t)
        return t

    def _createTextShape(self, x: int, y: int, text: str, font: Font = None):
        """
        Create a text shape and add it to the diagram.

        Args:
            x,: position of the text, relative to the origin of the shape
            y : position of the text, relative to the origin of the shape
            text: text to add

            font: font to use

        Returns:  TextShape : the created shape

        """
        from miniogl.TextShape import TextShape

        textShape: TextShape = TextShape(x, y, text, parent=self, font=font)
        if self._diagram is not None:
            self._diagram.AddShape(textShape)

        return textShape


Shapes = NewType('Shapes', List[Shape])
