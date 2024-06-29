from django import forms
from courses.models import Course

class CourseEnrollForm(forms.Form):
    course = forms.ModelChoiceField(
        queryset=Course.objects.none(),
        widget=forms.HiddenInput
    )

    def __init__(self, *args, **kwargs):
        initial_course = kwargs.pop('initial', None)
        super().__init__(*args, **kwargs)
        if initial_course:
            self.fields['course'].initial = initial_course['course']
        self.fields['course'].queryset = Course.objects.all()
