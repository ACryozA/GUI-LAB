import sys
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlQuery, QSqlQueryModel
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QComboBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTabWidget,
    QTableView,
    QVBoxLayout,
    QWidget,
    QHeaderView,
)

from database import DatabaseManager
from queries import (
    QUERY_TAB1,
    QUERY_TAB2,
    QUERY_TAB4,
    QUERY_TAB5,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Лабораторная работа №3 — PyQt5 и SQLite")
        self.resize(1100, 690)

        self.database = DatabaseManager()
        self.models = [None] * 5
        self.views = []
        self.tab_labels = []

        self.build_menu()
        self.build_interface()
        self.apply_styles()
        self.set_connected_state(False)
        self.statusBar().showMessage("Подключите базу: Menu → Set connection")

    def build_menu(self):
        menu = self.menuBar().addMenu("Menu")

        self.connect_action = QAction("Set connection", self)
        self.connect_action.triggered.connect(self.select_database)
        menu.addAction(self.connect_action)

        self.close_action = QAction("Close connection", self)
        self.close_action.triggered.connect(self.close_connection)
        menu.addAction(self.close_action)

    def build_interface(self):
        central = QWidget(self)
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(22, 20, 22, 20)
        layout.setSpacing(18)

        controls = QHBoxLayout()
        controls.setSpacing(12)

        self.button1 = QPushButton('bt1 «SELECT Column»')
        self.button1.clicked.connect(self.run_tab2)
        controls.addWidget(self.button1)

        self.button2 = QPushButton('bt2 «Query2»')
        self.button2.clicked.connect(self.run_tab4)
        controls.addWidget(self.button2)

        self.button3 = QPushButton('bt3 «Query3»')
        self.button3.clicked.connect(self.run_tab5)
        controls.addWidget(self.button3)

        controls.addStretch(1)
        controls.addWidget(QLabel('Tables:'))

        self.column_combo = QComboBox()
        self.column_combo.setMinimumWidth(220)
        self.column_combo.addItem('Выберите колонку...', None)
        self.column_combo.currentIndexChanged.connect(self.run_tab3)
        controls.addWidget(self.column_combo)
        layout.addLayout(controls)

        self.tabs = QTabWidget()
        for index in range(5):
            page = QWidget()
            page_layout = QVBoxLayout(page)
            page_layout.setContentsMargins(12, 16, 12, 12)
            page_layout.setSpacing(10)

            description = QLabel('Нет данных. Подключите базу SQLite через Menu.')
            description.setWordWrap(True)
            description.setObjectName('description')
            page_layout.addWidget(description)

            view = QTableView()
            view.setAlternatingRowColors(True)
            view.setSelectionBehavior(QTableView.SelectRows)
            view.setSelectionMode(QTableView.SingleSelection)
            view.setEditTriggers(QTableView.NoEditTriggers)
            view.verticalHeader().setDefaultSectionSize(34)
            view.horizontalHeader().setMinimumHeight(38)
            view.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
            view.horizontalHeader().setStretchLastSection(True)
            page_layout.addWidget(view)

            self.tabs.addTab(page, f'Tab{index + 1}')
            self.views.append(view)
            self.tab_labels.append(description)
        layout.addWidget(self.tabs, 1)

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow, QWidget { background-color: #f7f9fc; color: #1f2937; }
            QMenuBar { background-color: #ffffff; font-size: 12pt; padding: 5px; }
            QMenu { background-color: #ffffff; font-size: 11pt; }
            QPushButton {
                background-color: #e8eef9; border: 1px solid #bbc9e0;
                border-radius: 7px; min-height: 46px;
                padding: 0 16px; font-size: 11pt; font-weight: 300;
            }
            QPushButton:hover { background-color: #d7e5fc; }
            QPushButton:pressed { background-color: #c5d8f6; }
            QPushButton:disabled {
                background-color: #e8e9ed; color: #9ca3af;
                border-color: #d8dbe2;
            }
            QLabel { font-size: 10pt; }
            QLabel#description { color: #4b5563; padding: 4px 0; }
            QComboBox {
                min-height: 46px; background: #ffffff;
                border: 1px solid #bbc9e0; border-radius: 7px;
                padding: 0 12px; font-size: 10pt;
            }
            QComboBox:disabled { background: #eeeeef; color: #9ca3af; }
            QComboBox QAbstractItemView { background: #ffffff; font-size: 11pt; }
            QTabWidget::pane {
                border: 1px solid #d0d8e5; border-radius: 5px;
                background-color: #ffffff;
            }
            QTabBar::tab {
                font-size: 11pt;
                font-weight: regular;
                min-width: 50px;
                min-height: 20px;
                padding: 8px 20px;
                background-color: #e8edf5;
                border: 1px solid #ccd6e4;
}

QTabBar::tab:selected {
    background-color: white;
}
            QTabBar::tab:hover { background-color: #dce7f7; }
            QTableView {
                background-color: #ffffff; alternate-background-color: #f2f6fc;
                gridline-color: #e2e8f0; font-size: 11pt;
                selection-background-color: #cfe2fa;
                selection-color: #1f2937;
            }
            QHeaderView::section {
                background-color: #eaf0f8; border: 1px solid #d6deea;
                padding: 6px; font-size: 11pt; font-weight: 600;
            }
            QStatusBar { font-size: 10pt; background-color: #ffffff; }
        """)

    def set_connected_state(self, connected: bool):
        self.button1.setEnabled(connected)
        self.button2.setEnabled(connected)
        self.button3.setEnabled(connected)
        self.column_combo.setEnabled(connected)
        self.close_action.setEnabled(connected)

    def clear_tables(self):
        for index, view in enumerate(self.views):
            view.setModel(None)
            model = self.models[index]
            if model is not None:
                model.clear()
                model.deleteLater()
                self.models[index] = None
            self.tab_labels[index].setText("Нет данных. Подключите базу SQLite через Menu.")
        self.column_combo.blockSignals(True)
        self.column_combo.setCurrentIndex(0)
        self.column_combo.blockSignals(False)
        self.tabs.setCurrentIndex(0)

    def close_connection(self):
        self.clear_tables()
        self.database.close()
        self.set_connected_state(False)
        self.statusBar().showMessage("Соединение закрыто. Все таблицы очищены.")

    def select_database(self):
        start_dir = str(Path(__file__).resolve().parent)
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите базу данных SQLite",
            start_dir,
            "SQLite (*.db *.sqlite *.sqlite3);;Все файлы (*)",
        )
        if not file_path:
            return  # Отмена выбора не разрывает текущее подключение.

        self.close_connection()
        ok, error_text = self.database.open(file_path)
        if not ok:
            QMessageBox.critical(self, "Ошибка подключения", error_text)
            self.statusBar().showMessage("Не удалось подключиться к базе данных")
            return

        self.load_tables()
        self.set_connected_state(True)
        self.display_query(0, QUERY_TAB1, "SELECT * FROM sqlite_master")
        self.statusBar().showMessage(f"Подключено: {file_path}")

    def display_query(self, tab_index: int, sql: str, description: str):
        if not self.database.connected:
            QMessageBox.warning(self, "Нет соединения", "Сначала подключите базу данных.")
            return

        self.views[tab_index].setModel(None)
        old_model = self.models[tab_index]
        if old_model is not None:
            old_model.clear()
            old_model.deleteLater()

        model = QSqlQueryModel(self)
        model.setQuery(sql, self.database.db)
        error = model.lastError()
        if error.isValid():
            self.models[tab_index] = None
            model.deleteLater()
            QMessageBox.critical(self, "Ошибка SQL", error.text())
            return

        self.models[tab_index] = model
        self.views[tab_index].setModel(model)
        self.tab_labels[tab_index].setText(description)
        self.tabs.setCurrentIndex(tab_index)
        self.statusBar().showMessage(f"Tab{tab_index + 1}: запрос выполнен")

    def run_tab2(self):
        self.display_query(1, QUERY_TAB2, "SELECT name FROM sqlite_master ORDER BY name")

    
    def load_tables(self):

        self.column_combo.blockSignals(True)
        self.column_combo.clear()
        self.column_combo.addItem("Выберите таблицу...", None)

        query = QSqlQuery(self.database.db)
        query.exec_("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """)

        while query.next():
            table_name = query.value(0)
            self.column_combo.addItem(table_name, table_name)

        self.column_combo.blockSignals(False)


    
    def run_tab3(self, index: int):

        table_name = self.column_combo.itemData(index)

        if not table_name or not self.database.connected:
            return

        # Проверяем, что таблица присутствует в списке
        query = QSqlQuery(self.database.db)
        query.prepare("""
            SELECT COUNT(*)
            FROM sqlite_master
            WHERE type = 'table' AND name = ?
        """)
        query.addBindValue(table_name)

        if not query.exec_() or not query.next() or query.value(0) == 0:
            QMessageBox.warning(
                self, "Ошибка", "Выбранная таблица не найдена."
            )
            return

        safe_name = table_name.replace('"', '""')

        sql = f'SELECT * FROM "{safe_name}"'

        self.display_query(
            2,
            sql,
            f'Содержимое таблицы "{table_name}"'
        )


    def run_tab4(self):
        self.display_query(3, QUERY_TAB4, "Количество объектов базы данных по типам")

    def run_tab5(self):
        self.display_query(4, QUERY_TAB5, "Список пользовательских таблиц и SQL их создания")

    def closeEvent(self, event):
        self.clear_tables()
        self.database.close()
        event.accept()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
