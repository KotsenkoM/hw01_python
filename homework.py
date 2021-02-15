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
        self.today = dt.date.today()

    def add_record(self, new_note):
        self.records.append(new_note)

    def get_today_stats(self):
        return sum(note.amount for note in self.records
                   if note.date == self.today)

    def remainder(self):
        get_rem = self.limit - self.get_today_stats()
        return get_rem

    def get_week_stats(self):
        week_ago = self.today - dt.timedelta(days=7)
        return sum(note.amount for note in self.records
                   if self.today >= note.date >= week_ago)


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        if 0 < self.remainder() < self.limit:
            return (
                'Сегодня можно съесть что-нибудь ещё, '
                f'но с общей калорийностью не более {self.remainder()} кКал'
            )
        return 'Хватит есть!'


class CashCalculator(Calculator):
    RUB_RATE = 1
    EURO_RATE = 88.91
    USD_RATE = 73.27

    def get_today_cash_remained(self, currency):
        try:
            rub = abs(self.remainder())
            euro = round(rub / self.EURO_RATE, 2)
            usd = round(rub / self.USD_RATE, 2)
            currency_list = {
                'rub': ('руб', rub),
                'eur': ('Euro', euro),
                'usd': ('USD', usd)
            }

            set_currency = ','.join(set(currency_list.keys()))

            currency_name, currency_rate = currency_list[currency]
            if 0 < self.get_today_stats() < self.limit:
                return f'На сегодня осталось {currency_rate} {currency_name}'
            if self.get_today_stats() > self.limit:
                return (
                    'Денег нет, держись: ' 
                    f'твой долг - {currency_rate} {currency_name}'
                )
            if self.get_today_stats() == self.limit:
                return 'Денег нет, держись'
        except KeyError:
            return (
                f'"{currency}" - валюта неверная, '
                f'правильные: {set_currency}'
            )
