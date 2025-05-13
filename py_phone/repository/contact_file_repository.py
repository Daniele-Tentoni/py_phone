import re
from typing import List
from py_phone.model.contact import Contact
from py_phone.repository.contact_repository import ContactRepository


import logging
import os


class ContactFileFormatter:
    """
    Provide utilities to convert a contact to a string and back. Use a default separator '~'.
    """

    separator = "~"

    def format(self, contact: Contact):
        return f"{contact.first_name}{self.separator}{contact.last_name}{self.separator}{contact.address}{self.separator}{contact.telephone}{self.separator}{contact.age}"

    def get(self, contact: Contact):
        """
        Convert a contact to a string.

        >>> ContactFileFormatter().get(Contact("primo", "secondo", "terzo", "quarto", 5))
        'primo~secondo~terzo~quarto~5'
        """
        return self.separator.join([str(v) for v in list(vars(contact).values())])

    def set(self, string: str):
        """
        Convert a string to a Contact.

        >>> ContactFileFormatter().set('primo~secondo~terzo~quarto~5')
        Contact("primo", "secondo", "terzo", "quarto", 5)

        >>> ContactFileFormatter().set('primo~secondo~terzo~quarto~5 5')
        Contact("primo", "secondo", "terzo", "quarto", 55)

        >>> ContactFileFormatter().set('primo~secondo~terzo~quarto~ 5 5 ')
        Contact("primo", "secondo", "terzo", "quarto", 55)
        """
        splitted = [re.sub("[\s+]", "", s) for s in string.split(self.separator)]
        if len(splitted) < 5:
            raise ValueError("Given contact have less then 5 fields.")

        return Contact(
            splitted[0],
            splitted[1],
            splitted[2],
            splitted[3],
            "".join(splitted[4].split()),
        )


class ContactFileRepository(ContactRepository):
    """
    Save contacts in a file.

    This doen't work well with big files in order of gigabytes.
    """

    def __init__(self):
        super().__init__()
        self.file = "informazioni.txt"
        # Look for file
        if not os.path.isfile(self.file):
            with open(self.file, "w", encoding="utf-8") as w:
                w.write("")

    def append(self, c: Contact):
        with open(self.file, "a+", encoding="utf-8") as a:
            line = ContactFileFormatter().format(c)
            a.writelines([line, "\n"])

        with open(self.file, "r", encoding="utf-8") as r:
            # Return the number of rows in a as identifier.
            index = sum(1 for _ in r) - 1
            logging.info(f"Appended contact {c.label()} at {index}")
            return index

    def items(self):
        logging.info("Reading items from file")
        formatter = ContactFileFormatter()
        with open(self.file, "r", encoding="utf-8") as r:
            for line in r.readlines():
                split = "".join(line.split())
                if len(split):
                    logging.info(f"Reading item line {split}:{len(split)}.")
                    try:
                        contact = formatter.set(split)
                        yield contact
                    except ValueError as v:
                        logging.error(f"Can't yield contact due to {v}")

    def pop(self, id):
        with open(self.file, "r", encoding="utf-8") as p:
            lines = p.readlines()

        if len(lines) < id:
            raise IndexError("Index out of bound error.")

        try:
            c = ContactFileFormatter().set(lines[id])
            del lines[id]

            self.write_all(lines)
            return c
        except Exception as e:
            logging.error(f"Error when popping contact {id} due to {e}")
            return None

    def get(self, id: int) -> Contact:
        logging.info(f"Want to read contact {id}")
        with open(self.file, "r+", encoding="utf-8") as r:
            lines = r.readlines()

        return ContactFileFormatter().set(lines[id])

    def set(self, id, c):
        with open(self.file, "r", encoding="utf-8") as r:
            lines = r.readlines()

        if len(lines) < id:
            raise IndexError("Index out of bound.")

        string = ContactFileFormatter().get(c)
        lines[id] = string + "\n"
        logging.info(f"Update row {id} using {string}")

        self.write_all(lines)

    def write_all(self, lines: List[str]) -> None:
        no_empty = [x for x in lines if len(x.split())]
        logging.info(f"Write all lines {len(no_empty)} of {len(lines)}.")
        with open(self.file, "w", encoding="utf-8") as w:
            w.writelines(no_empty)
