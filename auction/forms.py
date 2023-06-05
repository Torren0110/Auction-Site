from django import forms
from .models import Item, ItemPhoto
from datetime import datetime
from django.utils import timezone
from django.forms import inlineformset_factory

class ItemEnlistForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(
        attrs={'type' : 'date'}
    ))
    start_clock = forms.TimeField(
        label='Start Time',
        widget=forms.TimeInput(
            attrs={'type' : 'time'}
        )
    )

    end_date = forms.DateField(widget=forms.DateInput(
        attrs={'type' : 'date'}
    ))
    end_clock = forms.TimeField(
        label='End Time',
        widget=forms.TimeInput(
            attrs={'type' : 'time'}
        )
    )

    def clean(self):
        super().clean()

        if self.cleaned_data['start_date'] and self.cleaned_data['start_clock'] and self.cleaned_data['end_date'] and self.cleaned_data['end_clock']:
            st = timezone.make_aware(
            timezone.datetime.combine(self.cleaned_data['start_date'], self.cleaned_data['start_clock']),
            timezone.get_current_timezone()
            )

            et = timezone.make_aware(
                timezone.datetime.combine(self.cleaned_data['end_date'], self.cleaned_data['end_clock']),
                timezone.get_current_timezone()
            )
            if st <= timezone.now():
                raise forms.ValidationError('Start time should be greater than current time')

            if st >= et:
                raise forms.ValidationError("End Time should be Greater than Start time")


    

    class Meta:
        model = Item
        fields = ['name', 'description', 'start_date', 'start_clock', 'end_date', 'end_clock', 'initial_bid']

    def save(self, user, commit = True):
        instance = super().save(commit=False)
        st = timezone.make_aware(
            timezone.datetime.combine(self.cleaned_data['start_date'], self.cleaned_data['start_clock']),
            timezone.get_current_timezone()
        )

        et = timezone.make_aware(
            timezone.datetime.combine(self.cleaned_data['end_date'], self.cleaned_data['end_clock']),
            timezone.get_current_timezone()
        )
        instance.start_time = st
        instance.end_time = et
        instance.user = user

        if commit:
            instance.save()

        return instance
    
class ItemImageForm(forms.ModelForm):
    
    class Meta:
        fields = ['photo']
        labels = {
            'photo' : 'Upload Image'
        }

ImageFormSet = inlineformset_factory(
    Item,
    ItemPhoto,
    form=ItemImageForm,
    fields=('photo',),
    extra=5,
    can_delete=False
)

