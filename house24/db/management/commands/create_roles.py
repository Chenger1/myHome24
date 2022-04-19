import logging

from django.core.management import BaseCommand

from db.models.user import Role, RoleEnum


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            roles = []
            for name in RoleEnum:
                if not Role.objects.filter(name=name.value).exists():
                    roles.append(Role(name=name.value))
            Role.objects.bulk_create(roles)
        except Exception as e:
            logger.error(str(e))
        else:
            logger.info('Roles created')
