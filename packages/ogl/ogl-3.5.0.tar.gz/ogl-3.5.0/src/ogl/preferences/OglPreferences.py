
from logging import Logger
from logging import getLogger

from codeallybasic.SecureConversions import SecureConversions
from codeallybasic.SingletonV3 import SingletonV3

from miniogl.MiniOglColorEnum import MiniOglColorEnum
from miniogl.MiniOglPenStyle import MiniOglPenStyle

from ogl.OglDimensions import OglDimensions
from ogl.OglTextFontFamily import OglTextFontFamily

from codeallybasic.DynamicConfiguration import DynamicConfiguration
from codeallybasic.DynamicConfiguration import KeyName
from codeallybasic.DynamicConfiguration import SectionName
from codeallybasic.DynamicConfiguration import Sections
from codeallybasic.DynamicConfiguration import ValueDescription
from codeallybasic.DynamicConfiguration import ValueDescriptions

MODULE_NAME:           str = 'ogl'
PREFERENCES_FILE_NAME: str = f'{MODULE_NAME}.ini'

DEFAULT_CLASS_BACKGROUND_COLOR: str = MiniOglColorEnum.MINT_CREAM.value
DEFAULT_CLASS_TEXT_COLOR:       str = MiniOglColorEnum.BLACK.value
DEFAULT_GRID_LINE_COLOR:        str = MiniOglColorEnum.LIGHT_GREY.value
DEFAULT_GRID_LINE_STYLE:        str = MiniOglPenStyle.DOT.value

oglProperties: ValueDescriptions = ValueDescriptions(
    {
        KeyName('textValue'):            ValueDescription(defaultValue='fac America magna iterum'),
        KeyName('noteText'):             ValueDescription(defaultValue='This is the note text'),
        KeyName('noteDimensions'):       ValueDescription(defaultValue=str(OglDimensions(100, 50)), deserializer=OglDimensions.deSerialize),
        KeyName('textDimensions'):       ValueDescription(defaultValue=str(OglDimensions(125, 50)), deserializer=OglDimensions.deSerialize),
        KeyName('textBold'):             ValueDescription(defaultValue='False',                     deserializer=SecureConversions.secureBoolean),
        KeyName('textItalicize'):        ValueDescription(defaultValue='False',                     deserializer=SecureConversions.secureBoolean),
        KeyName('textFontFamily'):       ValueDescription(defaultValue='Swiss',                     deserializer=OglTextFontFamily.deSerialize),
        KeyName('textFontSize'):         ValueDescription(defaultValue='14',                        deserializer=SecureConversions.secureInteger),
        KeyName('displayConstructor'):   ValueDescription(defaultValue='True',                      deserializer=SecureConversions.secureBoolean),
        KeyName('displayDunderMethods'): ValueDescription(defaultValue='True',                      deserializer=SecureConversions.secureBoolean),
        KeyName('classDimensions'):      ValueDescription(defaultValue=str(OglDimensions(150, 75)), deserializer=OglDimensions.deSerialize),
        KeyName('classBackGroundColor'): ValueDescription(defaultValue=DEFAULT_CLASS_BACKGROUND_COLOR, enumUseValue=True, deserializer=MiniOglColorEnum),
        KeyName('classTextColor'):       ValueDescription(defaultValue=DEFAULT_CLASS_TEXT_COLOR,       enumUseValue=True, deserializer=MiniOglColorEnum),
    }
)
diagramProperties: ValueDescriptions = ValueDescriptions(
    {
        KeyName('centerDiagram'):          ValueDescription(defaultValue='False', deserializer=SecureConversions.secureBoolean),
        KeyName('backGroundGridEnabled'):  ValueDescription(defaultValue='True',  deserializer=SecureConversions.secureBoolean),
        KeyName('snapToGrid'):             ValueDescription(defaultValue='True',  deserializer=SecureConversions.secureBoolean),
        KeyName('showParameters'):         ValueDescription(defaultValue='False', deserializer=SecureConversions.secureBoolean),
        KeyName('backgroundGridInterval'): ValueDescription(defaultValue='25',    deserializer=SecureConversions.secureInteger),
        KeyName('gridLineColor'):          ValueDescription(defaultValue=DEFAULT_GRID_LINE_COLOR, enumUseValue=True, deserializer=MiniOglColorEnum),
        KeyName('gridLineStyle'):          ValueDescription(defaultValue=DEFAULT_GRID_LINE_STYLE, enumUseValue=True, deserializer=MiniOglPenStyle),
    }
)

namePreferences: ValueDescriptions = ValueDescriptions(
    {
        KeyName('defaultClassName'):     ValueDescription(defaultValue='ClassName'),
        KeyName('defaultNameInterface'): ValueDescription(defaultValue='IClassInterface'),
        KeyName('defaultNameUsecase'):   ValueDescription(defaultValue='UseCaseName'),
        KeyName('defaultNameActor'):     ValueDescription(defaultValue='ActorName'),
        KeyName('defaultNameMethod'):    ValueDescription(defaultValue='MethodName'),
        KeyName('defaultNameField'):     ValueDescription(defaultValue='FieldName'),
        KeyName('defaultNameParameter'): ValueDescription(defaultValue='ParameterName'),
    }
)
sequenceDiagramPreferences: ValueDescriptions = ValueDescriptions(
    {
        KeyName('instanceYPosition'):  ValueDescription(defaultValue='50',                         deserializer=SecureConversions.secureInteger),
        KeyName('instanceDimensions'): ValueDescription(defaultValue=str(OglDimensions(100, 400)), deserializer=OglDimensions.deSerialize)
    }
)
associationsPreferences: ValueDescriptions = ValueDescriptions(
    {
        KeyName('associationTextFontSize'): ValueDescription(defaultValue='12', deserializer=SecureConversions.secureInteger),
        KeyName('diamondSize'):             ValueDescription(defaultValue='7',  deserializer=SecureConversions.secureInteger),
    }
)
debugPreferences: ValueDescriptions = ValueDescriptions(
    {
        KeyName('debugDiagramFrame'): ValueDescription(defaultValue='False', deserializer=SecureConversions.secureBoolean),
        KeyName('debugBasicShape'):   ValueDescription(defaultValue='False', deserializer=SecureConversions.secureBoolean),
    }
)

sections: Sections = Sections(
    {
        SectionName('Ogl'):              oglProperties,
        SectionName('Diagram'):          diagramProperties,
        SectionName('Names'):            namePreferences,
        SectionName('SequenceDiagrams'): sequenceDiagramPreferences,
        SectionName('Associations'):     associationsPreferences,
        SectionName('Debug'):            debugPreferences,
    }
)


class OglPreferences(DynamicConfiguration, metaclass=SingletonV3):

    def __init__(self):
        self._logger: Logger = getLogger(__name__)

        super().__init__(baseFileName=f'{PREFERENCES_FILE_NAME}', moduleName=MODULE_NAME, sections=sections)
