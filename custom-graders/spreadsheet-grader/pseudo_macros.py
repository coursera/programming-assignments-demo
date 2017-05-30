import re

def parse_simple_formula(formula):
    MACRO_FORMULA_REGEX = "='?(\w+)'?\*?\((\$(\w+)\.)?([A-Z]+[0-9]+)\)"
    # Match expressions of the following form:
    #   =MacroName(A1)              => MacroName, None, A1
    #   =MacroName($Sheet1.A1)      => MacroName, Sheet1, A1
    #   ='MacroName'(A1)            => MacroName, None, A1
    #   ='MacroName'*(A1)           => MacroName, None, A1
    match = re.match(MACRO_FORMULA_REGEX, formula)
    if match:
        function_name = match.group(1)
        sheet_name = match.group(3)
        cell_name = match.group(4)
        return (function_name, sheet_name, cell_name)
    else:
        return (None, None, None)

PRIMITIVE_CELL_ATTRS = ['AbsoluteName', 'ArrayFormula', 'AsianVerticalMode',
'CellBackColor', 'CellStyle', 'CharColor', 'CharContoured', 'CharCrossedOut',
'CharEmphasis', 'CharFont', 'CharFontCharSet', 'CharFontCharSetAsian',
'CharFontCharSetComplex', 'CharFontFamily', 'CharFontFamilyAsian',
'CharFontFamilyComplex', 'CharFontName', 'CharFontNameAsian',
'CharFontNameComplex', 'CharFontPitch', 'CharFontPitchAsian',
'CharFontPitchComplex', 'CharFontStyleName', 'CharFontStyleNameAsian',
'CharFontStyleNameComplex', 'CharHeight', 'CharHeightAsian',
'CharHeightComplex', 'CharOverline', 'CharOverlineColor',
'CharOverlineHasColor', 'CharRelief', 'CharShadowed', 'CharStrikeout',
'CharUnderline', 'CharUnderlineColor', 'CharUnderlineHasColor',
'CharWeight', 'CharWeightAsian', 'CharWeightComplex', 'CharWordMode',
'ChartColumnAsLabel', 'ChartRowAsLabel', 'Error', 'Formula', 'FormulaLocal',
'HoriJustifyMethod', 'Hyperlink', 'ImplementationName',
'IsCellBackgroundTransparent', 'IsMerged', 'IsTextWrapped', 'NotANumber',
'NumberFormat', 'ParaAdjust', 'ParaBottomMargin', 'ParaIndent',
'ParaIsCharacterDistance', 'ParaIsForbiddenRules', 'ParaIsHangingPunctuation',
'ParaIsHyphenation', 'ParaLastLineAdjust', 'ParaLeftMargin', 'ParaRightMargin',
'ParaTopMargin', 'RotateAngle', 'RotateReference', 'ShrinkToFit', 'String',
'Value', 'VertJustify', 'VertJustifyMethod', 'WritingMode']

PRIMITIVE_CELL_ATTRS_MAP = {p.lower(): p for p in PRIMITIVE_CELL_ATTRS}

def evaluate_cell_property_formula(window, sheet, property_formula):
    (function_name, sheet_name, cell_name) = parse_simple_formula(property_formula)
    if sheet_name:
        sheet = window.get_sheet_by_name(sheet_name)
    if cell_name:
        cell = sheet.get_cell_range_by_name(cell_name)
        # openoffice sometimes casts names to lowercase
        attrname = PRIMITIVE_CELL_ATTRS_MAP.get(function_name.lower())
        if attrname:
            return cell.__getattr__(attrname)

def evaluate_macro(window, sheet, formula):
    # TODO amory: Add support for additional macros
    property_value = evaluate_cell_property_formula(window, sheet, formula)
    if property_value:
        return property_value
