class ActionParameter:
    """
    Generic class used to specify the parameters for an action.
    Combined with templates, this allow to dynamically generate appropriate forms for the actions.
    """
    type = 'null'
    def __init__(self, name: str, display_name: str, hint: str = None):
        self.name = name
        self.display_name = display_name
        self.hint = hint

    def value_is_valid(self, value):
        return True

    def get_type(self):
        return ActionParameter.type

class StringParameter(ActionParameter):
    type = "str"
    def __init__(self, name, display_name, hint = None, possible_values: dict = None):
        ActionParameter.__init__(self, name, display_name, hint)
        self.possible_values = possible_values;

    def value_is_valid(self, value):
        return isinstance(value, str) and (self.possible_values is None or value in self.possible_values)

    def get_type(self):
        return StringParameter.type

class IntegerParameter(ActionParameter):
    type = 'int'
    def __init__(self, name, display_name, hint=None, minValue=None, maxValue=None):
        ActionParameter.__init__(self, name, display_name, hint)
        self.minValue = minValue
        self.maxValue = maxValue

    def value_is_valid(self, value):
        return isinstance(value, int) and (max is None or value <= max) and (min is None or value >= min)
    
    def get_type(self):
        return IntegerParameter.type

class BooleanParameter(ActionParameter):
    type = 'bool'
    def __init__(self, name, display_name, hint = None):
        ActionParameter.__init__(self, name, display_name, hint)

    def value_is_valid(self, value):
        return isinstance(value, bool) or (isinstance(value, int) and (value == 0 or value == 1))
    
    def get_type(self):
        return BooleanParameter.type