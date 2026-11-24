# Лабораторная работа №3 

## Цель

Реализовать приложение на PyQt5 с использованием `QTableView`, `QTabWidget`, `QComboBox`, `QFileDialog` и SQL-запросов к базе данных SQLite.

## Возможности

- **Menu → Set connection** — выбрать существующий файл базы данных `.db`, `.sqlite` или `.sqlite3` и открыть его.
- **Menu → Close connection** — закрыть соединение и очистить все пять вкладок.
- **Tab1** — после успешного подключения автоматически выводится `SELECT * FROM sqlite_master`.
- **bt1 «SELECT Column» → Tab2** — запрос `SELECT name FROM sqlite_master ORDER BY name`.
- **Columns (QComboBox) → Tab3** — вывод выбранной колонки (`type`, `name`, `tbl_name`, `rootpage` или `sql`) из `sqlite_master`.
- **bt2 «Query2» → Tab4** — количество объектов базы по типам (`table`, `index`, `view` и др.).
- **bt3 «Query3» → Tab5** — список пользовательских таблиц и SQL-команд их создания.

Таблицы доступны только для просмотра. Пока соединение не установлено, кнопки и список колонок неактивны.

## Скриншоты

`DatabaseManager` из `database.py` открывает выбранный через `QFileDialog` файл с помощью `QSqlDatabase` и драйвера `QSQLITE`. После подключения `MainWindow` выполняет SQL-запрос и помещает его результат в `QSqlQueryModel`, связанную с `QTableView` нужной вкладки. Кнопки подключены к обработчикам через сигнал `clicked.connect()`, а выбор поля — через `currentIndexChanged.connect()`. Перед закрытием соединения модели отвязываются от таблиц, чтобы освободить запросы.

### Tab1 — структура базы

![Tab1 — sqlite_master]

### Tab2 — имена объектов

![Tab2 — запрос SELECT name]

### Tab3 — выбранная колонка

![Tab3 — QComboBox]

### Tab4 — группировка объектов по типам

![Tab4 — Query2]

### Tab5 — пользовательские таблицы

![Tab5 — Query3]

## Вывод

В ходе лабораторной работы создано графическое приложение PyQt5 для подключения к базе данных SQLite, выполнения выборочных SQL-запросов и отображения их результатов в табличном виде. Изучены компоненты `QMainWindow`, `QFileDialog`, `QTabWidget`, `QComboBox`, `QTableView`, `QSqlDatabase` и `QSqlQueryModel`.
