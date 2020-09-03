from django.http import HttpResponse
from django.shortcuts import render
from random import randint
from game.form import GameForm
from game.models import Player, Game, PlayerGameInfo


def show_home(request):
    context = {}
    current_game = Game.objects.filter(is_finished=False).first()

    if not request.session.session_key:
        request.session.create()
    session_id = request.session.session_key

    user = Player.objects.get_or_create(player_session=session_id)[0]

    if request.method == 'GET':
        if not current_game:
            hidden_number = randint(1, 100)
            current_game = Game.objects.create(hidden_number=hidden_number)
            current_game.creator.set(user)
            request.session['game_owner'] = user.id

        if not PlayerGameInfo.objects.filter(game=current_game, players=user):
            PlayerGameInfo.objects.create(game=current_game, players=user)

        context['hidden_number'] = current_game.hidden_number
        context['game_owner'] = request.session.get('game_owner', None)
        request.session['current_game_id'] = current_game.id
        request.session['hidden_number'] = current_game.hidden_number
        context['form'] = GameForm
    return render(request, 'home.html', context)

    # if request.method == "POST":
    #     game_form = GameForm(request.POST)
    #     # request.session.create()
    #     if game_form.is_valid():
    #         player_number = game_form.cleaned_data
    #         player_game = Player.objects.create(**player_number)
    #         request.session['player_game_id'] = player_game.id
    #         request.session['player_number'] = player_game.player_number
    #         context['player_id'] = request.session.get('player_game_id')
    #         if request.session.get("player_number") == request.session.get("hidden_number"):
    #             Game.objects.set(is_finished=True)
    #             return HttpResponse('Вы угадали загаданное число!')
    #         elif request.session.get("player_number") > request.session.get("hidden_number"):
    #             return HttpResponse('Введенное число больше угадываемого.')
    #         elif request.session.get("player_number") < request.session.get("hidden_number"):
    #             return HttpResponse('Введенное число меньше угадываемого.')
    # else:
    #     game_form = GameForm()
    #     return render(
    #         request,
    #         'home.html',
    #         {'form': game_form}
    #     )
  