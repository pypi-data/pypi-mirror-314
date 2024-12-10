"""
This is a suite of small classes used to draw RotatableShapes.
Each one represent a simple shape (line, rectangle, circle, ellipse...)
or abstract command (color change).
"""
from typing import List
from typing import NewType
from typing import cast

from abc import ABC
from abc import abstractmethod

from dataclasses import dataclass

from logging import Logger
from logging import getLogger

from wx import DC


@dataclass(kw_only=True)
class VShapePosition:
    x: int = 0
    y: int = 0

    def __iter__(self):
        return iter((self.x, self.y))


VShapePositions = NewType('VShapePositions', List[VShapePosition])


@dataclass(kw_only=True)
class VShapeSize:
    width:  int = 99
    height: int = 49


@dataclass
class VBasicDetails(VShapePosition, VShapeSize):
    pass


@dataclass
class VRectangleDetails(VBasicDetails):
    pass


@dataclass
class VEllipseDetails(VBasicDetails):
    pass


@dataclass
class VCircleDetails(VShapePosition):
    radius: int = 0


@dataclass
class VArcDetails:
    xStart:  int = 0
    yStart:  int = 0
    xEnd:    int = 0
    yEnd:    int = 0
    xCenter: int = 0
    yCenter: int = 0


@dataclass
class ShapeData:
    start:  int = 0
    end:    int = 0
    w:      int = 0
    h:      int = 0


@dataclass(kw_only=True)
class VEllipticArcDetails(VBasicDetails):
    start: int = 0
    end:   int = 0

    def __iter__(self):
        return iter((self.x, self.y, self.width, self.height, self.start, self.end))


class VShape(ABC):
    """
    Base VShape class.

    """
    def __init__(self):
        pass

    @classmethod
    def convert(cls, angle, x, y):
        T = [
            [1, 0, 0, 1], [0, -1, 1, 0], [-1, 0, 0, -1], [0, 1, -1, 0]
        ]
        nx = T[angle][0] * x + T[angle][1] * y
        ny = T[angle][2] * x + T[angle][3] * y
        return nx, ny

    @abstractmethod
    def SetAngle(self, angle):
        pass

    def Scale(self, factor, data):
        return map(lambda x: x * factor, data)


class VBasicShape(VShape, ABC):
    def __init__(self, vBasicDetails: VBasicDetails):
        super().__init__()

        self._vBasicDetails: vBasicDetails = vBasicDetails

    def scale(self, factor: int) -> VBasicDetails:

        if factor == 1:
            x: int = self._vBasicDetails.x
            y: int = self._vBasicDetails.y
            w: int = self._vBasicDetails.width
            h: int = self._vBasicDetails.height
        else:
            x: int = self._vBasicDetails.x * factor
            y: int = self._vBasicDetails.y * factor
            w: int = self._vBasicDetails.width  * factor
            h: int = self._vBasicDetails.height * factor

        return VBasicDetails(x=x, y=y, width=w, height=h)


class VRectangle(VBasicShape):
    def __init__(self, vRectangleDetails: VRectangleDetails):
        """

        Args:
            vRectangleDetails
        """
        super().__init__(vBasicDetails=vRectangleDetails)

    def SetAngle(self, angle):
        x: int = self._vBasicDetails.x
        y: int = self._vBasicDetails.y
        w: int = self._vBasicDetails.width
        h: int = self._vBasicDetails.height

        x, y = self.convert(angle, x, y)
        w, h = self.convert(angle, w, h)
        self._vBasicDetails = VRectangleDetails(x=x, y=y, width=w, height=h)

    def Draw(self, dc: DC, ox, oy, scale):

        scaledDetails: VBasicDetails = self.scale(scale)
        dc.DrawRectangle(ox + scaledDetails.x, oy + scaledDetails.y, scaledDetails.width, scaledDetails.height)


class VEllipse(VBasicShape):
    def __init__(self, vEllipseDetails: VEllipseDetails):
        super().__init__(vBasicDetails=vEllipseDetails)

    def SetAngle(self, angle):
        x: int = self._vBasicDetails.x
        y: int = self._vBasicDetails.y
        w: int = self._vBasicDetails.width
        h: int = self._vBasicDetails.height

        x, y = self.convert(angle, x, y)
        w, h = self.convert(angle, w, h)
        self._vBasicDetails = VRectangleDetails(x=x, y=y, width=w, height=h)

    def Draw(self, dc, ox, oy, scale):

        scaledDetails: VBasicDetails = self.scale(scale)
        dc.DrawEllipse(ox + scaledDetails.x, oy + scaledDetails.y, scaledDetails.width, scaledDetails.height)


class VCircle(VShape):
    def __init__(self, vCircleDetails: VCircleDetails):
        super().__init__()
        self._vCircleDetails: VCircleDetails = vCircleDetails

    def SetAngle(self, angle):
        x, y = self.convert(angle, self._vCircleDetails.x, self._vCircleDetails.y)
        self._vCircleDetails = VCircleDetails(x=x, y=y, radius=self._vCircleDetails.radius)

    def Draw(self, dc, ox, oy, scale):
        vCircleDetails: VCircleDetails = self.scale(scale)
        dc.DrawCircle(ox + vCircleDetails.x, oy + vCircleDetails.y, vCircleDetails.radius)

    def scale(self, factor: int) -> VCircleDetails:

        x: int = self._vCircleDetails.x * factor
        y: int = self._vCircleDetails.y * factor
        r: int = self._vCircleDetails.radius * factor

        return VCircleDetails(x=x, y=y, radius=r)


class VArc(VShape):
    def __init__(self, vArcDetails: VArcDetails):
        super().__init__()
        self._vArcDetails: VArcDetails = vArcDetails

    def SetAngle(self, angle):
        # x1, y1, x2, y2, xc, yc = self._data
        x1: int = self._vArcDetails.xStart
        y1: int = self._vArcDetails.yStart
        x2: int = self._vArcDetails.xEnd
        y2: int = self._vArcDetails.yEnd
        xc: int = self._vArcDetails.xCenter
        yc: int = self._vArcDetails.yCenter

        x1, y1 = self.convert(angle, x1, y1)
        x2, y2 = self.convert(angle, x2, y2)
        xc, yc = self.convert(angle, xc, yc)
        # self._data = (x1, y1, x2, y2, xc, yc)
        self._vArcDetails = VArcDetails(xStart=x1, yStart=y1, xEnd=x2, yEnd=y2, xCenter=xc, yCenter=yc)

    def Draw(self, dc, ox, oy, scale):
        self._vArcDetails = self.scale(scale)
        # dc.DrawArc(ox + x1, oy + y1, ox + x2, oy + y2, ox + xc, oy + yc)
        dc.DrawArc(ox + self._vArcDetails.xStart,
                   oy + self._vArcDetails.yStart,
                   ox + self._vArcDetails.xEnd,
                   oy + self._vArcDetails.yEnd,
                   ox + self._vArcDetails.xCenter,
                   oy + self._vArcDetails.yCenter)

    def scale(self, factor: int) -> VArcDetails:

        x1: int = self._vArcDetails.xStart * factor
        y1: int = self._vArcDetails.yStart * factor
        x2: int = self._vArcDetails.xEnd * factor
        y2: int = self._vArcDetails.yEnd * factor
        xc: int = self._vArcDetails.xCenter * factor
        yc: int = self._vArcDetails.yCenter * factor

        return VArcDetails(xStart=x1, yStart=y1, xEnd=x2, yEnd=y2, xCenter=xc, yCenter=yc)


class VEllipticArc(VShape):
    def __init__(self, details: VEllipticArcDetails):
        super().__init__()
        self.logger: Logger = getLogger(__name__)
        self._details: VEllipticArcDetails = details

    def SetAngle(self, angle):
        x, y, w, h, start, end  = self._details
        x, y = self.convert(angle, x, y)
        w, h = self.convert(angle, w, h)
        start -= angle * 90
        end -= angle * 90
        self._details = VEllipticArcDetails(x=x, y=y, width=w, height=h, start=start, end=end)

    def Draw(self, dc, ox, oy, scale):
        if scale == 1:
            x, y, w, h, start, end  = self._details
            self.logger.debug(f'Draw: {self._details=}')
        else:
            x, y, w, h = self.Scale(scale, self._details[0:4])
            start, end = self._details[4:]
        dc.DrawEllipticArc(ox + x, oy + y, w, h, start, end)


class VLineLength(VShape):
    def __init__(self, x, y, w, h):
        super().__init__()
        self._data = ShapeData(x, y, w, h)

    def SetAngle(self, angle):
        x, y, w, h = self._data
        x, y = self.convert(angle, x, y)
        w, h = self.convert(angle, w, h)
        self._data = (x, y, w, h)

    def Draw(self, dc, ox, oy, scale):
        if scale == 1:
            x, y, w, h = self._data
        else:
            x, y, w, h = self.Scale(scale, self._data)
        x, y = ox + x, oy + y
        dc.DrawLine(x, y, x + w, y + h)


class VLineDest(VShape):
    def __init__(self, sx, sy, dx, dy):
        super().__init__()
        self._data = (sx, sy, dx, dy)

    def SetAngle(self, angle):
        sx, sy, dx, dy = self._data
        sx, sy = self.convert(angle, sx, sy)
        dx, dy = self.convert(angle, dx, dy)
        self._data = (sx, sy, dx, dy)

    def Draw(self, dc, ox, oy, scale):
        if scale == 1:
            sx, sy, dx, dy = self._data
        else:
            sx, sy, dx, dy = self.Scale(scale, self._data)
        dc.DrawLine(ox + sx, oy + sy, ox + dx, oy + dy)


class VPolygon(VShape):
    def __init__(self, points: VShapePositions):
        super().__init__()
        self._points = points

    def SetAngle(self, angle):
        new: VShapePositions = VShapePositions([])

        for pt in self._points:
            vShapePosition: VShapePosition = cast(VShapePosition, pt)
            x: int = vShapePosition.x
            y: int = vShapePosition.y

            x, y = self.convert(angle, x, y)
            newPt: VShapePosition = VShapePosition(x=x, y=y)
            new.append(newPt)

        self._points = tuple(new)

    def Draw(self, dc, ox, oy, scale):
        if scale == 1:
            points = []
            for pt in self._points:
                vShapePosition: VShapePosition = cast(VShapePosition, pt)
                x: int = vShapePosition.x
                y: int = vShapePosition.y

                points.append((x, y))
        else:
            points = []
            for pt in self._points:
                vShapePosition: VShapePosition = cast(VShapePosition, pt)

                x: int = vShapePosition.x
                y: int = vShapePosition.y

                points.append(tuple(self.Scale(scale, (x, y))))

        dc.DrawPolygon(points, ox, oy)


class VPen(VShape):
    def __init__(self, pen):
        super().__init__()
        self._pen = pen

    def SetAngle(self, angle):
        pass

    # noinspection PyUnusedLocal
    def Draw(self, dc, x, y, scale=1):
        dc.SetPen(self._pen)


class VBrush(VShape):
    def __init__(self, brush):
        super().__init__()
        self._brush = brush

    def SetAngle(self, angle):
        pass

    # noinspection PyUnusedLocal
    def Draw(self, dc, x, y, scale=1):
        dc.SetBrush(self._brush)
