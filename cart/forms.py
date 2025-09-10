import django.forms


class ContactInfoForm(django.forms.Form):
    name = django.forms.CharField(
        label="Имя",
        max_length=100,
        widget=django.forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Иванов Иван Иванович",
            }
        ),
    )
    email = django.forms.EmailField(
        label="Email",
        widget=django.forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "example@danke.ru",
            }
        ),
    )
    phone_number = django.forms.CharField(
        label="Номер телефона",
        widget=django.forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "+7 (xxx) xxx-xx-xx",
            }
        ),
    )
    telegram = django.forms.CharField(
        label="Telegram",
        widget=django.forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "@danke",
            }
        ),
    )


class DeliveryInfoForm(django.forms.Form):
    country = django.forms.CharField(
        label="Страна",
        max_length=100,
        widget=django.forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Россия",
            }
        ),
    )
    address = django.forms.CharField(
        label="Полный адрес",
        widget=django.forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Москва, ул. Тверская, дом 3, квартира 1",
            }
        ),
    )
    index = django.forms.CharField(
        label="Индекс",
        widget=django.forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "xxxxxx",
            }
        ),
    )


class PromocodeForm(django.forms.Form):
    code = django.forms.CharField(
        max_length=50,
        widget=django.forms.TextInput(
            attrs={
                "placeholder": "Промокод",
                "class": "promocode-form",
            }
        ),
    )


__all__ = ()
