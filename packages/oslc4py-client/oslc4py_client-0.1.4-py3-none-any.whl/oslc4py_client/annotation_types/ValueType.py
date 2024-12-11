from enum import Enum

class ValueType(Enum):
    BOOLEAN = "Boolean"
    DATE = "Date"
    DATETIME = "DateTime"
    DECIMAL = "Decimal"
    DOUBLE = "Double"
    FLOAT = "Float"
    INTEGER = "Integer"
    LOCALRESOURCE = "LocalResource"
    RESOURCE = "Resource"
    STRING = "String"
    XMLLITERAL = "XMLLiteral"