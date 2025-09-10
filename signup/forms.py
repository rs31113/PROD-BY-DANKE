from django import forms
import signup.models


class SignupForm(forms.ModelForm):
    consent = forms.BooleanField(
        label='Я согласен с <a href="/privacy-policy/" target="_blank">политикой конфиденциальности</a>.',
        required=True,
        widget=forms.CheckboxInput(attrs={'id': 'consent-checkbox'})
    )

    class Meta:
        model = signup.models.Subscriber
        fields = ['email', 'consent']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email', 'class': 'form-control'}),
        }

    def clean_consent(self):
        consent = self.cleaned_data.get('consent')
        if not consent:
            raise forms.ValidationError('Вы должны согласиться с политикой конфиденциальности.')
        return consent


__all__ = ()
