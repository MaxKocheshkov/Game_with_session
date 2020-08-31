from django.contrib.sessions.models import Session
from django.db import models


class Player(models.Model):
    player_number = models.IntegerField(default=None, verbose_name="Введите число")
    player_session = models.ForeignKey(Session, on_delete=models.CASCADE)


class Game(models.Model):
    hidden_number = models.IntegerField(default=None, verbose_name="Введите число")
    is_finished = models.BooleanField(default=False)
    creator = models.ManyToManyField(
        Player,
        through='PlayerGameInfo',
        through_fields=('game', 'players')
    )


class PlayerGameInfo(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    players = models.ForeignKey(Player, on_delete=models.CASCADE)
    attempts = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name='player_game_attempts'
    )
    player_attempts = models.IntegerField()