import random

from django.shortcuts import render

from game.models import Player, Game


def show_home(request):
    return render(
        request,
        'home.html',
    )
