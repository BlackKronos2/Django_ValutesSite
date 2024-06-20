import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

class ValuteData:

    def __init__(self, name, value, char_code):
        self.name = name
        self.value = value
        self.char_code = char_code


class ValutesParser:
    def __init__(self):
        self.url = 'https://www.cbr.ru/currency_base/daily/'

    def parse_currencies(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table', {'class': 'data'})
            currencies = []
            for row in table.find_all('tr')[1:]:
                columns = row.find_all('td')
                code = columns[1].text.strip()
                name = columns[3].text.strip()
                value = float(columns[4].text.replace(',', '.'))
                currencies.append(ValuteData(name, value, code))
            return currencies

    @staticmethod
    def get_currency_rate(self, currency):
        currencies = self.parse_currencies()
        if currency in currencies:
            return currencies[currency]
        else:
            print("Currency not found.")

    def get_currency_history(self, valute_code):
        # Вычисляем даты за последние 30 дней
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=30)

        # Формируем URL для получения курса валют ЦБ РФ
        url = f'https://www.cbr.ru/currency_base/dynamics/?UniDbQuery.Posted=True&UniDbQuery.To={end_date.strftime("%d.%m.%Y")}&UniDbQuery.From={start_date.strftime("%d.%m.%Y")}&UniDbQuery.Currency={valute_code}'

        # Отправка запроса и получение содержимого страницы
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Находим таблицу с курсами валют
        table = soup.find('table', {'class': 'data'})

        # Проверяем, найдена ли таблица
        if table is None:
            return "Таблица с курсами валют не найдена."

        # Извлекаем данные за последние 30 дней
        rows = table.find_all('tr')[1:]  # Пропускаем заголовок таблицы

        # Проверяем, есть ли строки с данными
        if not rows:
            return "Данные о курсах валют за последние 30 дней не найдены."

        dates = []
        rates = []
        rows.remove(rows[0])

        for row in rows:
            data = row.find_all('td')
            dates.append(datetime.strptime(data[0].text.strip(), "%d.%m.%Y"))
            rates.append(float(data[2].text.replace(',', '.')))

        return dates, rates

    def parse_all_currencies(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table', {'class': 'data'})
            currencies = {}
            for row in table.find_all('tr')[1:]:
                columns = row.find_all('td')
                name = columns[1].text.strip()
                value = float(columns[4].text.replace(',', '.'))
                currencies[name] = value
            return currencies