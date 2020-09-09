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

    if request.method == 'GET':
        game_owner = Player.objects.get_or_create(player_session=session_id)[0]
        if not current_game:
            hidden_number = randint(1, 100)
            current_game = Game.objects.create(hidden_number=hidden_number)
            current_game.creator.set(game_owner)
            request.session['game_owner'] = game_owner.id

        if not PlayerGameInfo.objects.filter(game=current_game, players=game_owner):
            PlayerGameInfo.objects.create(game=current_game, players=game_owner)

        context['hidden_number'] = current_game.hidden_number
        context['game_owner'] = request.session.get('game_owner', None)
        request.session['current_game_id'] = current_game.id
        request.session['hidden_number'] = current_game.hidden_number
        context['form'] = GameForm

    if request.method == 'POST':
        game_form = GameForm(request.POST)
        if game_form.is_valid():
            player_game = game_form.cleaned_data.get("player_number")
            player_number = Game.objects.create(player_number=player_game)
            if current_game.hidden_number == player_number.player_number:
                request.session['player_number'] = player_number.id
                Game.objects.create(is_finished=True)
                return HttpResponse('Вы угадали число!')
            elif current_game.hidden_number != player_number.player_number:
                request.session['player_number'] = player_number.id
                return HttpResponse('Попробуйте еще раз')

    return render(request, 'home.html', context)
