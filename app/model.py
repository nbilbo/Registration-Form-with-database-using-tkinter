import sqlite3
import typing


class Model:
    """
    Model layer.
    Offers operations for querying and manipulating records.
    """

    def __init__(self, db_name: str = ':memory:') -> None:
        self.db_name = db_name
        self.create_tables()

    def create_tables(self) -> None:
        with sqlite3.connect(self.db_name) as conn:
            conn.execute(
                """
                create table if not exists student (
                idstudent integer primary key autoincrement,
                name text not null,
                email text unique,
                sex text,
                branch text,
                programming text
                );
                """
            )

    def insert_student(
        self,
        name: typing.Optional[str],
        email: typing.Optional[str],
        sex: typing.Optional[str],
        branch: typing.Optional[str],
        programming: typing.Optional[str],
    ) -> int:
        with sqlite3.connect(self.db_name) as conn:
            sql = 'insert into student \
            (name, email, sex, branch, programming) \
            values (?, ?, ?, ?, ?)'
            parameters = (name, email, sex, branch, programming)
            result = conn.execute(sql, parameters)
            return result.lastrowid

    def delete_student(self, primary_key: int) -> None:
        with sqlite3.connect(self.db_name) as conn:
            sql = 'delete from student where idstudent=?'
            parameters = (primary_key,)
            conn.execute(sql, parameters)

    def update_student(
        self,
        primary_key: int,
        name: typing.Optional[str],
        email: typing.Optional[str],
        sex: typing.Optional[str],
        branch: typing.Optional[str],
        programming: typing.Optional[str],
    ) -> None:
        with sqlite3.connect(self.db_name) as conn:
            sql = 'update student set name=?, email=?, sex=?, branch=?, \
            programming=? where idstudent=?'
            parameters = (name, email, sex, branch, programming, primary_key)
            conn.execute(sql, parameters)

    def select_students(self) -> typing.List:
        with sqlite3.connect(self.db_name) as conn:
            sql = 'select * from student'
            result = conn.execute(sql)
            return result.fetchall()

    def select_student_by_email(
        self, email: typing.Optional[str]
    ) -> typing.Optional[typing.Tuple]:
        with sqlite3.connect(self.db_name) as conn:
            sql = 'select * from student where email=?'
            parameters = (email,)
            result = conn.execute(sql, parameters)
            return result.fetchone()

    def select_student_by_primary_key(
        self, primary_key: int
    ) -> typing.Optional[typing.Tuple]:
        with sqlite3.connect(self.db_name) as conn:
            sql = 'select * from student where idstudent = ?'
            parameters = (primary_key,)
            result = conn.execute(sql, parameters)
            return result.fetchone()
