import datetime as dt


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        date_format = '%d.%m.%Y'
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, date_format).date()


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, new_note):
        self.records.append(new_note)

    def get_today_stats(self):
        count_stats = 0
        for note in self.records:
            if note.date == dt.date.today():
                count_stats += note.amount
        return count_stats

    def get_week_stats(self):
        count_stats = 0
        today = dt.date.today()
        week_ago = today - dt.timedelta(days=7)
        for note in self.records:
            if today >= note.date >= week_ago:
                count_stats += note.amount
        return count_stats


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        count_cal = self.get_today_stats()
        today_cal = self.limit - count_cal
        if 0 < today_cal < self.limit:
            return f'Сегодня можно съесть что-нибудь ещё,' \
                   f'но с общей калорийностью не более {today_cal} кКал'
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    EURO_RATE = 89.63
    USD_RATE = 73.76

    def get_today_cash_remained(self, currency):
        spent_money = self.get_today_stats()
        count_money = self.limit - spent_money
        eur_money = count_money / self.EURO_RATE
        usd_money = count_money / self.USD_RATE
        if currency == 'rub' and 0 < count_money < self.limit:
            return f'На сегодня осталось {count_money} руб'
        elif currency == 'eur' and 0 < count_money < self.limit:
            return f'На сегодня осталось {round(eur_money, 2)} Euro'
        elif currency == 'usd' and 0 < count_money < self.limit:
            return f'На сегодня осталось {round(usd_money, 2)} USD'
        elif currency == 'rub' and spent_money > self.limit:
            return f'Денег нет, держись: твой долг - {count_money * -1} руб'
        elif currency == 'eur' and spent_money > self.limit:
            return f'Денег нет, держись: твой долг' \
                   f' - {round(eur_money, 2) * -1} Euro'
        elif currency == 'usd' and spent_money > self.limit:
            return f'Денег нет, держись: твой долг' \
                   f' - {round(usd_money, 2) * -1} USD'
        elif currency == 'rub' and spent_money == self.limit:
            return 'Денег нет, держись'
        elif currency == 'eur' and spent_money == self.limit:
            return 'Денег нет, держись'
        elif currency == 'usd' and spent_money == self.limit:
            return 'Денег нет, держись'
