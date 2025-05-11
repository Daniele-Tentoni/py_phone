from typing import Optional


class Contact:
    """
    The information about a person in the phonebook.
    """

    first_name: str
    """
    The first name of the person registered.
    """

    def __init__(
        self,
        first_name: str = "",
        last_name: str = "",
        address: str = "",
        telephone: str = "",
        age: Optional[int] = None,
    ):
        """
        Initialize a new contact with basic info.
        """
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.telephone = telephone
        self.age = age

    def __repr__(self):
        return f'Contact("{self.first_name}", "{self.last_name}", "{self.address}", "{self.telephone}", {self.age})'

    def label(self):
        """
        Get the label to show in the phonebook.
        """
        return f"{self.first_name} {self.last_name}"
