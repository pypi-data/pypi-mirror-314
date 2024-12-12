from enum import Enum


class ParameterType(Enum):
    TextField = "TextField"
    Cron = "Cron"
    Select = "Select"
    Autocomplete = "Autocomplete"
    CheckBox = "CheckBox"
    Switch = "Switch"
    SwitchWithParameter = "SwitchWithParameter"
    Code = "Code"
    FilterList = "FilterList"
    SelectByParameter = "SelectByParameter"
    Password = "Password"
    ListObject = "ListObject"
    ListString = "ListString"
    Group = "Group"
    TextFieldWithText = "TextFieldWithText"
    Accordion = "Accordion"
    SelectRoles = "SelectRoles"
    SelectBlocks = "SelectBlocks"
    Tree = "Tree"
    Tabs = "Tabs"
    FileField = "FileField"
    MappingData = "MappingData"
    Label = "Label"
    NumberField = "NumberField"
    DoubleField = "DoubleField"


class ConnectorDirection(Enum):
    input = "input"
    output = "output"
    both = "both"


class DataSendingStatus(Enum):
    success = "success"
    failed = "failed"
