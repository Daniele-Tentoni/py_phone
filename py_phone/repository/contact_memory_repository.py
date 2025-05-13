from py_phone.model.contact import Contact
from py_phone.repository.contact_repository import ContactRepository


import logging
from typing import List


class ContactMemoryRepository(ContactRepository):
    """
    Save contacts in the local memory.
    """

    phonebook: List[Contact] = [Contact("1234")]

    def __init__(self):
        super().__init__()

    def append(self, c: Contact) -> int:
        """
        >>> mem = ContactMemoryRepository()
        >>> mem.append(Contact("primo", "secondo", "terzo", "quarto", 5))
        1

        >>> len([x for x in mem.items()])
        2
        """
        self.phonebook.append(c)
        index = self.phonebook.index(c)
        logging.info(f"Appended contact {c.label()} at {index}")
        return index

    def items(self):
        for contact in self.phonebook:
            yield contact

    def pop(self, id: int) -> Contact:
        """
        >>> ContactMemoryRepository().pop(0)
        Contact("1234", "", "", "", None)
        """
        return self.phonebook.pop(id)

    def get(self, id: int) -> Contact:
        return self.phonebook[id]

    def set(self, id: int, c: Contact) -> Contact:
        self.phonebook[id] = c
