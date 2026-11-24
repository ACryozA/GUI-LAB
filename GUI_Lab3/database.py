from pathlib import Path
from uuid import uuid4

from PyQt5.QtSql import QSqlDatabase


class DatabaseManager:
    def __init__(self):
        self.connection_name = f"gui_lab3_{uuid4().hex}"
        self.db = None
        self.file_path = None

    @property
    def connected(self) -> bool:
        return self.db is not None and self.db.isOpen()

    def open(self, file_path: str):
    
        self.close()
        path = Path(file_path)
        if not path.is_file():
            return False, "Выбранный файл не существует."

        self.db = QSqlDatabase.addDatabase("QSQLITE", self.connection_name)
        self.db.setDatabaseName(str(path))

        if not self.db.open():
            error_text = self.db.lastError().text()
            self.close()
            return False, error_text

       
        from PyQt5.QtSql import QSqlQuery
        query = QSqlQuery(self.db)
        ok = query.exec_("SELECT name FROM sqlite_master LIMIT 1")
        if not ok:
            error_text = query.lastError().text()
            query = None  
            self.close()
            return False, error_text
        query = None

        self.file_path = str(path)
        return True, ""

    def close(self):
        if self.db is not None:
            self.db.close()
            self.db = None
            QSqlDatabase.removeDatabase(self.connection_name)
        self.file_path = None
