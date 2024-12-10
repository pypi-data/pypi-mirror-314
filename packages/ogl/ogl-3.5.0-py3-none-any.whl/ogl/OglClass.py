
from typing import Tuple
from typing import cast

from logging import Logger
from logging import getLogger

from dataclasses import dataclass

from wx import DC
from wx import FONTFAMILY_SWISS
from wx import FONTSTYLE_NORMAL
from wx import FONTWEIGHT_BOLD

from wx import Font
from wx import ClientDC
from wx import MouseEvent
from wx import Point
from wx import Brush
from wx import Colour

from pyutmodelv2.enumerations.PyutDisplayMethods import PyutDisplayMethods
from pyutmodelv2.enumerations.PyutDisplayParameters import PyutDisplayParameters
from pyutmodelv2.enumerations.PyutStereotype import PyutStereotype

from pyutmodelv2.PyutMethod import PyutMethod
from pyutmodelv2.PyutObject import PyutObject
from pyutmodelv2.PyutClass import PyutClass

from miniogl.MiniOglColorEnum import MiniOglColorEnum
from miniogl.SelectAnchorPoint import SelectAnchorPoint

from ogl.OglDimensions import OglDimensions
from ogl.OglObject import OglObject
from ogl.OglObject import DEFAULT_FONT_SIZE

from ogl.events.OglEvents import OglEventType

from ogl.preferences.OglPreferences import OglPreferences

from ogl.ui.OglClassMenuHandler import OglClassMenuHandler

DUNDER_METHOD_INDICATOR: str = '__'
CONSTRUCTOR_NAME:        str = '__init__'

MARGIN: int = 10
#
#  When I added optional display of constructor and dunder methods, I introduced this bug
#  I'll fix this later
#
HACK_FIX_AUTO_RESIZE: bool = True   # TODO:  This should be a debug flag


@dataclass
class ClickedOnSelectAnchorPointData:
    clicked:           bool             = False
    selectAnchorPoint: SelectAnchorPoint = cast(SelectAnchorPoint, None)


class OglClass(OglObject):
    """
    OGL object that represents a modeling class in class diagrams.
    This Python class defines a graphical object that represents a specific UML class.
    You instantiate an OGL class and add it to the diagram.
    Links, resizing, are managed by parent class `OglObject`.

    For more instructions about how to create an OGL object, refer
    to the `OglObject` class.
    """
    def __init__(self, pyutClass: PyutClass | None, w: int = 0, h: int = 0):
        """

        Args:
            pyutClass: a PyutClass object
            w: Width of the shape
            h: Height of the shape
        """
        if pyutClass is None:
            pyutObject = PyutClass()
        else:
            pyutObject = pyutClass

        width:  int = w
        height: int = h

        self._oglPreferences: OglPreferences = OglPreferences()

        # Use preferences to get initial size if not specified
        # Note: auto_resize_shape_on_edit must be False for this size to actually stick
        if w == 0:
            width = self._oglPreferences.classDimensions.width
        if h == 0:
            height = self._oglPreferences.classDimensions.height

        super().__init__(pyutObject, width=width, height=height)

        self._nameFont:  Font             = Font(DEFAULT_FONT_SIZE, FONTFAMILY_SWISS, FONTSTYLE_NORMAL, FONTWEIGHT_BOLD)
        oglTextColor:    MiniOglColorEnum = self._oglPreferences.classTextColor
        self._textColor: Colour           = Colour(MiniOglColorEnum.toWxColor(oglTextColor))

        oglBackgroundColor: MiniOglColorEnum = self._oglPreferences.classBackGroundColor
        backgroundColor:    Colour           = Colour(MiniOglColorEnum.toWxColor(oglBackgroundColor))

        self.brush = Brush(backgroundColor)

        self.logger:    Logger = getLogger(__name__)

        self._menuHandler: OglClassMenuHandler = cast(OglClassMenuHandler, None)

    def handleSelectAnchorPointSelection(self, event: MouseEvent):
        """
        May be called (inexcusably bad form) by the selection anchor point left down handler
        by using its parent protected attribute

        Args:
            event:
        """
        self.logger.info(f'OnLeftDown: {event.GetPosition()}')
        # noinspection PyPropertyAccess
        clickPoint: Point = event.Position
        selectData: ClickedOnSelectAnchorPointData = self._didWeClickOnSelectAnchorPoint(clickPoint=clickPoint)
        if selectData.clicked is True:
            self.eventEngine.sendEvent(OglEventType.CreateLollipopInterface, implementor=self, attachmentPoint=selectData.selectAnchorPoint)

    def GetTextWidth(self, dc, text):
        width = dc.GetTextExtent(text)[0]
        return width

    def GetTextHeight(self, dc, text):
        height = dc.GetTextExtent(text)[1]
        return height

    def Draw(self, dc, withChildren=False):
        """
        Paint handler, draws the content of the shape.

        WARNING: Every change here must be reported in autoResize pyutMethod

        Args:
            dc: device context to draw to
            withChildren: A boolean indicating whether to draw this figure's children
        """

        pyutObject: PyutClass = cast(PyutClass, self.pyutObject)

        # Draw rectangle shape
        super().Draw(dc)
        # drawing is restricted in the specified region of the device
        w, h = self._width, self._height
        x, y = self.GetPosition()           # Get position
        dc.SetClippingRegion(x, y, w, h)

        # Draw header
        (headerX, headerY, headerW, headerH) = self._drawClassHeader(dc, True)
        y = headerY + headerH

        if pyutObject.showFields is True:
            # Draw line
            dc.DrawLine(x, y, x + w, y)

            # Draw fields
            (fieldsX, fieldsY, fieldsW, fieldsH) = self._drawClassFields(dc, True, initialY=y)
            y = fieldsY + fieldsH
        # Draw line
        dc.DrawLine(x, y, x + w, y)
        #
        # Method needs to be called even though returned values not used  -- TODO look at refactoring
        #
        if pyutObject.showMethods is True:
            (methodsX, methodsY, methodsW, methodsH) = self._drawClassMethods(dc=dc, initialY=y)
            # noinspection PyUnusedLocal
            y = methodsY + methodsH
            if methodsW > self._width:
                self._width = methodsW

        dc.DestroyClippingRegion()

    def autoResize(self):
        """
        Auto-resize the class

        WARNING: Every change here must be reported in DRAW pyutMethod
        """
        # Init
        pyutObject: PyutClass = cast(PyutClass, self.pyutObject)
        umlFrame = self.diagram.panel
        dc = ClientDC(umlFrame)

        # Get header size
        (headerX, headerY, headerW, headerH) = self._drawClassHeader(dc, False, calcWidth=True)
        y = headerY + headerH

        # Get the size of the field's portion of the display
        if pyutObject.showFields is True:
            (fieldsX, fieldsY, fieldsW, fieldsH) = self._drawClassFields(dc, False, initialY=y)
            y = fieldsY + fieldsH
        else:
            fieldsW, fieldsH = 0, 0

        # Get method's size
        if pyutObject.showMethods is True:
            (methodX, methodY, methodW, methodH) = self._drawClassMethods(dc=dc, initialY=y)
            y = methodY + methodH
        else:
            methodW, methodH = 0, 0

        w = max(headerW, fieldsW, methodW)
        h = y - headerY
        w += 2 * MARGIN

        minDimensions: OglDimensions = self._oglPreferences.classDimensions
        if w < minDimensions.width:
            w = minDimensions.width
        if h < minDimensions.height:
            h = minDimensions.height

        if HACK_FIX_AUTO_RESIZE is True:
            w = w - 20      # Hack keeps growing
        self.SetSize(w, h)

        # to automatically replace the sizer objects at a correct place
        if self.selected is True:
            self.selected = False
            self.selected = True

        self.eventEngine.sendEvent(OglEventType.DiagramFrameModified)

    def OnRightDown(self, event: MouseEvent):
        """
        Callback for right clicks
        """
        if self._menuHandler is None:
            self._menuHandler = OglClassMenuHandler(oglClass=self, eventEngine=self.eventEngine)

        self._menuHandler.popupMenu(event=event)

    def _didWeClickOnSelectAnchorPoint(self, clickPoint: Point) -> ClickedOnSelectAnchorPointData:
        """

        Args:
            clickPoint:

        Returns: Data class with relevant information
        """
        from miniogl.Shape import Shape

        selectData: ClickedOnSelectAnchorPointData = ClickedOnSelectAnchorPointData(clicked=False)
        anchors = self.anchors
        for shape in anchors:
            child: Shape = cast(Shape, shape)
            if isinstance(child, SelectAnchorPoint):
                selectAnchorPoint: SelectAnchorPoint = cast(SelectAnchorPoint, child)
                x, y = clickPoint.Get()
                if selectAnchorPoint.Inside(x=x, y=y):
                    selectData.selectAnchorPoint = child
                    selectData.clicked           = True
                    break

        return selectData

    def _isSameName(self, other) -> bool:

        ans: bool = False
        selfPyutObj:  PyutObject = self.pyutObject
        otherPyutObj: PyutObject = other.pyutObject

        if selfPyutObj.name == otherPyutObj.name:
            ans = True
        return ans

    def _isSameId(self, other):

        ans: bool = False
        if self.id == other.id:
            ans = True
        return ans

    def _drawClassHeader(self, dc: DC, draw: bool = False, initialX=None, initialY=None, calcWidth: bool = False):
        """
        Calculate the class header position and size and display it if
        a draw is True

        Args:
            dc:
            draw:
            initialX:
            initialY:
            calcWidth:

        Returns: tuple (x, y, w, h) = position and size of the header
        """
        # Init
        dc.SetFont(self._defaultFont)
        dc.SetTextForeground(self._textColor)

        x, y = self.GetPosition()
        if initialX is not None:
            x = initialX
        if initialY is not None:
            y = initialY
        w = self._width
        h = 0
        if calcWidth:
            w = 0

        # define space between the text and line
        lth = dc.GetTextExtent("*")[1] // 2

        # from where begin the text
        h += lth

        # draw a pyutClass name
        name: str = self.pyutObject.name
        dc.SetFont(self._nameFont)
        nameWidth: int = self.GetTextWidth(dc, name)
        if draw:
            dc.DrawText(name, x + (w - nameWidth) // 2, y + h)
        if calcWidth:
            w = max(nameWidth, w)
        dc.SetFont(self._defaultFont)
        h += self.GetTextHeight(dc, str(name))
        h += lth
        #
        # Draw the stereotype value
        #
        pyutClass: PyutClass = self.pyutObject
        stereo: PyutStereotype = pyutClass.stereotype

        if pyutClass.displayStereoType is True and stereo is not None and stereo != PyutStereotype.NO_STEREOTYPE:
            stereoTypeValue: str = f'<<{stereo.value}>>'
        else:
            stereoTypeValue = ''

        stereoTypeValueWidth = self.GetTextWidth(dc, stereoTypeValue)
        if draw:
            dc.DrawText(stereoTypeValue, x + (w - stereoTypeValueWidth) // 2, y + h)
        if calcWidth:
            w = max(stereoTypeValueWidth, w)
        h += self.GetTextHeight(dc, str(stereoTypeValue))
        h += lth

        # Return sizes
        return x, y, w, h

    def _drawClassFields(self, dc, draw=False, initialX=None, initialY=None, calcWidth=False):
        """
        Calculate the class fields position and size and display it if
        a draw is True

        Args:
            dc:
            draw:
            initialX:
            initialY:
            calcWidth:

        Returns: A tuple (x, y, w, h) = position and size of the field
        """
        # Init
        dc.SetFont(self._defaultFont)
        dc.SetTextForeground(self._textColor)

        x, y = self.GetPosition()
        if initialX is not None:
            x = initialX
        if initialY is not None:
            y = initialY
        w = self._width
        h = 0
        if calcWidth:
            w = 0

        # Define the space between the text and the line
        lth: int = dc.GetTextExtent("*")[1] // 2

        # Add space
        pyutClass: PyutClass = cast(PyutClass, self.pyutObject)
        if len(pyutClass.fields) > 0:
            h += lth

        # draw pyutClass fields
        if pyutClass.showFields is True:
            for field in pyutClass.fields:
                if draw:
                    dc.DrawText(str(field), x + MARGIN, y + h)
                if calcWidth:
                    w = max(w, self.GetTextWidth(dc, str(field)))

                h += self.GetTextHeight(dc, str(field))

        # Add space
        if len(pyutClass.fields) > 0:
            h += lth

        # Return sizes
        return x, y, w, h

    def _drawClassMethods(self, dc, initialY=None) -> Tuple[int, int, int, int]:
        """
        Calculate the class methods position and size and display it if
        a showMethods is True

        Args:
            dc:
            initialY:

        Returns: tuple (x, y, w, h) which is position and size of the method's portion of the OglClass
        """

        dc.SetFont(self._defaultFont)
        dc.SetTextForeground(self._textColor)

        x, y = self.GetPosition()

        if initialY is not None:
            y = initialY
        w: int = 0
        h: int = 0

        # Define the space between the text and the line
        lth = dc.GetTextExtent("*")[1] // 2

        # Add space
        pyutClass: PyutClass = cast(PyutClass, self.pyutObject)
        if len(pyutClass.methods) > 0:
            h += lth

        # draw pyutClass methods
        self.logger.debug(f"showMethods => {pyutClass.showMethods}")
        if pyutClass.showMethods is True:
            for method in pyutClass.methods:
                if self._eligibleToDraw(pyutClass=pyutClass, pyutMethod=method) is True:

                    self._drawMethod(dc, method, pyutClass, x, y, h)

                    pyutMethod: PyutMethod = cast(PyutMethod, method)
                    if pyutClass.displayParameters == PyutDisplayParameters.WITH_PARAMETERS or self._oglPreferences.showParameters is True:
                        w = max(w, self.GetTextWidth(dc, str(pyutMethod.methodWithParameters())))
                    else:
                        w = max(w, self.GetTextWidth(dc, str(pyutMethod.methodWithoutParameters())))
                    h += self.GetTextHeight(dc, str(method))

        # Add space
        if len(pyutClass.methods) > 0:
            h += lth

        # Return sizes
        return x, y, w, h

    def _drawMethod(self, dc: DC, pyutMethod: PyutMethod, pyutClass: PyutClass, x: int, y: int, h: int):
        """
        If the preference is not set at the individual class level, then defer to global preference; Otherwise,
        respect the class level preference

        Args:
            dc:
            pyutMethod:
            pyutClass:
            x:
            y:
            h:
        """
        self.logger.debug(f'{pyutClass.displayParameters=} - {self._oglPreferences.showParameters=}')
        dc.SetTextForeground(self._textColor)
        if pyutClass.displayParameters == PyutDisplayParameters.UNSPECIFIED:
            if self._oglPreferences.showParameters is True:
                dc.DrawText(pyutMethod.methodWithParameters(), x + MARGIN, y + h)
            else:
                dc.DrawText(pyutMethod.methodWithoutParameters(), x + MARGIN, y + h)
        elif pyutClass.displayParameters == PyutDisplayParameters.WITH_PARAMETERS:
            dc.DrawText(pyutMethod.methodWithParameters(), x + MARGIN, y + h)
        elif pyutClass.displayParameters == PyutDisplayParameters.WITHOUT_PARAMETERS:
            dc.DrawText(pyutMethod.methodWithoutParameters(), x + MARGIN, y + h)
        else:
            assert False, 'Internal error unknown pyutMethod parameter display type'

    def _eligibleToDraw(self, pyutClass: PyutClass, pyutMethod: PyutMethod):
        """
        Is it one of those 'special' dunder methods?

        Args:
            pyutClass: The class we need to check
            pyutMethod: The particular method we are asked about

        Returns: `True` if we can draw it, `False` if we should not
        """

        ans: bool = True

        methodName: str = pyutMethod.name
        if methodName == CONSTRUCTOR_NAME:
            ans = self._checkConstructor(pyutClass=pyutClass)
        elif methodName.startswith(DUNDER_METHOD_INDICATOR) and methodName.endswith(DUNDER_METHOD_INDICATOR):
            ans = self._checkDunderMethod(pyutClass=pyutClass)

        return ans

    def _checkConstructor(self, pyutClass: PyutClass) -> bool:
        """
        If class property is UNSPECIFIED, defer to the global value; otherwise check the local value

        Args:
            pyutClass: The specified class to check

        Returns: Always `True` unless the specific class says `False` or class does not care then returns
        `False` if the global value says so
        """
        ans: bool = self._allowDraw(classProperty=pyutClass.displayConstructor, globalValue=self._oglPreferences.displayConstructor)

        return ans

    def _checkDunderMethod(self, pyutClass: PyutClass):
        """
        If class property is UNSPECIFIED, defer to the global value; otherwise check the local value

        Args:
            pyutClass: The specified class to check

        Returns: Always `True` unless the specific class says `False` or class does not care then returns
        `False` if the global value says so
        """
        ans: bool = self._allowDraw(classProperty=pyutClass.displayDunderMethods, globalValue=self._oglPreferences.displayDunderMethods)

        return ans

    def _allowDraw(self, classProperty: PyutDisplayMethods, globalValue: bool) -> bool:
        ans: bool = True

        if classProperty == PyutDisplayMethods.UNSPECIFIED:
            if globalValue is False:
                ans = False
        else:
            if classProperty == PyutDisplayMethods.DO_NOT_DISPLAY:
                ans = False

        return ans

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        selfName: str = self.pyutObject.name
        modelId:  int = self.pyutObject.id
        return f'OglClass.{selfName} modelId: {modelId}'

    def __eq__(self, other) -> bool:

        if isinstance(other, OglClass):
            if self._isSameName(other) is True and self._isSameId(other) is True:
                return True
            else:
                return False
        else:
            return False

    def __hash__(self):

        selfPyutObj:  PyutObject = self.pyutObject

        return hash(selfPyutObj.name) + hash(self.id)
