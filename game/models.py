from django.db import models


class Player(models.Model):
    player_id = models.ForeignKey('Game', on_delete=models.CASCADE)
    player_number = models.IntegerField(default=None)


class Game(models.Model):
    game_id = models.IntegerField()
    game_info = models.ManyToManyField(
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