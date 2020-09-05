from django import forms


class GameForm(forms.Form):
    hidden_number = forms.IntegerField(label="Введите число", max_value=100, )

