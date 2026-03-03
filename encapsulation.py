"""Module defining the Student class with encapsulated attributes."""


class Student:
    """Represent a student with a name, ID, and status."""

    def __init__(self, name, id):
        """Initialize a new Student with a name, ID, and default status."""
        self.__name = name
        self.__id = id
        self.__status = "Active"

    def get_id(self):
        """Initialize a new Student with a name, ID, and default status."""
        return self.__id

    def set_name(self, name):
        """Initialize a new Student with a name, ID, and default status."""
        self.__name = name

    def get_name(self):
        """Initialize a new Student with a name, ID, and default status."""
        return self.__name

    def set_status(self, status):
        """Initialize a new Student with a name, ID, and default status."""
        allowed_status = {"Active", "Expelled", "Finished", "Inactive"}
        if status in allowed_status:
            self.__status = status

    def get_status(self):
        """Initialize a new Student with a name, ID, and default status."""
        return self.__status
