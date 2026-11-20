

from PyQt5.QtCore import QObject, pyqtSignal


class Data(QObject):
    
    value_changed = pyqtSignal(str, float)

    
    RUB_PER_USD = 82.0
    USD_PER_EUR = 1.10

    def __init__(self):
        super().__init__()
        self.myData = {"USD": 0.0, "RUB": 0.0, "EUR": 0.0}

    def getData(self):
        return self.myData.copy()

    def setData(self, currency, value):
        if currency == "USD":
            usd = value
        elif currency == "RUB":
            usd = value / self.RUB_PER_USD
        elif currency == "EUR":
            usd = value * self.USD_PER_EUR
        else:
            raise ValueError(f"Неизвестная валюта: {currency}")

        self.myData = {
            "USD": usd,
            "RUB": usd * self.RUB_PER_USD,
            "EUR": usd / self.USD_PER_EUR,
        }
        self.value_changed.emit(currency, value)
