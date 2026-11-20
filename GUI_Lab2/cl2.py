
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFrame, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout


class CurrencyField(QFrame):
   
    edited = pyqtSignal(str, str)

    def __init__(self, currency, title, symbol):
        super().__init__()
        self.currency = currency
        self.setObjectName("currencyCard")

        caption = QLabel(title)
        caption.setObjectName("currencyTitle")
        code = QLabel(f"{currency}  {symbol}")
        code.setObjectName("currencyCode")
        self.input = QLineEdit("0.00")
        self.input.setPlaceholderText("Введите сумму")
        self.input.setObjectName("currencyInput")
        self.input.textEdited.connect(self._forward_change)

        heading = QHBoxLayout()
        heading.addWidget(caption)
        heading.addStretch()
        heading.addWidget(code)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 13, 18, 14)
        layout.setSpacing(8)
        layout.addLayout(heading)
        layout.addWidget(self.input)

    def _forward_change(self, text):
        self.edited.emit(self.currency, text)

    def set_amount(self, amount):
        self.input.blockSignals(True)
        try:
            self.input.setText(f"{amount:.2f}")
        finally:
            self.input.blockSignals(False)

    def clear_amount(self):
        self.input.blockSignals(True)
        try:
            self.input.clear()
        finally:
            self.input.blockSignals(False)
