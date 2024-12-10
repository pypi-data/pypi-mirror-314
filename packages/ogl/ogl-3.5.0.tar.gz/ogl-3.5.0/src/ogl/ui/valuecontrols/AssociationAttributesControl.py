
from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from wx import CB_READONLY
from wx import CommandEvent
from wx import EVT_COMBOBOX
from wx import ID_ANY

from wx import ComboBox
from wx import StaticText
from wx import Window

from wx.lib.sized_controls import SizedPanel


from ogl.preferences.OglPreferences import OglPreferences


class AssociationAttributesControl(SizedPanel):

    def __init__(self, parent: Window):

        self.logger:       Logger         = getLogger(__name__)
        self._preferences: OglPreferences = OglPreferences()
        super().__init__(parent)
        self.SetSizerType('horizontal')

        self._textFontSize: ComboBox = cast(ComboBox, None)
        self._diamondSize:  ComboBox = cast(ComboBox, None)

        self._layoutControls(parentPanel=self)
        self._setControlValues()

        self.Bind(EVT_COMBOBOX, self._onTextFontSizedChanged, self._textFontSize)
        self.Bind(EVT_COMBOBOX, self._onDiamondSizeChanged,   self._diamondSize)

    def _layoutControls(self, parentPanel: SizedPanel):

        fontSizes:    List[str] = ['8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']
        diamondSizes: List[str] = ['6', '7', '8', '10', '11', '12', '13', '14', '15']

        formPanel: SizedPanel = SizedPanel(parentPanel)
        formPanel.SetSizerType('form')

        # First Line
        StaticText(formPanel, ID_ANY, 'Font Size')
        self._textFontSize = ComboBox(formPanel, choices=fontSizes, style=CB_READONLY)

        # Second Line
        StaticText(formPanel, ID_ANY, 'Diamond Size')
        self._diamondSize = ComboBox(formPanel, choices=diamondSizes, style=CB_READONLY)

    def _setControlValues(self):
        self._textFontSize.SetValue(str(self._preferences.associationTextFontSize))
        self._diamondSize.SetValue(str(self._preferences.diamondSize))

    def _onTextFontSizedChanged(self, event: CommandEvent):
        newFontSize: str = event.GetString()
        self._preferences.associationTextFontSize = int(newFontSize)

    def _onDiamondSizeChanged(self, event: CommandEvent):
        newDiamondSize: str = event.GetString()
        self._preferences.associationDiamondSize = int(newDiamondSize)
