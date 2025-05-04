from tortoise import fields, models

class User(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    email = fields.CharField(max_length=100, unique=True)
    password = fields.CharField(max_length=255)
    idade = fields.IntField(null=True) 
    nome = fields.CharField(max_length=100)
    cpf = fields.CharField(max_length=14, unique=True)
    estado = fields.CharField(max_length=2, null=True)
    endereco = fields.TextField(null=True)
    score = fields.IntField(default=0)
    bio = fields.TextField(null=True)
    avatar_url = fields.TextField(null=True)
    discord = fields.TextField(null=True)
    twitter = fields.CharField(max_length=255, null=True)
    steam = fields.TextField(null=True)
    google = fields.TextField(null=True)
    interesses = fields.TextField(null=True)
    is_verified = fields.BooleanField(default=False)
    document_type = fields.CharField(max_length=100, null=True)
    admin = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True, use_timezone=True)

    class Meta:
        table = "users"


class Follower(models.Model):
    id = fields.IntField(pk=True)
    follower = fields.ForeignKeyField("models.User", related_name="following", on_delete=fields.CASCADE)
    following = fields.ForeignKeyField("models.User", related_name="followers", on_delete=fields.CASCADE)
    created_at = fields.DatetimeField(auto_now_add=True, use_timezone=True)

    class Meta:
        table = "followers"
        unique_together = ("follower", "following")


class SocialAccount(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="social_accounts", on_delete=fields.CASCADE)
    platform = fields.CharField(max_length=50)
    username = fields.CharField(max_length=100, null=True)
    profile_url = fields.TextField(null=True)
    avatar_url = fields.TextField(null=True)
    connected_at = fields.DatetimeField(auto_now_add=True, use_timezone=True)
    last_checked = fields.DatetimeField(null=True)

    class Meta:
        table = "social_accounts"
