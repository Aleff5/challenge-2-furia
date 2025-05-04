from tortoise import fields, models

class Event(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=100)
    description = fields.TextField(null=True)
    event_date = fields.DatetimeField()
    created_at = fields.DatetimeField(auto_now_add=True, use_timezone=True)

    class Meta:
        table = "events"


class UserEvent(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="events", on_delete=fields.CASCADE)
    event = fields.ForeignKeyField("models.Event", related_name="participants", on_delete=fields.CASCADE)
    joined_at = fields.DatetimeField(auto_now_add=True, use_timezone=True)

    class Meta:
        table = "user_events"
        unique_together = ("user", "event")
        indexes = [("user",), ("event",)]
        
