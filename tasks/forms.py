from django import forms
from tasks.models import Employee, TaskDetails, Task


class StyledFormMixin:
    """Mixin to apply style to form fields."""
    default_classes = "form-control"

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            # DateField default widget is DateInput (TextInput subclass),
            # so SelectDateWidget must be set before the TextInput check.
            if isinstance(field, forms.DateField) and not isinstance(field, forms.DateTimeField):
                field.widget = forms.SelectDateWidget()

            # ManyToMany / MultipleChoiceField default widget is SelectMultiple.
            if isinstance(field, (forms.MultipleChoiceField, forms.ModelMultipleChoiceField)):
                choices = field.choices
                field.widget = forms.CheckboxSelectMultiple()
                field.widget.choices = choices

            # Model CharField(choices=...) becomes a ChoiceField with Select by default.
            elif isinstance(field, forms.ChoiceField) and not isinstance(
                field, (forms.MultipleChoiceField, forms.ModelChoiceField, forms.ModelMultipleChoiceField)
            ):
                choices = field.choices
                field.widget = forms.RadioSelect()
                field.widget.choices = choices

            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    "class": self.default_classes,
                    "placeholder": f"Enter {field.label.lower()} such as......",
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({
                    "class": "form-select",
                })
            elif isinstance(field.widget, (forms.CheckboxSelectMultiple, forms.RadioSelect)):
                field.widget.attrs.update({
                    "class": self.default_classes,
                })
            elif isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    "class": self.default_classes,
                    "placeholder": f"Enter {field.label.lower()} such as......",
                })


# Django Form for Task Creation
class TaskForm(forms.Form):
    title = forms.CharField(max_length=200)
    description = forms.CharField(widget=forms.Textarea, label="Description")
    due_date = forms.DateField(widget=forms.SelectDateWidget, label="Due Date")
    assign_to = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=[], label="Assign To")
    priority = forms.ChoiceField(widget=forms.RadioSelect, choices=[], label="Priority")

    def __init__(self, *args, **kwargs):
        employees = kwargs.pop('employees', [])

        super().__init__(*args, **kwargs)
        self.fields['assign_to'].choices = [(employee.id, employee.name) for employee in employees]
        self.fields['priority'].choices = TaskDetails.PRIORITY_OPTIONS


# Django ModelForm for Task Creation
class TaskModelForm(StyledFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'assign_to', 'status']
        # widgets = {
        #     'title': forms.TextInput(attrs={
        #         'class': 'form-control',
        #         'placeholder': 'e.g. Design database schema',
        #     }),
        #     'description': forms.Textarea(attrs={
        #         'class': 'form-control min-h-32',
        #         'rows': 5,
        #         'placeholder': 'Describe the task, expected outcome, and notes',
        #     }),
        #     'due_date': forms.SelectDateWidget(attrs={'class': 'form-select'}),
        #     'assign_to': forms.CheckboxSelectMultiple(),
        # }


class TaskDetailModelForm(StyledFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()

    class Meta:
        model = TaskDetails
        fields = ["priority", "note"]
        # task is set in the view after the Task is saved
