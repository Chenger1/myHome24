from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils.translation import gettext_lazy as _


def create_role_instances(sender, **kwargs):
    #  Create basic instances after migrations
    from db.models.user import Role, RoleEnum  # import inside function because apps aren`t loaded yet

    try:
        for name in RoleEnum:
            if not Role.objects.filter(name.value).exists():
                Role.objects.create(name=name.value)
    except Exception:
        pass

def create_payment_item_instance(sender, **kwargs):
    from db.models.house import PaymentItem
    PaymentItem.objects.get_or_create(name=_('Main income'), type=0, default_income_type=True)
    PaymentItem.objects.get_or_create(name=_('Main outcome'), type=1)


def create_measure_instances(sender, **kwargs):
    from db.models.house import Measure
    Measure.objects.get_or_create(measure_name=_('м3'))
    Measure.objects.get_or_create(measure_name=_('cur./м2'))
    Measure.objects.get_or_create(measure_name=_('cur./mon'))
    Measure.objects.get_or_create(measure_name=_('sq.m.cCal'))
    Measure.objects.get_or_create(measure_name='un.')
    Measure.objects.get_or_create(measure_name='month')
    Measure.objects.get_or_create(measure_name='kw.h')


class DbConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'db'

    def ready(self):
        post_migrate.connect(create_role_instances, sender=self)
        post_migrate.connect(create_payment_item_instance, sender=self)
        post_migrate.connect(create_measure_instances, sender=self)
