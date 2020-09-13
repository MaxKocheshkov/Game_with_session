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

    if request.method == 'POST':
        form = GameForm(request.POST)

        if form.is_valid():
            if form.cleaned_data['player_number']:
                result_type = False
                result = 'Вы угадали, игра завершена'
                number_from_site = form.cleaned_data['player_number']
                number_current = request.session['hidden_number']

                if number_from_site > number_current:
                    result = 'Вы не угадали, ваше число больше загаданного'
                elif number_from_site < number_current:
                    result = 'Вы не угадали, ваше число меньше загаданного'
                else:
                    result_type = True
                    Game.objects.filter(id=request.session['current_game_id']).update(is_finished=True)
                # set_player_game_info(current_game, user, result_type)
                context['form'] = form
                context['result_text'] = result
                context['result_type'] = result_type

                return render(request, 'home.html', context)

    return render(
        request,
        'home.html', context=context
    )
