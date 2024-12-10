
from typing import Tuple

from wx import DC

from ogl.OglObject import OglObject

from pyutmodelv2.PyutActor import PyutActor


MARGIN: int = 10


class OglActor(OglObject):
    """
    OGL object that represent a UML actor in use case diagrams.
    This class defines OGL objects that represents an actor for Use
    Cases diagram. You can just instantiate an OGL actor and add it to
    the diagram, links, resizing, ... are managed by parent class
    `OglObject`.

    For more instructions about how to create an OGL object, please refer
    to the `OglObject` class.

    :version: $Revision: 1.9 $
    :author: Philippe Waelti
    :contact: pwaelti@eivd.ch
    """
    def __init__(self, pyutActor=None, w: int = 80, h: int = 100):
        """

        Args:
            pyutActor:

            w:  width of shape
            h:  height of shape
        """

        # Init associated PyutObject
        if pyutActor is None:
            pyutObject = PyutActor()
        else:
            pyutObject = pyutActor

        super().__init__(pyutObject, w, h)

        self._drawFrame = False

    def Draw(self, dc: DC, withChildren: bool = False):
        """
        Draw an actor

        Args:
            dc:     The device context to draw on
            withChildren:   Draw the children or not

        """
        OglObject.Draw(self, dc)
        dc.SetFont(self._defaultFont)
        # Gets the minimum bounding box for the shape
        width, height = self.GetSize()
        # Calculate the top center of the shape
        x, y = self.GetPosition()
        # drawing is restricted in the specified region of the device
        dc.SetClippingRegion(x, y, width, height)

        # Our sweet actor size
        actorWidth:   int = width
        actorHeight:  int = round(0.8 * (height - 2.0 * MARGIN))  # 80 % of total height
        actorMinSize: int = min(actorHeight, actorWidth)

        centerX, centerY, y = self._drawActorHead(dc=dc, actorMinSize=actorMinSize, height=height, width=width, x=x, y=y)
        x, y                = self._drawBodyAndArms(dc=dc, actorMinSize=actorMinSize, actorHeight=actorHeight, actorWidth=actorWidth, centerX=centerX, y=y)
        self._drawActorFeet(dc, actorHeight, actorWidth, x, y)
        self._drawBuddyName(dc, actorHeight, centerY,  height, x)

        dc.DestroyClippingRegion()

    def _drawBuddyName(self, dc: DC, actorHeight: int, centerY: int, height: int, x: int):
        """
        Args:
            dc:
            actorHeight:
            centerY:
            height:
            x:
        """

        textWidth, textHeight = dc.GetTextExtent(self.pyutObject.name)

        y = round(centerY + 0.5 * height - MARGIN - 0.1 * actorHeight)

        dc.DrawText(self.pyutObject.name, round(x - 0.5 * textWidth), y)

    def _drawActorHead(self, dc: DC, actorMinSize: int, height: int, width: int, x: int, y: int) -> Tuple[int, int, int]:
        """
        Draw our actor head
        Args:
            dc:
            height:
            actorMinSize:
            width:
            x:
            y:

        Returns:  The center coordinates (centerX, centerY) and the adjusted y position
        """
        centerX: int = x + width // 2
        centerY: int = y + height // 2

        x = round(centerX - 0.2 * actorMinSize)
        y += MARGIN

        percentageOfMinSize: int = round(0.4 * actorMinSize)
        dc.DrawEllipse(x, y, percentageOfMinSize, percentageOfMinSize)

        return centerX, centerY, y

    def _drawBodyAndArms(self, dc: DC, actorMinSize: int, actorHeight, actorWidth, centerX, y: int) -> Tuple[int, int]:
        """
        Draw body and arms
        Args:
            dc:
            actorMinSize:
            actorHeight:
            actorWidth:
            centerX:
            y:

        Returns: Updated x, y positions as a tuple
        """
        x: int = centerX
        y += round(0.4 * actorMinSize)

        dc.DrawLine(x, y, x, y + round(0.3 * actorHeight))
        dc.DrawLine(round(x - 0.25 * actorWidth), round(y + 0.15 * actorHeight),
                    round(x + 0.25 * actorWidth), round(y + 0.15 * actorHeight))
        return x, y

    def _drawActorFeet(self, dc: DC, actorHeight: int, actorWidth: int, x: int, y: int):
        """

        Args:
            dc:
            actorHeight:
            actorWidth:
            x:
            y:
        """
        actorFeetPercentage: int = round(0.3 * actorHeight)
        y += round(actorFeetPercentage)

        dc.DrawLine(x, y, x - round(0.25 * actorWidth), y + actorFeetPercentage)
        dc.DrawLine(x, y, x + round(0.25 * actorWidth), y + actorFeetPercentage)
