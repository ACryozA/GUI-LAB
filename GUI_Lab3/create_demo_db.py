from pathlib import Path
import sqlite3


BASE_DIR = Path(__file__).resolve().parent
DB_FILE = BASE_DIR / "demo.db"


def main():
    if DB_FILE.exists():
        print(f"Файл уже существует: {DB_FILE}. Данные не перезаписаны.")
        return

    with sqlite3.connect(DB_FILE) as conn:
        conn.executescript("""
            CREATE TABLE students (
                id INTEGER PRIMARY KEY,
                full_name TEXT NOT NULL,
                study_group TEXT NOT NULL
            );
            CREATE TABLE subjects (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                hours INTEGER NOT NULL
            );
            CREATE TABLE grades (
                student_id INTEGER NOT NULL,
                subject_id INTEGER NOT NULL,
                grade INTEGER NOT NULL,
                FOREIGN KEY(student_id) REFERENCES students(id),
                FOREIGN KEY(subject_id) REFERENCES subjects(id)
            );
            CREATE INDEX idx_students_group ON students(study_group);
            CREATE VIEW student_count_by_group AS
                SELECT study_group, COUNT(*) AS students_total
                FROM students GROUP BY study_group;
            INSERT INTO students (full_name, study_group) VALUES
                ('Иван Петров', 'М-21'),
                ('Анна Смирнова', 'М-21'),
                ('Мария Соколова', 'М-22');
            INSERT INTO subjects (title, hours) VALUES
                ('Графический интерфейс', 72),
                ('Базы данных', 54);
            INSERT INTO grades (student_id, subject_id, grade) VALUES
                (1, 1, 5), (2, 1, 4), (3, 2, 5);
        """)
    print(f"Учебная база данных создана: {DB_FILE}")


if __name__ == "__main__":
    main()
