from django import forms

class ContactForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'placeholder': 'Email', 'class': 'form-control','required': True}
        ))

    name = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Име', 'class': 'form-control','required': True}
        ))

    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'placeholder': 'Вашето съобщение', 'rows': 5, 'class': 'form-control','required': True}
        ))