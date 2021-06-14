import xlwt


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


class TransactionSpreadSheet(SpreadSheerCreator):
    def create_spreadsheet(self, queryset):
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        self.ws.write(0, 0, '#', font_style)
        self.ws.write(0, 1, 'Дата', font_style)
        self.ws.write(0, 3, 'Тип платежа', font_style)
        self.ws.write(0, 5, 'Владелец', font_style)
        self.ws.write(0, 8, 'Лицевой счет', font_style)
        self.ws.write(0, 11, 'Статус', font_style)
        self.ws.write(0, 14, 'Квитанция', font_style)
        self.ws.write(0, 17, 'Приход/расход', font_style)
        self.ws.write(0, 19, 'Сумма(грн)', font_style)
        self.ws.write(0, 21, 'Валюта', font_style)

        font_style = xlwt.XFStyle()
        row_num = 0
        for row_data in queryset:
            row_num += 1
            self.ws.write(row_num, 0, row_data.number, font_style)
            self.ws.write(row_num, 1, row_data.created.strftime('%d-%m-%Y'), font_style)
            self.ws.write(row_num, 3, row_data.payment_item_type.name, font_style)
            self.ws.write(row_num, 5, row_data.owner, font_style)
            self.ws.write(row_num, 8, row_data.personal_account, font_style)
            self.ws.write(row_num, 11, row_data.status_display, font_style)
            if row_data.payment_ticket:
                self.ws.write(row_num, 14, row_data.payment_ticket.__str__(), font_style)
            else:
                self.ws.write(row_num, 14, '', font_style)
            self.ws.write(row_num, 17, row_data.payment_item_type.get_type_display(), font_style)
            self.ws.write(row_num, 19, row_data.paid_sum, font_style)
            self.ws.write(row_num, 21, 'грн.', font_style)
        return self.wb
