from django import forms
from django.core.validators import RegexValidator

from lash_store.orders.models import Order, ShippingAddress

class CheckoutForm(forms.ModelForm):
    MAX_POSTAL_CODE_LENGTH = 4
    MIN_POSTAL_CODE_LENGTH = 4

    name = forms.CharField(
        max_length=ShippingAddress.MAX_NAME_LENGTH,
        widget=forms.TextInput(
            attrs={
                'placeholder': '',
                'class': 'floating-textarea',
                'autocomplete': 'name',
            }
        ),
    )

    phone_number = forms.CharField(
        max_length=ShippingAddress.MAX_PHONE_NUMBER_LENGTH,
        validators=[RegexValidator(
            regex=r"^((?:\+359|0)8[7-9]\d{7}|(?:\+359|0)[2-9]\d{6,8})$",
            message="Моля въведете валиден телефоне номер с формат 0888123456"
        )],
        widget = forms.NumberInput(
            attrs={
                'placeholder': '',
                'class': 'floating-textarea',
                'autocomplete': 'tel',
            }
        ),
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'placeholder': '',
                'class': 'floating-textarea',
                'autocomplete': 'email',
            }
        ),
    )

    address = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'placeholder': '',
                'class': 'floating-textarea',
                'rows': 5,
                'autocomplete': 'street-address',
            }
        ),
    )

    city = forms.CharField(
        max_length=ShippingAddress.MAX_CITY_LENGTH,
        widget=forms.TextInput(
            attrs={
                'placeholder': '',
                'class': 'floating-textarea',
                'autocomplete': 'address-level2',
            }
        ),
    )

    postal_code = forms.CharField(
        max_length=MAX_POSTAL_CODE_LENGTH,
        min_length=MIN_POSTAL_CODE_LENGTH,
        validators=[RegexValidator(r'^\d{4}$',"Въведете валиден пощенски код от 4 цифри.")],
        widget=forms.TextInput(
            attrs={
                'placeholder': '',
                'class': 'floating-textarea',
                'autocomplete': 'postal-code',
            }
        ),
    )

    payment_method = forms.ChoiceField(
        choices=ShippingAddress.PAYMENT_CHOICES,
        widget=forms.RadioSelect,
        initial='pay_on_delivery'
    )

    note = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'placeholder': '',
                'class': 'floating-textarea',
                'rows': 5,
            }
        ),
    )

    class Meta:
        model = Order
        fields = []

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self._prepopulate_fields()

    def _prepopulate_fields(self):
        last_order = ShippingAddress.objects.filter(customer=self.user).order_by('-created_at').first()
        if last_order:
            self.fields['name'].initial = last_order.name
            self.fields['phone_number'].initial = last_order.phone_number
            self.fields['email'].initial = last_order.email
            self.fields['address'].initial = last_order.address
            self.fields['city'].initial = last_order.city
            self.fields['postal_code'].initial = last_order.postal_code
        else:
            self.fields['phone_number'].initial = self.user.profile.phone_number
            self.fields['email'].initial = self.user.email

    def clean(self):
        cleaned_data = super().clean()

        cart = getattr(self.user, 'cart', None)
        if not cart:
            raise forms.ValidationError("Количката ви е празна или не е създадена.")

        cart_items = cart.items.all()
        cleaned_data['total_price'] = sum(item.product.price * item.quantity for item in cart_items)
        cleaned_data['status'] = 'Pending'
        return cleaned_data

    def save(self, commit=True):
        order = super().save(commit=False)
        order.note = self.cleaned_data.get('note')
        order.customer = self.user
        order.total_price = self.cleaned_data['total_price']
        order.status = self.cleaned_data['status']

        if commit:
            order.save()

            ShippingAddress.objects.create(
                name=self.cleaned_data['name'],
                phone_number=self.cleaned_data['phone_number'],
                email=self.cleaned_data['email'],
                customer=self.user,
                order=order,
                address=self.cleaned_data['address'],
                city=self.cleaned_data['city'],
                postal_code=self.cleaned_data['postal_code'],
            )

            return order
