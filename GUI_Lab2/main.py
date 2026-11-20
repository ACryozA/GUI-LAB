import math
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton
)
from cl1 import Data
from cl2 import CurrencyField


class Some(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Лабораторная №2")
        self.resize(530, 545)
        self.setMinimumWidth(420)

        self.data = Data()
        self.fields = {
            "USD": CurrencyField("USD", "Доллар США", "$"),
            "RUB": CurrencyField("RUB", "Российский рубль", "₽"),
            "EUR": CurrencyField("EUR", "Евро", "€"),
        }

        root = QWidget()
        root.setObjectName("root")
        layout = QVBoxLayout(root)
        layout.setContentsMargins(28, 26, 28, 26)
        layout.setSpacing(12)

        heading = QLabel("Конвертер валют")
        heading.setObjectName("heading")
        subtitle = QLabel("Измените любое поле - остальные обновятся автоматически")
        subtitle.setObjectName("subtitle")
        subtitle.setWordWrap(True)
        layout.addWidget(heading)
        layout.addWidget(subtitle)
        layout.addSpacing(7)

        for field in self.fields.values():
            layout.addWidget(field)
            field.edited.connect(self.on_amount_edited)

        self.info = QLabel("Курс валют 1 USD = 82 RUB; 1 EUR = 1.10 USD")
        self.info.setObjectName("info")
        self.info.setWordWrap(True)
        layout.addWidget(self.info)

        reset_button = QPushButton("Сбросить значения")
        reset_button.setObjectName("resetButton")
        reset_button.clicked.connect(self.reset_values)
        layout.addWidget(reset_button)
        layout.addStretch()
        self.setCentralWidget(root)

      
        self.data.value_changed.connect(self.update_fields)
        

    def on_amount_edited(self, currency, raw_text):
    
        raw_text = raw_text.strip().replace(" ", "").replace(",", ".")
        if not raw_text:
            for code, field in self.fields.items():
                if code != currency:
                    field.clear_amount()
            self.info.setText("Введите сумму в любое поле")
            return
        try:
            amount = float(raw_text)
            if not math.isfinite(amount) or amount < 0:
                raise ValueError
        except ValueError:
            self.info.setText("Введите неотрицательное число (например, 125.50)")
            return
        self.info.setText("Курс валют 1 USD = 82 RUB; 1 EUR = 1.10 USD")
        self.data.setData(currency, amount)

    def update_fields(self, source_currency, _value):
        for currency, amount in self.data.getData().items():
            if currency != source_currency:
                self.fields[currency].set_amount(amount)

    def reset_values(self):
        for field in self.fields.values():
            field.set_amount(0.0)
        self.data.setData("USD", 0.0)
        self.info.setText("Курс валют 1 USD = 82 RUB; 1 EUR = 1.10 USD")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Some()
    window.show()
    sys.exit(app.exec_())
