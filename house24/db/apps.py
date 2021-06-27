from django.apps import AppConfig
from django.db.models.signals import post_migrate


def create_role_instances(sender, **kwargs):
    #  Create basic instances after migrations
    from db.models.user import Role  # import inside function because apps aren`t loaded yet
    for name in Role.reserved_names:
        if not Role.objects.filter(name=name).exists():
            Role.objects.create(name=name)


def create_payment_item_instance(sender, **kwargs):
    from db.models.house import PaymentItem
    PaymentItem.objects.get_or_create(name='Основной приход', type=0, default_income_type=True)
    PaymentItem.objects.get_or_create(name='Основной расход', type=1, default_income_type=True)


def create_measure_instances(sender, **kwargs):
    from db.models.house import Measure
    Measure.objects.get_or_create(measure_name='м3')
    Measure.objects.get_or_create(measure_name='грн./м2')
    Measure.objects.get_or_create(measure_name='грн./мес.')
    Measure.objects.get_or_create(measure_name='кв.м.кКал')
    Measure.objects.get_or_create(measure_name='ед.')
    Measure.objects.get_or_create(measure_name='мес.')
    Measure.objects.get_or_create(measure_name='кВт.ч')


class DbConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'db'

    def ready(self):
        post_migrate.connect(create_role_instances, sender=self)
        post_migrate.connect(create_payment_item_instance, sender=self)
        post_migrate.connect(create_measure_instances, sender=self)
