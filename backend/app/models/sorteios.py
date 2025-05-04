from tortoise import fields, models

class Sorteio(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=100)
    description = fields.TextField(null=True)
    start_date = fields.DatetimeField()
    end_date = fields.DatetimeField()
    created_at = fields.DatetimeField(auto_now_add=True, use_timezone=True)

    class Meta:
        table = "sorteios"


class UserSorteio(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="raffles", on_delete=fields.CASCADE)
    sorteio = fields.ForeignKeyField("models.Sorteio", related_name="participants", on_delete=fields.CASCADE)
    status = fields.CharField(max_length=20, default="registered")
    joined_at = fields.DatetimeField(auto_now_add=True, use_timezone=True)

    class Meta:
        table = "user_sorteio"
        unique_together = ("user", "sorteio")
        indexes = [("user",), ("sorteio",)]


