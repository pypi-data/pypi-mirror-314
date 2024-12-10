from speedtab.formats import Color, Number, Dollar, Percent, Date, Time, DateTime, Scientific, Text


class AxisPosition:
    LEFT_AXIS = 'LEFT_AXIS'
    RIGHT_AXIS = 'RIGHT_AXIS'
    BOTTOM_AXIS = 'BOTTOM_AXIS'


class BooleanConditionTypes:
    NUMBER_GREATER = 'NUMBER_GREATER'
    NUMBER_GREATER_THAN_EQ = 'NUMBER_GREATER_THAN_EQ'
    NUMBER_LESS = 'NUMBER_LESS'
    NUMBER_LESS_THAN_EQ = 'NUMBER_LESS_THAN_EQ'
    NUMBER_EQ = 'NUMBER_EQ'
    NUMBER_NOT_EQ = 'NUMBER_NOT_EQ'
    NUMBER_BETWEEN = 'NUMBER_BETWEEN'
    NUMBER_NOT_BETWEEN = 'NUMBER_NOT_BETWEEN'
    TEXT_CONTAINS = 'TEXT_CONTAINS'
    TEXT_NOT_CONTAINS = 'TEXT_NOT_CONTAINS'
    TEXT_STARTS_WITH = 'TEXT_STARTS_WITH'
    TEXT_ENDS_WITH = 'TEXT_ENDS_WITH'
    TEXT_EQ = 'TEXT_EQ'
    TEXT_IS_EMAIL = 'TEXT_IS_EMAIL'
    TEXT_IS_URL = 'TEXT_IS_URL'
    DATE_EQ = 'DATE_EQ'
    DATE_BEFORE = 'DATE_BEFORE'
    DATE_AFTER = 'DATE_AFTER'
    DATE_ON_OR_BEFORE = 'DATE_ON_OR_BEFORE'
    DATE_ON_OR_AFTER = 'DATE_ON_OR_AFTER'
    DATE_BETWEEN = 'DATE_BETWEEN'
    DATE_NOT_BETWEEN = 'DATE_NOT_BETWEEN'
    DATE_IS_VALID = 'DATE_IS_VALID'
    ONE_OF_RANGE = 'ONE_OF_RANGE'
    ONE_OF_LIST = 'ONE_OF_LIST'
    BLANK = 'BLANK'
    IS_EMPTY = 'BLANK'
    NOT_BLANK = 'NOT_BLANK'
    IS_NOT_EMPTY = 'NOT_BLANK'
    CUSTOM_FORMULA = 'CUSTOM_FORMULA'
    BOOLEAN = 'BOOLEAN'
    TEXT_NOT_EQ = 'TEXT_NOT_EQ'
    DATE_NOT_EQ = 'DATE_NOT_EQ'


class BorderSides:
    ALL = ('top', 'bottom', 'left', 'right', 'innerHorizontal', 'innerVertical')
    INNER = ('innerHorizontal', 'innerVertical')
    OUTER = ('top', 'bottom', 'left', 'right')
    TOP = ('top',)
    BOTTOM = ('bottom',)
    LEFT = ('left',)
    RIGHT = ('right',)
    HORIZONTAL = ('innerHorizontal',)
    VERTICAL = ('innerVertical',)

class BorderStyle:
    SOLID = 'SOLID'
    SOLID_MEDIUM = 'SOLID_MEDIUM'
    SOLID_THICK = 'SOLID_THICK'
    DOTTED = 'DOTTED'
    DASHED = 'DASHED'
    DOUBLE = 'DOUBLE'


class ChartType:
    BAR = 'BAR'
    LINE = 'LINE'
    AREA = 'AREA'
    COLUMN = 'COLUMN'
    SCATTER = 'SCATTER'


class ClearSpecific:
    NONE = None

    NUMBER_FORMAT = 'userEnteredFormat(numberFormat)'
    BACKGROUND_COLOR = 'userEnteredFormat(backgroundColor)'
    BACKGROUND_COLOR_STYLE = 'userEnteredFormat(backgroundColorStyle)'
    ALL_BORDERS = 'userEnteredFormat(borders)'
    TOP_BORDER = 'userEnteredFormat(borders.top)'
    BOTTOM_BORDER = 'userEnteredFormat(borders.bottom)'
    LEFT_BORDER = 'userEnteredFormat(borders.left)'
    RIGHT_BORDER = 'userEnteredFormat(borders.right)'
    PADDING = 'userEnteredFormat(padding)'
    HORIZONTAL_ALIGNMENT = 'userEnteredFormat(horizontalAlignment)'
    VERTICAL_ALIGNMENT = 'userEnteredFormat(verticalAlignment)'
    WRAP_STRATEGY = 'userEnteredFormat(wrapStrategy)'
    TEXT_DIRECTION = 'userEnteredFormat(textDirection)'
    TEXT_FORMAT = 'userEnteredFormat(textFormat)'
    HYPERLINK_DISPLAY_TYPE = 'userEnteredFormat(hyperlinkDisplayType)'
    TEXT_ROTATION = 'userEnteredFormat(textRotation)'

    NUMBER_VALUE = 'userEnteredValue(numberValue)'
    STRING_VALUE = 'userEnteredValue(stringValue)'
    BOOL_VALUE = 'userEnteredValue(boolValue)'
    FORMULA_VALUE = 'userEnteredValue(formulaValue)'
    ERROR_VALUE = 'userEnteredValue(errorValue)'
class CustomFormats:
    DATE = Date
    DATETIME = DateTime
    DECIMAL = Number
    DECIMAL_PERCENT = Percent
    DOLLAR = Dollar
    NUMBER = Number
    PERCENT = Percent
    SCIENTIFIC = Scientific
    TEXT = Text
    TIME = Time

class DefaultColors:
    BLACK = Color('#000000')
    DARK_GREY4 = Color('#434343')
    DARK_GREY3 = Color('#666666')
    DARK_GREY2 = Color('#999999')
    DARK_GREY1 = Color('#b7b7b7')
    GREY = Color('#cccccc')
    LIGHT_GREY1 = Color('#d9d9d9')
    LIGHT_GREY2 = Color('#efefef')
    LIGHT_GREY3 = Color('#f3f3f3')
    WHITE = Color('#ffffff')
    RED_BERRY = Color('#980000')
    LIGHT_RED_BERRY3 = Color('#e6b8af')
    LIGHT_RED_BERRY2 = Color('#dd7e6b')
    LIGHT_RED_BERRY1 = Color('#cc4125')
    DARK_RED_BERRY1 = Color('#a61c00')
    DARK_RED_BERRY2 = Color('#85200c')
    DARK_RED_BERRY3 = Color('#5b0f00')
    RED = Color('#ff0000')
    LIGHT_RED3 = Color('#f4cccc')
    LIGHT_RED2 = Color('#ea9999')
    LIGHT_RED1 = Color('#e06666')
    DARK_RED1 = Color('#cc0000')
    DARK_RED2 = Color('#990000')
    DARK_RED3 = Color('#660000')
    ORANGE = Color('#ff9900')
    LIGHT_ORANGE3 = Color('#fce5cd')
    LIGHT_ORANGE2 = Color('#f9cb9c')
    LIGHT_ORANGE1 = Color('#f6b26b')
    DARK_ORANGE1 = Color('#e69138')
    DARK_ORANGE2 = Color('#b45f06')
    DARK_ORANGE3 = Color('#783f04')
    YELLOW = Color('#ffff00')
    LIGHT_YELLOW3 = Color('#fff2cc')
    LIGHT_YELLOW2 = Color('#ffe599')
    LIGHT_YELLOW1 = Color('#ffd966')
    DARK_YELLOW1 = Color('#f1c232')
    DARK_YELLOW2 = Color('#bf9000')
    DARK_YELLOW3 = Color('#7f6000')
    GREEN = Color('#00ff00')
    LIGHT_GREEN3 = Color('#d9ead3')
    LIGHT_GREEN2 = Color('#b6d7a8')
    LIGHT_GREEN1 = Color('#93c47d')
    DARK_GREEN1 = Color('#6aa84f')
    DARK_GREEN2 = Color('#38761d')
    DARK_GREEN3 = Color('#274e13')
    CYAN = Color('#00ffff')
    LIGHT_CYAN3 = Color('#d0e0e3')
    LIGHT_CYAN2 = Color('#a2c4c9')
    LIGHT_CYAN1 = Color('#76a5af')
    DARK_CYAN1 = Color('#45818e')
    DARK_CYAN2 = Color('#134f5c')
    DARK_CYAN3 = Color('#0c343d')
    CORNFLOWER_BLUE = Color('#4a86e8')
    LIGHT_CORNFLOWER_BLUE3 = Color('#c9daf8')
    LIGHT_CORNFLOWER_BLUE2 = Color('#a4c2f4')
    LIGHT_CORNFLOWER_BLUE1 = Color('#6d9eeb')
    DARK_CORNFLOWER_BLUE1 = Color('#3c78d8')
    DARK_CORNFLOWER_BLUE2 = Color('#1155cc')
    DARK_CORNFLOWER_BLUE3 = Color('#1c4587')
    BLUE = Color('#0000ff')
    LIGHT_BLUE3 = Color('#cfe2f3')
    LIGHT_BLUE2 = Color('#9fc5e8')
    LIGHT_BLUE1 = Color('#6fa8dc')
    DARK_BLUE1 = Color('#3d85c6')
    DARK_BLUE2 = Color('#0b5394')
    DARK_BLUE3 = Color('#073763')
    PURPLE = Color('#9900ff')
    LIGHT_PURPLE3 = Color('#d9d2e9')
    LIGHT_PURPLE2 = Color('#b4a7d6')
    LIGHT_PURPLE1 = Color('#8e7cc3')
    DARK_PURPLE1 = Color('#674ea7')
    DARK_PURPLE2 = Color('#351c75')
    DARK_PURPLE3 = Color('#20124d')
    MAGENTA = Color('#ff00ff')
    LIGHT_MAGENTA3 = Color('#ead1dc')
    LIGHT_MAGENTA2 = Color('#d5a6bd')
    LIGHT_MAGENTA1 = Color('#c27ba0')
    DARK_MAGENTA1 = Color('#a64d79')
    DARK_MAGENTA2 = Color('#741b47')
    DARK_MAGENTA3 = Color('#4c1130')


class HorizontalAlignment:
    LEFT = 'LEFT'
    CENTER = 'CENTER'
    RIGHT = 'RIGHT'


class LegendPosition:
    BOTTOM_LEGEND = 'BOTTOM_LEGEND'
    LEFT_LEGEND = 'LEFT_LEGEND'
    RIGHT_LEGEND = 'RIGHT_LEGEND'
    TOP_LEGEND = 'TOP_LEGEND'
    NO_LEGEND = 'NO_LEGEND'


class MergeType:
    MERGE_ALL = 'MERGE_ALL'
    MERGE_COLUMNS = 'MERGE_COLUMNS'
    MERGE_ROWS = 'MERGE_ROWS'


class ReadyFormats:
    DATE = Date()
    DATETIME = DateTime()
    DECIMAL = Number('0.00')
    DECIMAL_PERCENT = Percent('0.00%')
    DOLLAR = Dollar()
    NUMBER = Number()
    PRETTY_DOLLAR = Dollar('_($* #,##0.00_);_($* -#,##0.00;_($* "-"??_);_(@_)')
    PERCENT = Percent()
    SCIENTIFIC = Scientific()
    TEXT = Text()
    TIME = Time()


class ShareRole:
    VIEWER = 'reader'
    COMMENTER = 'commenter'
    EDITOR = 'writer'



class StackedType:
    STACKED = 'STACKED'
    PERCENT_STACKED = 'PERCENT_STACKED'
    NONE = None


class VerticalAlignment:
    TOP = 'TOP'
    MIDDLE = 'MIDDLE'
    BOTTOM = 'BOTTOM'


class WrapStrategy:
    OVERFLOW_CELL = 'OVERFLOW_CELL'
    LEGACY_WRAP = 'LEGACY_WRAP'
    CLIP = 'CLIP'
    WRAP = 'WRAP'


