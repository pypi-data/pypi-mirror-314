from django import forms

import flowbite_classes.forms


def charfield_get_bound_field(self, form, field_name):
    return flowbite_classes.forms.CharBoundField(form, self, field_name)


forms.CharField.get_bound_field = charfield_get_bound_field
forms.EmailField.get_bound_field = charfield_get_bound_field
forms.IntegerField.get_bound_field = charfield_get_bound_field
forms.ChoiceField.get_bound_field = charfield_get_bound_field
forms.MultipleChoiceField.get_bound_field = charfield_get_bound_field


def boolean_get_bound_field(self, form, field_name):
    return flowbite_classes.forms.BooleanBoundField(form, self, field_name)


forms.BooleanField.get_bound_field = boolean_get_bound_field


def file_get_bound_field(self, form, field_name):
    return flowbite_classes.forms.FileBoundField(form, self, field_name)


forms.FileField.get_bound_field = file_get_bound_field


def time_get_bound_field(self, form, field_name):
    return flowbite_classes.forms.TimeBoundField(form, self, field_name)


forms.TimeField.get_bound_field = time_get_bound_field


def date_get_bound_field(self, form, field_name):
    return flowbite_classes.forms.DateBoundField(form, self, field_name)


forms.DateField.get_bound_field = date_get_bound_field
