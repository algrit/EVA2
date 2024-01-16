from django import forms
from django.db.models import Q

from education.models import CourseSubscription


class CourseSubscribeForm(forms.ModelForm):
    class Meta:
        model = CourseSubscription
        fields = ['user', 'course']

    def clean(self):
        cleaned_data = super(CourseSubscribeForm, self).clean()
        user_id = cleaned_data.get('user').id
        course_id = cleaned_data.get('course').id
        if CourseSubscription.objects.filter(
                Q(user_id=user_id) &
                Q(course_id=course_id) &
                Q(active=True)).exists():
            raise forms.ValidationError('Subscription is not allowed! This user is already subscribed to this course.')