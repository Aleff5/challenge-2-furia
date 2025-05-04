from tortoise import fields, models

class Game(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, unique=True)
    followers = fields.IntField(default=0)

    class Meta:
        table = "games"


class UserGame(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="games", on_delete=fields.CASCADE)
    game = fields.ForeignKeyField("models.Game", related_name="user_followers", on_delete=fields.CASCADE)

    class Meta:
        table = "user_games"
        unique_together = ("user", "game")
        indexes = [("user",), ("game",)]
      
