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
            user = Player.objects.get_or_create(player_session=session_id)[1]
            game_form = GameForm(request.POST)
            if game_form.is_valid():
                player_number = game_form.cleaned_data
                player_game = Game.objects.create(player_number=player_number)
                request.session['user'] = user.id
                context['player_number'] = player_game.player_number
                context['user'] = request.session.get('user', None)
                request.session['player_game_id'] = player_game.id
                request.session['player_number'] = player_game.player_number
                context['form'] = GameForm
                if context['player_number'] == context['hidden_number']:
                    Game.objects.set(is_finished=True)

    return render(request, 'home.html', context)

