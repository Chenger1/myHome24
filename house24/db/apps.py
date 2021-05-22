from django.apps import AppConfig
from django.db.models.signals import post_migrate


def create_role_instances(sender, **kwargs):
    #  Create basic instances after migrations
    from db.models.user import Role  # import inside function because apps aren`t loaded yet
    for name in Role.reserved_names:
        if not Role.objects.filter(name=name).exists():
            Role.objects.create(name=name)


class DbConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'db'

    def ready(self):
        post_migrate.connect(create_role_instances, sender=self)
