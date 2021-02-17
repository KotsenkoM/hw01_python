import datetime as dt


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, new_note):
        self.records.append(new_note)

    def get_today_stats(self):
        today = dt.date.today()
        return sum(note.amount for note in self.records
                   if note.date == today)

    def remainder(self):
        return self.limit - self.get_today_stats()

    def get_week_stats(self):
        today = dt.date.today()
        week_ago = today - dt.timedelta(days=7)
        return sum(note.amount for note in self.records
                   if today >= note.date >= week_ago)


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        remaind = self.remainder()
        if 0 < remaind:
            return (
                'Сегодня можно съесть что-нибудь ещё, '
                f'но с общей калорийностью не более {remaind} кКал'
            )
        return 'Хватит есть!'


class CashCalculator(Calculator):
    RUB_RATE = 1.0
    EURO_RATE = 88.91
    USD_RATE = 73.27

    def get_today_cash_remained(self, currency):
        remaind = self.remainder()
        if remaind == 0:
            return 'Денег нет, держись'
        abs_remaind = abs(remaind)
        currency_list = {
            'rub': ('руб', self.RUB_RATE),
            'eur': ('Euro', self.EURO_RATE),
            'usd': ('USD', self.USD_RATE)
        }
        set_currency = ','.join(currency_list.keys())
        if currency not in currency_list:
            raise ValueError(
                f'"{currency}" - валюта неверная, '
                f'правильные: {set_currency}'
            )
        currency_name, currency_rate = currency_list[currency]
        value = round(abs_remaind / currency_rate, 2)
        if remaind > 0:
            return f'На сегодня осталось {value} {currency_name}'
        return (
            'Денег нет, держись: '
            f'твой долг - {value} {currency_name}'
        )
