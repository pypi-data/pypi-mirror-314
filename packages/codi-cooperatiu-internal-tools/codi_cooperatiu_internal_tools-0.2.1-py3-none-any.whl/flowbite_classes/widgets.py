from django import forms


class FlowBiteTimeInput(forms.TimeInput):
    input_type = "time"


class FlowBiteDateTimeInput(forms.DateTimeInput):
    input_type = "datetime-local"

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%dT%H:%M"
        super().__init__(**kwargs)


class FlowBiteDateInput(forms.DateTimeInput):
    input_type = "date"

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%d"
        super().__init__(**kwargs)


class FlowBiteNumericInput(forms.NumberInput):
    input_type = "text"

    def __init__(self, attrs=None):
        attrs = attrs or {}
        if attrs is None:
            attrs = {}
        attrs.update(
            {
                "data-input-counter": "",
            }
        )
        super().__init__(attrs)


class FlowBiteNumericIncrementalInput(forms.NumberInput):
    template_name = "flowbite_classes/widgets/numeric_incremental.html"
    input_type = "text"

    def __init__(self, attrs=None):
        attrs = attrs or {}
        if attrs is None:
            attrs = {}
        attrs.update(
            {
                "data-input-counter": "",
            }
        )
        super().__init__(attrs)
