import datetime
import logging
import os
from pathlib import Path
from typing import List
import uuid

from py_phone.model.contact import Contact
from py_phone.repository.contact_repository import ContactRepository


class ContactFolderFormatter:
    separator = "\n"

    def get(self, contact: Contact):
        """
        Convert a contact to a string.

        :param contact: contact to convert.
        :type contact: Contact

        >>> ContactFolderFormatter().get(Contact("primo", "secondo", "terzo", "quarto", 5))
        'primo\\nsecondo\\nterzo\\nquarto\\n5'
        """
        return self.separator.join([str(v) for v in list(vars(contact).values())])

    def set(self, string: List[str]):
        """
        Given the content of a contact file, return a contact cointained.

        :param file: file name to open.
        :type file: str


        >>> ContactFolderFormatter().set('primo\\nsecondo\\nterzo\\nquarto\\n5')
        Contact("primo", "secondo", "terzo", "quarto", 5)

        """
        logging.info(f"Extracting {string}")
        if len(string) < 5:
            raise ValueError("Given contact has less then 5 fields.")

        return Contact(
            string[0],
            string[1],
            string[2],
            string[3],
            int("".join(string[4].split())),
        )


class ContactFolderRepository(ContactRepository):
    """
    Save contacts in a file for each contact inside a phonebook folder.
    """

    def __init__(self):
        super().__init__()
        self.folder = "informazioni"
        if not os.path.isdir(self.folder):
            os.mkdir(self.folder)

    def list_files(self):
        """
        List all files in the folder. Does not sort them.
        """
        for f in os.listdir(self.folder):
            if os.path.isfile(os.path.join(self.folder, f)):
                yield f
    
    def sorted_files(self):
        names = [f for f in self.list_files()]
        logging.info(f"In the folder there are {len(names)} files = {names}.")
        names.sort(
            key=lambda f: os.path.getctime(os.path.join(self.folder, f)), reverse=True
        )
        return names

    def append(self, c):
        base_path = Path(self.folder)
        if base_path.is_dir():
            fullpath = Path(base_path, str(uuid.uuid4()))
            fullpath = fullpath.with_suffix(".txt")
            with open(fullpath, "w", encoding="utf-8") as w:
                file = ContactFolderFormatter().get(c)
                w.writelines(file)

            index = sum(1 for _ in self.list_files())
            logging.info(f"Folder length is {index}")

            return index

    def items(self):
        logging.info("Reading contact from folder")
        formatter = ContactFolderFormatter()
        base_path = Path(self.folder)
        if base_path.is_dir():
            names = self.sorted_files()

            try:
                if first := names[0]:
                    ct = os.path.getctime(os.path.join(base_path, first))
                    c = datetime.datetime.fromtimestamp(ct)
                    logging.info(
                        f"Last file created was {first} at {c}"
                    )
            except IndexError as i:
                logging.error(f"No items found in base folder {i}")

            for name in names:
                full_path = Path(base_path, name).with_suffix(".txt")
                if full_path.is_file():
                    with open(full_path, "r", encoding="utf-8") as r:
                        file_content = r.readlines()
                        logging.info(f"Reading {full_path} for {file_content}")
                        yield formatter.set(file_content)
                else:
                    logging.warning("Why it's not a file?")
                    

    def pop(self, id):
        base_path = Path(self.folder)
        if base_path.is_dir():
            files = [f for f in self.sorted_files()]
            if selected := files[id]:
                full_path = Path(base_path, selected).with_suffix(".txt")
                if full_path.is_file():
                    with open(full_path, "r", encoding="utf-8") as r:
                        c = ContactFolderFormatter().set(r.readlines())

                    full_path.unlink()
                    return c

            raise IndexError("Index out of bound exception or the file does not exists")

        raise ValueError("Missing base folder")

    def get(self, id):
        base_path = Path(self.folder)
        if base_path.is_dir():
            files = [f for f in self.sorted_files()]
            if selected := files[id]:
                full_path = Path(base_path, selected).with_suffix(".txt")
                with open(full_path, "r", encoding="utf-8") as r:
                    return ContactFolderFormatter().set(r.readlines())

    def set(self, id, c):
        base_path = Path(self.folder)
        if base_path.is_dir():
            files = [f for f in self.sorted_files()]
            if selected := files[id]:
                full_path = Path(base_path, selected).with_suffix(".txt")
                with open(full_path, "w", encoding="utf-8") as w:
                    string = ContactFolderFormatter().get(c)
                    w.writelines(string)
