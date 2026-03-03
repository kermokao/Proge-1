"""Course class with name and grades."""


class Course:
    """,."""
    def __init__(self, name: str):
        """,."""
        self._name = name
        self._grades = []

    def add_grade(self, student, grade: int):
        """,."""
        self._grades.append((student, grade))

    def get_grades(self) -> list[tuple["Student", int]]:
        """,."""
        return self._grades.copy()

    def get_average_grade(self) -> float:
        """,."""
        if len(self._grades) == 0:
            return -1
        else:
            return sum(grade for _, grade in self._grades) / len(self._grades)

    def __repr__(self):
        """,."""
        return self._name
