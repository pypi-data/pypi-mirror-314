
from logging import Logger
from logging import getLogger

from wx import BLACK
from wx import RED
from wx import Size
from wx import WHITE
from wx import PENSTYLE_SOLID
from wx import PENSTYLE_DOT

from wx import Font
from wx import Colour
from wx import MouseEvent
from wx import Pen

from wx import DC

from miniogl.Shape import Shape
from miniogl.RectangleShape import RectangleShape

from miniogl.models.TextShapeModel import TextShapeModel


TEXT_Y_MARGIN: int = 2
TEXT_X_MARGIN: int = 3

DEFAULT_WIDTH:  int = 100
DEFAULT_HEIGHT: int = 24

TEXT_HEIGHT_ADJUSTMENT: int = 12
TEXT_WIDTH_ADJUSTMENT:  int = 24


class TextShape(RectangleShape):

    clsLogger: Logger = getLogger(__name__)
    """
    A text shape that can be attached to another shape standalone).
    """
    def __init__(self, x: int, y: int, text: str, parent=None, font: Font = None):
        """

        Args:
            x:          x position of the point
            y:          y position of the point
            text:       the text that the shape displays
            parent:     parent shape
            font:       Font to use
        """
        super().__init__(x, y, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, parent=parent)

        self._text: str = text

        self._drawFrame: bool = False
        self._resizable: bool = False

        self._textColor:            Colour = BLACK
        self._textBackgroundColor:  Colour = WHITE

        self._redColor:    Colour = RED
        self._font:        Font   = font
        self._selectedPen: Pen = Pen(colour=RED, width=1, style=PENSTYLE_DOT)

        self._model: TextShapeModel = TextShapeModel(self)

    def Attach(self, diagram):
        """
        Do not use this method, use Diagram.AddShape instead !!!
        Attach the shape to a diagram.
        When you create a new shape, you must attach it to a diagram before
        you can see it. This method is used internally by Diagram.AddShape.

        Args:
            diagram
        """
        # RectangleShape.Attach(self, diagram)
        super().Attach(diagram)
        self._textBackgroundColor = self._diagram.panel.GetBackgroundColour()

    @property
    def text(self) -> str:
        """
        Returns:  The text that the text shape displays
        """
        return self._text

    @text.setter
    def text(self, newValue: str):
        """
        Set the text that the shape displays

        Args:
              newValue
        """
        self._text = newValue

    @property
    def color(self) -> Colour:
        """
        Returns The text color
        """
        return self._textColor

    @color.setter
    def color(self, color: Colour):
        """
        Sets the color of the text.

        Args:
             color
        """
        self._textColor = color

    @property
    def font(self) -> Font:
        """
        Returns:  The text shape's private font
        """
        return self._font

    @property
    def textBackground(self):
        """
        Get the text background color.

        Returns:  The text background color
        """
        return self._textBackgroundColor

    @textBackground.setter
    def textBackground(self, color: Colour):
        """
        Set the text background color.

        Args:
            color:
        """
        self._text = color

    def Draw(self, dc: DC, withChildren: bool = True):
        """
        Draw the text on the dc.

        Args:
            dc
            withChildren
        """
        if self._visible:
            super().Draw(dc=dc, withChildren=False)
            if self._selected:
                dc.SetPen(self._selectedPen)
                dc.SetTextForeground(self._redColor)
                self.DrawBorder(dc=dc)
            else:
                dc.SetTextForeground(self._textColor)

            self._computeTextSize(dc=dc)
            self._drawText(dc)

            if withChildren:
                self.DrawChildren(dc)

    def DrawBorder(self, dc: DC):
        """
        Draw the border of the shape, for fast rendering.

        Args:
            dc
        """
        if self._selected:
            RectangleShape.DrawBorder(self, dc)
        else:
            Shape.DrawBorder(self, dc)

    def UpdateFromModel(self):
        """
        Updates the shape position and size from the model in light of a
        change of state of the diagram frame.  Here it is only for the zoom
        """

        # change the position and size of the shape from the model
        # RectangleShape.UpdateFromModel(self)
        super().UpdateFromModel()
        # get the diagram frame ratio between the shape and the model
        ratio = self.diagram.panel.currentZoom

        fontSize = round(self.model.GetFontSize() * ratio)
        TextShape.clsLogger.debug(f'UpdateFromModel - ratio: {ratio}')

        # set the new font size
        if self._font is not None:
            self._font.SetPointSize(fontSize)

    def UpdateModel(self):
        """
        Updates the model when the shape (view) is displaced or resized.
        """
        # change the coordinates and size of model
        # RectangleShape.UpdateModel(self)
        super().UpdateModel()

        # get the ratio between the model and the shape (view) from
        # the diagram frame where the shape is displayed.
        ratio = self.diagram.panel.currentZoom

        # TextShape.clsLogger.debug(f'UpdateModel - ratio: {ratio}')
        if self.font is not None:
            fontSize = self.font.GetPointSize() // ratio
            self.model.SetFontSize(fontSize)

    # noinspection PyUnusedLocal
    def OnLeftDown(self, event: MouseEvent):
        """
        Callback for left clicks.
        Args:
            event:
        """
        self._selected = True

    # noinspection PyUnusedLocal
    def OnLeftUp(self, event: MouseEvent):
        """
        Callback for left clicks.

        Args:
            event:
        """
        TextShape.clsLogger.debug("Unhandled left up")

    def _computeTextSize(self, dc: DC):

        textSize:       Size = dc.GetTextExtent(self.text)
        adjustedWidth:  int  = textSize.GetWidth()  + TEXT_WIDTH_ADJUSTMENT
        adjustedHeight: int  = textSize.GetHeight() + TEXT_HEIGHT_ADJUSTMENT

        self.clsLogger.debug(f'{textSize=} {adjustedWidth=} {adjustedHeight=}')
        self.SetSize(width=adjustedWidth, height=adjustedHeight)

    def _drawText(self, dc: DC):

        dc.SetBackgroundMode(PENSTYLE_SOLID)
        dc.SetTextBackground(self._textBackgroundColor)

        x, y = self.GetPosition()
        # draw the text shape with its own font
        saveFont: Font = dc.GetFont()

        if self.font is not None:
            dc.SetFont(self.font)
        dc.DrawText(self._text, x + TEXT_X_MARGIN, y + TEXT_Y_MARGIN)

        dc.SetFont(saveFont)

    def __str__(self) -> str:
        x, y = self.GetPosition()
        return f'TextShape[{self._text=} position: ({x},{y}])'

    def __repr__(self):
        return self.__str__()
