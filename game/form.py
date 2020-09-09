from django import forms


class GameForm(forms.Form):
    player_number = forms.IntegerField(label="Введите число", max_value=100, )

