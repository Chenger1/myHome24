from django.db.models import Sum

from dataclasses import dataclass

from db.models.house import House, Flat, PersonalAccount, MasterRequest, PaymentTicket, Transaction
from db.models.user import User


@dataclass
class Statistic:
    """
    All fields are optional.
    """
    houses: int = None
    flats: int = None
    accounts: int = None
    users: int = None
    new_requests: int = None
    requests_in_work: int = None
    total_cash: int = None
    total_debt: int = None
    total_account_balance: int = None
    transaction_chart_income: dict = None
    transaction_chart_outcome: dict = None
    paid_ticket: dict = None
    unpaid_ticket: dict = None


class StatisticController:
    def prepare_statistic(self):
        total_cash, total_debt, total_account_balance = self.prepare_transaction()
        statistic = Statistic(
                self.prepare_houses(),
                self.prepare_flats(),
                self.prepare_accounts(),
                self.prepare_users(),
                self.prepare_new_requests(),
                self.prepare_requests_in_work(),
                total_cash,
                total_debt,
                total_account_balance,
                self.prepare_income(),
                self.prepare_outcome(),
                self.prepare_paid_ticket(),
                self.prepare_unpaid_ticket()
           )
        return statistic

    @staticmethod
    def prepare_houses():
        return House.objects.count()

    @staticmethod
    def prepare_flats():
        return Flat.objects.count()

    @staticmethod
    def prepare_accounts():
        return PersonalAccount.objects.count()

    @staticmethod
    def prepare_users():
        return User.objects.filter(is_staff=False, status=0).count()

    @staticmethod
    def prepare_new_requests():
        return MasterRequest.objects.filter(status=0).count()

    @staticmethod
    def prepare_requests_in_work():
        return MasterRequest.objects.filter(status=1).count()

    @staticmethod
    def prepare_transaction():
        total_debt, balance = PaymentTicket.total_balance()
        return Transaction.total_cash(), total_debt, balance

    @staticmethod
    def prepare_income():
        result = {}
        for month in range(1, 13):
            result[month] = Transaction.objects.filter(created__month=month, payment_item_type__type=0).\
                                aggregate(Sum('paid_sum'))['paid_sum__sum'] or 0
        return result

    @staticmethod
    def prepare_outcome():
        result = {}
        for month in range(1, 13):
            result[month] = Transaction.objects.filter(created__month=month, payment_item_type__type=1).\
                                aggregate(Sum('paid_sum'))['paid_sum__sum'] or 0
        return result

    @staticmethod
    def prepare_paid_ticket():
        result = {}
        for month in range(1, 13):
            result[month] = PaymentTicket.objects.filter(created__month=month, status=0). \
                                aggregate(Sum('sum'))['sum__sum'] or 0
        return result

    @staticmethod
    def prepare_unpaid_ticket():
        result = {}
        for month in range(1, 13):
            result[month] = PaymentTicket.objects.filter(created__month=month, status__in=(1, 2)). \
                                aggregate(Sum('sum'))['sum__sum'] or 0
        return result


class MinimalStatisticCollector(StatisticController):
    """
        For 'account-transaction' and 'payment-tickets' pages
    """
    def prepare_statistic(self):
        total_cash, total_debt, total_account_balance = self.prepare_transaction()
        statistic = Statistic(
            total_cash=total_cash,
            total_debt=total_debt,
            total_account_balance=total_account_balance
        )
        return statistic
