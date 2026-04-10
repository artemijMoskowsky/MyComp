from django.forms import ModelForm, RadioSelect, TextInput
from .models import Order

class OrderForm(ModelForm):
    class Meta:
        model = Order
        exclude = ["log", "user", "ordered_at"]
        widgets = {
            'type_of_delivery': RadioSelect,
            'type_of_payment': RadioSelect,
            'phone_number': TextInput(attrs={
                'type': 'tel',
                'class': 'phone-mask-input',
                'placeholder': '+380...'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["fullname"].label = "Введіть ваше повне ім’я"
        self.fields["phone_number"].label = "Введіть номер телефону"
        self.fields["type_of_delivery"].label = "Виберіть тип доставки"
        self.fields["type_of_payment"].label = "Виберіть тип оплати"
        self.fields["city"].label = "Виберіть місто"
        self.fields["postoffice"].label = "Виберіть відділення"
