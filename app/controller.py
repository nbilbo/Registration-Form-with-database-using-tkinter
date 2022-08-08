import sqlite3
import typing
from app import constants
from app.model import Model
if typing.TYPE_CHECKING:
    from app.view import View


class Controller:
    """
    Intermediate between the View and the Model.
    Uses the Model to perform queries, changes registers.
    Uses the  View to show registers and messages.
    """

    def __init__(self, view: 'View') -> None:
        self.model = Model(db_name=constants.DB_NAME)
        self.view = view

    def _format_output_student(
        self,
        primary_key: int,
        name: typing.Optional[str],
        email: typing.Optional[str],
        sex: typing.Optional[str],
        branch: typing.Optional[str],
        programming: typing.Optional[str],
    ) -> typing.Tuple:
        return (
            primary_key,
            name or '',
            email or '',
            sex or '',
            branch or '',
            programming or '',
        )

    def insert_student(
        self, name: str, email: str, sex: str, branch: str, programming: str
    ) -> None:
        formatted_name = name or None
        formatted_email = email or None
        formatted_sex = sex or None
        formatted_branch = branch or None
        formatted_programming = programming or None
        try:
            self.view.clear_form_feedback()
            self.model.insert_student(
                name=formatted_name,
                email=formatted_email,
                sex=formatted_sex,
                branch=formatted_branch,
                programming=formatted_programming,
            )
        except sqlite3.DatabaseError as error:
            warned = False
            if formatted_name is None:
                warned = True
                self.view.show_form_feedback('name', 'Required field')

            if formatted_email and self.model.select_student_by_email(
                formatted_email
            ):
                warned = True
                self.view.show_form_feedback('email', 'Email already exists.')

            if not warned:
                self.view.showwarning('error', str(error))
        else:
            self.view.clear_form_fields()
            self.view.form_display()
            self.view.showinfo('Success', f'Student has been registered.')

    def update_student(
        self,
        primary_key: int,
        name: str,
        email: str,
        sex: str,
        branch: str,
        programming: str,
    ) -> None:
        formatted_name = name or None
        formatted_email = email or None
        formatted_sex = sex or None
        formatted_branch = branch or None
        formatted_programming = programming or None
        if primary_key is None:
            self.view.showwarning('Wait', 'First select a register.')
        else:
            try:
                self.view.clear_form_feedback()
                self.model.update_student(
                    primary_key=primary_key,
                    name=formatted_name,
                    email=formatted_email,
                    sex=formatted_sex,
                    branch=formatted_branch,
                    programming=formatted_programming,
                )
            except sqlite3.DatabaseError as error:
                warned = False
                if formatted_name is None:
                    warned = True
                    self.view.show_form_feedback('name', 'Required field.')

                if formatted_email and self.model.select_student_by_email(
                    formatted_email
                ):
                    warned = True
                    self.view.show_form_feedback(
                        'email', 'Email already exists.'
                    )

                if not warned:
                    self.view.showwarning('error', str(error))
            else:
                self.view.form_display()
                self.view.clear_form_fields()
                self.view.showinfo('Success', 'Student has been updated.')

    def delete_student(self, primary_key: typing.Optional[int]) -> None:
        if primary_key:
            try:
                self.model.delete_student(primary_key)
                self.view.form_display()
                self.view.clear_form_fields()
                self.view.showinfo('Success', f'Student has been deleted.')
            except sqlite3.DatabaseError as error:
                self.view.showwarning('error', str(error))
        else:
            self.view.showwarning('Wait', f'First select a register.')

    def select_students(self) -> typing.List:
        students = []
        select_results = self.model.select_students()
        for result in select_results:
            register = self._format_output_student(
                primary_key=result[0],
                name=result[1],
                email=result[2],
                sex=result[3],
                branch=result[4],
                programming=result[5],
            )
            students.append(register)

        return students

    def select_student_by_primary_key(
        self, primary_key
    ) -> typing.Optional[typing.Tuple]:
        select_result = self.model.select_student_by_primary_key(primary_key)
        if select_result:
            return self._format_output_student(
                primary_key=select_result[0],
                name=select_result[1],
                email=select_result[2],
                sex=select_result[3],
                branch=select_result[4],
                programming=select_result[5],
            )
