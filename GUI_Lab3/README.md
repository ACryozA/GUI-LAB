# Лабораторная работа №3 

## Выполнил студент группы 6231 Маслюк А.С.

### Цель

Реализовать приложение на PyQt5 с использованием `QTableView`, `QTabWidget`, `QComboBox`, `QFileDialog` и SQL-запросов к базе данных SQLite.

### Возможности

- **Menu → Set connection** — выбрать существующий файл базы данных `.db`, `.sqlite` или `.sqlite3` и открыть его.
- **Menu → Close connection** — закрыть соединение и очистить все пять вкладок.
- **Tab1** — после успешного подключения автоматически выводится `SELECT * FROM sqlite_master`.
- **bt1 «SELECT Column» → Tab2** — запрос `SELECT name FROM sqlite_master ORDER BY name`.
- **Columns (QComboBox) → Tab3** — вывод выбранной колонки (`type`, `name`, `tbl_name`, `rootpage` или `sql`) из `sqlite_master`.
- **bt2 «Query2» → Tab4** — количество объектов базы по типам (`table`, `index`, `view` и др.).
- **bt3 «Query3» → Tab5** — список пользовательских таблиц и SQL-команд их создания.

Таблицы доступны только для просмотра. Пока соединение не установлено, кнопки и список колонок неактивны.

### Результат работы программы

`DatabaseManager` из `database.py` открывает выбранный через `QFileDialog` файл с помощью `QSqlDatabase` и драйвера `QSQLITE`. После подключения `MainWindow` выполняет SQL-запрос и помещает его результат в `QSqlQueryModel`, связанную с `QTableView` нужной вкладки. Кнопки подключены к обработчикам через сигнал `clicked.connect()`, а выбор поля — через `currentIndexChanged.connect()`. Перед закрытием соединения модели отвязываются от таблиц, чтобы освободить запросы.

**<ins>1. Главное окно приложения</ins>**

После запуска программы отображается окно со всем основным функционалом

<img width="1100" height="701" alt="image" src="https://github.com/user-attachments/assets/ee17daf2-3d0d-4a23-914d-547191e78103" />

_Рисунок 1 - Главное окно приложения_

**<ins>2. Соединение с базой данных</ins>**

При нажатии кнопки `Menu` открывается список состоящий из двух кнопок: `Set connection`, которая позволяет установить связь с базой данных, и `Close connection`, которая позволяет разорвать связь с базой данных. 

<img width="525" height="462" alt="image" src="https://github.com/user-attachments/assets/d3a39f22-a1e2-42f8-9fd3-75125deb5bd0" />

_Рисунок 2 - Ввод суммы в долларах_

**<ins>3. Изменение суммы в евро</ins>**

Внесём сумму в 37 евро в соответсвующее поле ввода, получим результат конвертации в других полях

<img width="524" height="462" alt="image" src="https://github.com/user-attachments/assets/9790e76a-ab5a-4630-812f-0dfe0599be7b" />

_Рисунок 3 - Ввод суммы в евро_

**<ins>4. Изменение суммы в рублях</ins>**

Внесём сумму в 27000 рублей в соответсвующее поле ввода, получим результат конвертации в других полях

<img width="528" height="466" alt="image" src="https://github.com/user-attachments/assets/bfea8da9-01f6-477c-9df1-e1f70208cbc2" />

_Рисунок 4 - Ввод суммы в рублях_

**<ins>5. Сброс значений</ins>**

При нажатии кнопки "Сбросить значения" значения всех полей станут равны 0.00

<img width="529" height="466" alt="image" src="https://github.com/user-attachments/assets/cfb07323-719a-46bb-918a-3cf7be0d4922" />

_Рисунок 5 - Сброс значений во всех полях_


## Вывод

В ходе лабораторной работы создано графическое приложение PyQt5 для подключения к базе данных SQLite, выполнения выборочных SQL-запросов и отображения их результатов в табличном виде. Изучены компоненты `QMainWindow`, `QFileDialog`, `QTabWidget`, `QComboBox`, `QTableView`, `QSqlDatabase` и `QSqlQueryModel`.
