from django.db.models import Sum, Avg

from db.models.house import PaymentTicket

import datetime
import calendar


class StatisticController:
    def __init__(self, flat):
        self.flat = flat
        self.tickets = PaymentTicket.objects.filter(flat=self.flat)
        self.today = datetime.date.today()

    def prepare_statistic(self):
        result = {
            'total_balance': self.prepare_flat_balance(),
            'account': self.prepare_flat_account(),
            'average': self.prepare_average_outcome(),
            'month_outcome': self.prepare_month_outcome(),
            'year_outcome': self.prepare_year_outcome(),
            'outcome_by_month': self.prepare_outcome_by_month()
        }
        return result

    def prepare_flat_balance(self):
        total_debt = self.tickets.filter(is_done=True, status__in=(2, 1)).aggregate(Sum('sum'))
        total_paid = self.tickets.filter(is_done=True, status__in=(0, 1)).aggregate(Sum('transactions__paid_sum'))

        return round((total_paid['transactions__paid_sum__sum'] or 0) - (total_debt['sum__sum'] or 0), 2)

    def prepare_flat_account(self):
        return self.flat.account.number

    def prepare_average_outcome(self):
        days = calendar.monthrange(self.today.year, self.today.month)[1]

        average_outcome = self.tickets.filter(created__month=self.today.month).aggregate(Avg('services__outcome'))
        if average_outcome['services__outcome__avg']:
            return round(average_outcome['services__outcome__avg'] / days, 2)
        else:
            return 0

    def prepare_month_outcome(self):
        current_month_tickets = self.tickets.filter(created__month=self.today.month)
        return self.calculate_outcome(current_month_tickets)

    def prepare_year_outcome(self):
        current_year_tickets = self.tickets.filter(created__year=self.today.year)
        return self.calculate_outcome(current_year_tickets)

    def prepare_outcome_by_month(self):
        result = []
        for month in range(1, 13):
            # data = self.tickets.filter(created__month=month).values('services__service__name')\
            #     .annotate(service_sum=Sum('services__outcome'))
            data = self.tickets.filter(created__month=month).aggregate(service_sum=Sum('services__outcome'))
            if data.get('service_sum'):
                result.append(data.get('service_sum', 0))
            else:
                result.append(0)
        return result

    def calculate_outcome(self, queryset):
        # result = {}
        # for ticket in queryset:
        #     for service in ticket.services.all():
        #         if result.get(service.service.name):
        #             result[service.service.name] += service.outcome
        #         else:
        #             result[service.service.name] = service.outcome
        # return result
        data = queryset.values('services__service__name').annotate(Sum('services__outcome'))
        return self.serializer_value_queryset(data)

    def serializer_value_queryset(self, queryset):
        result = {}
        for index, ser in enumerate(queryset):
            result[index] = ser
        return result
