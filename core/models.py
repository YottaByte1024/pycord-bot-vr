from tortoise import fields
from tortoise.models import Model

# __models__ = ('User', 'Role', 'Channel', 'Guild')
__all__ = ('User', 'Role', 'Channel', 'Guild')


class BaseModel(Model):
    class Meta:
        abstract = True


class User(Model):
    id = fields.BigIntField(pk=True)
    coins = fields.BigIntField(default=0)

    def __str__(self):
        return self.id

    class Meta:
        table = "user"


class Role(Model):
    id = fields.BigIntField(pk=True)
    description = fields.CharField(default='', max_length=256)
    guild: fields.ForeignKeyRelation["Guild"] = fields.ForeignKeyField(
        'models.Guild', related_name='roles',
        on_delete=fields.CASCADE, null=True)
    free_role = fields.BooleanField(default=False)
    resident_role = fields.BooleanField(default=False)
    adult_role = fields.BooleanField(default=False)

    class Meta:
        table = 'role'


class Channel(Model):
    id = fields.BigIntField(pk=True)
    description = fields.CharField(default='', max_length=256)
    guild: fields.ForeignKeyRelation["Guild"] = fields.ForeignKeyField(
        'models.Guild', related_name='channels',
        on_delete=fields.CASCADE, null=True)
    bot_channel = fields.BooleanField(default=False)
    rules_channel = fields.BooleanField(default=False)

    class Meta:
        table = 'channel'


class Guild(Model):
    id = fields.BigIntField(pk=True)

    roles: fields.ReverseRelation["Role"]

    def __str__(self):
        return self.id

    class Meta:
        table = 'guild'
