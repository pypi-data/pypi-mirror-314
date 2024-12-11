from importlib import reload

from django import forms
from django.apps import apps
from django.template import Context, Template
from django.test.utils import override_settings

import flowbite_classes
from flowbite_classes import widgets
from flowbite_classes.forms import BooleanBoundField, CharBoundField, DateBoundField, FileBoundField, TimeBoundField


@override_settings(CODI_COOP_ENABLE_MONKEY_PATCH=False)
def test_monkey_patch_not_applied_without_config(mocker):
    # Fer mock del mètode que aplica el monkey patch
    mock_apply_patch = mocker.patch("flowbite_classes.apps.FlowbiteClassesConfig.apply_monkey_patch")

    # Recarregar el mòdul apps.py perquè el codi de ready() s'executi de nou
    reload(flowbite_classes)  # Recarregar el mòdul que conté la classe

    # Forçar la crida a ready() novament
    apps.get_app_config("flowbite_classes").ready()

    # Verificar que la funció apply_monkey_patch no s'ha cridat
    mock_apply_patch.assert_not_called()


@override_settings(CODI_COOP_ENABLE_MONKEY_PATCH=True)
def test_monkey_patch_applied_with_config(mocker):
    # Fer mock del mètode que aplica el monkey patch
    mock_apply_patch = mocker.patch("flowbite_classes.apps.FlowbiteClassesConfig.apply_monkey_patch")

    # Recarregar el mòdul apps.py perquè el codi de ready() s'executi de nou
    reload(flowbite_classes)  # Recarregar el mòdul que conté la classe

    # Forçar la crida a ready() novament
    apps.get_app_config("flowbite_classes").ready()

    # Verificar que la funció apply_monkey_patch s'ha cridat una vegada
    mock_apply_patch.assert_called_once()


class CharForm(forms.Form):
    """
    Example form that uses forms.CharField.
    """

    char_field = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "autofocus": True,
                "placeholder": "Text 1",
                "autocomplete": "text",
            }
        ),
        help_text="Help for char_field",
    )


class BooleanForm(forms.Form):
    boolean_field = forms.BooleanField(widget=forms.CheckboxInput, help_text="Help boolean_field")


class TimeForm(forms.Form):
    time_field = forms.TimeField(widget=widgets.FlowBiteTimeInput, help_text="Help time_field")


class DateForm(forms.Form):
    date_field = forms.DateField(widget=widgets.FlowBiteDateInput, help_text="Help date_field")


class FileForm(forms.Form):
    file_field = forms.FileField()


class NumericForm(forms.Form):
    number_field = forms.IntegerField(widget=widgets.FlowBiteNumericInput, help_text="Help number_field")


def test_monkey_patching_applied_to_charfield():
    """
    Verifies that the monkey patching applied to forms.CharField works correctly.
    """
    template = Template(
        """
        {{ form }}
        """
    )
    form_instance = CharForm()
    html = template.render(Context({"form": form_instance}))

    # Verify that only one input is rendered
    assert html.count("<input") == 1

    # Verify that the base classes have been applied
    assert CharBoundField.base_classes in html, "Base classes were not applied correctly."

    # Verify that the no-error classes have been applied
    assert CharBoundField.no_error_classes in html, "No-error classes were not applied correctly."


def test_monkey_patching_applied_to_booleanfield():
    """
    Verifies that the monkey patching applied to forms.CharField works correctly.
    """
    template = Template(
        """
        {{ form }}
        """
    )
    form_instance = BooleanForm()
    html = template.render(Context({"form": form_instance}))

    # Verify that only one input is rendered
    assert html.count("<input") == 1

    # Verify that the base classes have been applied
    assert BooleanBoundField.base_classes in html, "Base classes were not applied correctly."

    # Verify that the no-error classes have been applied
    assert BooleanBoundField.no_error_classes in html, "No-error classes were not applied correctly."


def test_monkey_patching_applied_to_timefield():
    """
    Verifies that the monkey patching applied to forms.CharField works correctly.
    """
    template = Template(
        """
        {{ form }}
        """
    )
    form_instance = TimeForm()
    html = template.render(Context({"form": form_instance}))

    # Verify that only one input is rendered
    assert html.count("<input") == 1

    # Verify that the base classes have been applied
    assert TimeBoundField.base_classes in html, "Base classes were not applied correctly."

    # Verify that the no-error classes have been applied
    assert TimeBoundField.no_error_classes in html, "No-error classes were not applied correctly."


def test_monkey_patching_applied_to_datefield():
    """
    Verifies that the monkey patching applied to forms.CharField works correctly.
    """
    template = Template(
        """
        {{ form }}
        """
    )
    form_instance = DateForm()
    html = template.render(Context({"form": form_instance}))

    # Verify that only one input is rendered
    assert html.count("<input") == 1

    # Verify that the base classes have been applied
    assert DateBoundField.base_classes in html, "Base classes were not applied correctly."

    # Verify that the no-error classes have been applied
    assert DateBoundField.no_error_classes in html, "No-error classes were not applied correctly."


def test_monkey_patching_applied_to_filefield():
    """
    Verifies that the monkey patching applied to forms.CharField works correctly.
    """
    template = Template(
        """
        {{ form }}
        """
    )
    form_instance = FileForm()
    html = template.render(Context({"form": form_instance}))

    # Verify that only one input is rendered
    assert html.count("<input") == 1

    # Verify that the base classes have been applied
    assert FileBoundField.base_classes in html, "Base classes were not applied correctly."

    # Verify that the no-error classes have been applied
    assert FileBoundField.no_error_classes in html, "No-error classes were not applied correctly."


def test_input_properties_in_number_field():
    """
    Verifies that the monkey patching applied to forms.CharField works correctly.
    """
    template = Template(
        """
        {{ form }}
        """
    )
    form_instance = NumericForm()
    html = template.render(Context({"form": form_instance}))

    # Verify that only one input is rendered
    assert html.count("<input") == 1

    # Verify that the field type is text
    assert html.count('type="text"') == 1

    # Verify that the property data-input-counter is present
    assert html.count("data-input-counter") == 1
