import xlwt
from django.utils.translation import gettext_lazy as _


class SpreadSheerCreator:
    def __init__(self, model):
        self.model = model
        self.wb = None
        self.ws = None
        self._create_new_file()

    def create_spreadsheet(self, queryset):
        pass

    def _create_new_file(self):
        self.wb = xlwt.Workbook(encoding='utf-8')
        self.ws = self.wb.add_sheet(self.model.__name__)

    def check_for_none(self, value):
        if value == 'None':
            return ''
        return value


class TransactionSpreadSheet(SpreadSheerCreator):
    def create_spreadsheet(self, queryset):
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        self.ws.write(0, 0, '#', font_style)
        self.ws.write(0, 1, _('Date'), font_style)
        self.ws.write(0, 3, _('Transaction type'), font_style)
        self.ws.write(0, 5, _('Owner'), font_style)
        self.ws.write(0, 8, _('Account'), font_style)
        self.ws.write(0, 11, _('Status'), font_style)
        self.ws.write(0, 14, _('Receipt'), font_style)
        self.ws.write(0, 17, _('Income/outcome'), font_style)
        self.ws.write(0, 19, _('Sum'), font_style)
        self.ws.write(0, 21, _('Currency'), font_style)

        font_style = xlwt.XFStyle()
        row_num = 0
        for row_data in queryset:
            row_num += 1
            self.ws.write(row_num, 0, row_data.number, font_style)
            self.ws.write(row_num, 1, row_data.created.strftime('%d-%m-%Y'), font_style)
            self.ws.write(row_num, 3, row_data.payment_item_type.name, font_style)
            self.ws.write(row_num, 5, self.check_for_none(str(row_data.owner)), font_style)
            self.ws.write(row_num, 8, self.check_for_none(str(row_data.personal_account)), font_style)
            self.ws.write(row_num, 11, row_data.status_display, font_style)
            self.ws.write(row_num, 14, self.check_for_none(str(row_data.payment_ticket)), font_style)
            self.ws.write(row_num, 17, row_data.payment_item_type.get_type_display(), font_style)
            self.ws.write(row_num, 19, row_data.paid_sum, font_style)
            self.ws.write(row_num, 21, 'грн.', font_style)
        return self.wb


class ConcreteTransactionSpreadSheer(SpreadSheerCreator):
    def create_spreadsheet(self, queryset):
        font_style = xlwt.XFStyle()
        # init info row
        self.ws.write(0, 0, _('Transaction'), font_style)
        self.ws.write(1, 0, _('Date'), font_style)
        self.ws.write(2, 0, _('Flat owner'), font_style)
        self.ws.write(3, 0, _('Account'), font_style)
        self.ws.write(4, 0, _('Income/Outcome'), font_style)
        self.ws.write(5, 0, _('Status'), font_style)
        self.ws.write(6, 0, _('Type'), font_style)
        self.ws.write(7, 0, _('Receipt'), font_style)
        self.ws.write(8, 0, _('SUm'), font_style)
        self.ws.write(9, 0, _('Currency'), font_style)
        self.ws.write(10, 0, _('Comment'), font_style)
        self.ws.write(11, 0, _('Manager'), font_style)
        # init data rows
        self.ws.write(0, 4, queryset.number, font_style)
        self.ws.write(1, 4, queryset.created.strftime('%d.%m.%Y'), font_style)
        self.ws.write(2, 4, self.check_for_none(str(queryset.owner)), font_style)
        self.ws.write(3, 4, self.check_for_none(str(queryset.personal_account)), font_style)
        self.ws.write(4, 4, queryset.payment_item_type.get_type_display(), font_style)
        self.ws.write(5, 4, queryset.status_display, font_style)
        self.ws.write(6, 4, queryset.payment_item_type.name, font_style)
        self.ws.write(7, 4, self.check_for_none(str(queryset.payment_ticket)), font_style)
        self.ws.write(8, 4, queryset.paid_sum, font_style)
        self.ws.write(9, 4, 'грн.', font_style)
        self.ws.write(10, 4, queryset.description, font_style)
        self.ws.write(11, 4, self.check_for_none(str(queryset.manager)), font_style)
        return self.wb


class AccountSpreadSheet(SpreadSheerCreator):
    def create_spreadsheet(self, queryset):
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        self.ws.write(0, 0, '№', font_style)
        self.ws.write(0, 1, _('Status'), font_style)
        self.ws.write(0, 3, _('Flat'), font_style)
        self.ws.write(0, 5, _('House'), font_style)
        self.ws.write(0, 8, _('Section'), font_style)
        self.ws.write(0, 11, _('Owner'), font_style)
        self.ws.write(0, 14, _('Balance'), font_style)
        font_style = xlwt.XFStyle()
        row_num = 0
        for row_data in queryset:
            row_num += 1
            self.ws.write(row_num, 0, row_data.number, font_style)
            self.ws.write(row_num, 1, row_data.get_status_display(), font_style)
            self.ws.write(row_num, 3, self.check_for_none(str(row_data.flat)), font_style)
            self.ws.write(row_num, 5, self.check_for_none(str(row_data.house)), font_style)
            self.ws.write(row_num, 8, self.check_for_none(str(row_data.section)), font_style)
            if row_data.flat and row_data.flat.owner:
                self.ws.write(row_num, 11, str(row_data.flat.owner), font_style)
            else:
                self.ws.write(row_num, 11, '', font_style)
            self.ws.write(row_num, 14, row_data.get_account_balance(), font_style)
        return self.wb
