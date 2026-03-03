"""Student class with student name and grades."""

class Student:
    """,."""
    def __init__(self, name:str):
        """,."""
        self._name = name
        self._grades = []
        self._id =  None

    def set_id(self, id: int):
        """,."""
        if self._id is None:
            self._id = id

    def get_id(self):
        """,."""
        return self._id

    def add_grade(self, course, grade: int):
        """,."""
        self._grades.append((course, grade))

    def get_grades(self) -> list[tuple["Course", int]]:
        """,."""
        return self._grades.copy()

    def get_average_grade(self) -> float:
        """,."""
        if len(self._grades) == 0:
            return -1
        else:
            return sum(grade for _, grade in self._grades) / len(self._grades)

    def __repr__(self) -> str:
        """,."""
        return self._name
