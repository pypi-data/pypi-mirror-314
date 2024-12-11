from django import forms


class BaseBoundField(forms.BoundField):
    """
    The reason we're overriding get_context() instead of css_classes() is:
    Method css_classes() is called when rendering the "div.html" template, in
    the line:
    <div{% with classes=field.css_classes %}{% if classes %}
    class="{{ classes }}"{% endif %}{% endwith %}>
    We previously tried to use it to alter the classes contained in the
    widget's attrs, but it's not the place for that.
    """

    base_classes = ""
    no_error_classes = ""
    error_classes = ""

    def get_context(self):
        ctxt = super().get_context()
        widget = ctxt["field"].field.widget
        classes = widget.attrs.get("class", "").split()
        classes.append(self.base_classes)
        if self.errors:
            classes.append(self.error_classes)
        else:
            classes.append(self.no_error_classes)
        widget.attrs["class"] = " ".join(classes)
        return ctxt


class CharBoundField(BaseBoundField):
    base_classes = "text-sm border rounded-lg block w-full p-2.5"
    no_error_classes = """
        bg-gray-50 border-gray-300 text-gray-900
        focus:ring-primary-600 focus:border-primary-600
        dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400
        dark:text-white dark:focus:ring-primary-500
        dark:focus:border-primary-500
        """
    error_classes = """
        bg-red-50 border-red-500 text-red-900 placeholder-red-700
        focus:ring-red-500 focus:border-red-500
        dark:bg-gray-700 dark:text-red-500 dark:placeholder-red-500
        dark:border-red-500
        """


class BooleanBoundField(BaseBoundField):
    base_classes = "w-4 h-4 border rounded text-primary-500"
    no_error_classes = (
        "border-gray-300 bg-gray-50 focus:ring-3 focus:ring-primary-300 "
        "dark:bg-gray-700 dark:border-gray-600 dark:focus:ring-primary-600 "
        "dark:ring-offset-gray-800"
    )
    error_classes = (
        "bg-red-50 border-red-500 text-red-700 placeholder-red-700 "
        "focus:ring-red-500focus:border-red-500 dark:bg-gray-700  "
        "dark:text-red-500 dark:placeholder-red-500 dark:border-red-500"
    )


class FileBoundField(BaseBoundField):
    base_classes = "text-sm border rounded-lg block w-full px-2.5"
    no_error_classes = "bg-gray-50 border-gray-300 text-gray-900 " "focus:ring-primary-600 focus:border-primary-600"
    error_classes = (
        "bg-red-50 border-red-500 text-red-900 placeholder-red-700 " "focus:ring-red-500 focus:border-red-500"
    )


class TimeBoundField(BaseBoundField):
    """
    When using this field type, you also have to use the widget
    flowbite_classes.widgets.FlowBiteTimeInput in your form.
    """

    base_classes = "text-sm border rounded-lg block w-full p-2.5"
    no_error_classes = "bg-gray-50 border-gray-300 text-gray-900 " "focus:ring-primary-600 focus:border-primary-600"
    error_classes = (
        "bg-red-50 border-red-500 text-red-900 placeholder-red-700 " "focus:ring-red-500 focus:border-red-500"
    )


class DateBoundField(BaseBoundField):
    """
    When using this field type, you also have to use the widget
    flowbite_classes.widgets.FlowBiteDateInput in your form.
    """

    base_classes = "text-sm border rounded-lg block w-full p-2.5"
    no_error_classes = "bg-gray-50 border-gray-300 text-gray-900 focus:ring-primary-600 " "focus:border-primary-600"
    error_classes = (
        "bg-red-50 border-red-500 text-red-900 placeholder-red-700 " "focus:ring-red-500 focus:border-red-500"
    )
