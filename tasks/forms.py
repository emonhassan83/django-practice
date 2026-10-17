from django import forms
from tasks.models import Employee, TaskDetails

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