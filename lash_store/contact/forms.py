from django import forms

class ContactForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'placeholder': 'Email', }
        ))

    name = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Име', }
        ))

    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'placeholder': 'Вашето съобщение', }
        ))