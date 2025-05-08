"""
Phonebook project
"""

import logging
from tkinter import Toplevel, messagebox
from typing import List, Optional
import tkinter

logging.basicConfig(level=logging.INFO)


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
    
    def label(self):
        """
        Get the label to show in the phonebook.
        """
        return f"{self.first_name} {self.last_name}"


class ContactRepository:
    """
    Connect to storage for contacts.
    """

    def __init__(self):
        """
        Initialize the storage for contacts.
        """
        pass

    def append(self, c: Contact) -> Contact:
        raise NotImplementedError()

    def items(self) -> List[Contact]:
        raise NotImplementedError()

    def pop(self, id: int) -> Contact:
        raise NotImplementedError()

    def get(self, id: int) -> Contact:
        raise NotImplementedError()

    def set(self, id: int, c: Contact) -> Contact:
        raise NotImplementedError()


class ContactMemoryStorage(ContactRepository):
    """
    Save contacts in the local memory.
    """

    phonebook: List[Contact] = [Contact("1234")]

    def __init__(self):
        super().__init__()

    def append(self, c: Contact) -> Contact:
        self.phonebook.append(c)
        return self.phonebook.index(c)

    def items(self) -> List[Contact]:
        return self.phonebook

    def pop(self, id: int) -> Contact:
        return self.phonebook.pop(id)

    def get(self, id: int) -> Contact:
        return self.phonebook[id]

    def set(self, id: int, c: Contact) -> Contact:
        self.phonebook[id] = c



phonebook: ContactRepository = ContactMemoryStorage()


class DetailContactWindow:
    """
    Show details of a contact. Used to change info too.
    """

    root: tkinter.Toplevel
    """
    The window where you create this one.
    """

    contact: Contact
    """
    The contact to be created or modified.
    """

    def control(self, root, text: str, row: int):
        """
        Create a new control to be placed in the grid.
        """
        tkinter.Label(root, text=text).grid(row=row, column=0, padx=5, pady=5)
        ent = tkinter.Entry(root)
        ent.grid(row=row, column=1, columnspan=2, padx=5, pady=5)
        return ent

    def __init__(self, root: tkinter.Toplevel, id: Optional[int] = None):
        """
        Initialize the window, showing info about contact if passed as param.
        """
        self.id = id
        self.contact = Contact() if id is None else phonebook.get(id)
        logging.info(f"Ho caricato il contatto {self.contact.first_name} a {self.id}")

        self.root = root
        root.title("Nuovo contatto")

        self.ent_firstname = self.control(root, "Nome > ", 0)
        self.ent_firstname.insert(0, self.contact.first_name)
        
        self.ent_lastname = self.control(root, "Cognome > ", 1)
        self.ent_lastname.insert(0, self.contact.last_name)

        self.ent_telephone = self.control(root, "Tel > ", 1)
        self.ent_telephone.insert(0, self.contact.telephone)

        self.ent_address = self.control(root, "Indirizzo > ", 1)
        self.ent_address.insert(0, self.contact.address)

        self.ent_age = self.control(root, "Età > ", 1)
        given_age = self.contact.age or ''
        logging.info(f"Given age is {given_age}")
        self.ent_age.insert(0, given_age)

        # Controlli
        self.add_btn = tkinter.Button(root, text="Salva", command=self.create_contact)
        self.add_btn.grid(row=5, column=0, padx=5, pady=5)

        self.delete_btn = tkinter.Button(root, text="Annulla", command=self.cancel)
        self.delete_btn.grid(row=5, column=1, padx=5, pady=5)

    def create_contact(self):
        """
        Create a new contact and append to the phonebook.
        """
        firstname = self.ent_firstname.get().strip()
        lastname = self.ent_lastname.get().strip()
        telephone = self.ent_telephone.get().strip()
        address = self.ent_address.get().strip()
        age = int(self.ent_age.get().strip())
        if self.id:
            # It's an existing contact
            self.contact.first_name = firstname
            self.contact.last_name = lastname
            self.contact.telephone = telephone
            self.contact.address = address
            self.contact.age = age
            phonebook.set(self.id, self.contact)
        elif new := Contact(firstname, lastname, address, telephone, age):
            # It's a new contact
            phonebook.append(new)
        else:
            messagebox.showwarning("Errore", "Controlla i campi che vuoi inserire.")

        self.root.destroy()

    def cancel(self):
        """
        Close the window without doing anything.
        """
        logging.info("Creation canceled")
        self.root.destroy()

    def reset(self):
        """
        Reset the status of the window.
        """
        self.ent_firstname.delete(0, tkinter.END)
        self.ent_lastname.delete(0, tkinter.END)
        self.ent_telephone.delete(0, tkinter.END)
        self.ent_address.delete(0, tkinter.END)
        self.ent_age.delete(0, tkinter.END)


class App:
    """
    The main application for tkinter.
    """

    def __init__(self, root: tkinter.Tk):
        self.root = root
        self.root.title("Phonebook")

        # Tabella
        self.table = tkinter.Listbox(root, width=50)
        self.table.grid(row=5, column=0, columnspan=3, padx=10, pady=5)

        # Controlli
        self.btn_add = tkinter.Button(root, text="Nuovo", command=self.new_contact)
        self.btn_add.grid(row=4, column=0, padx=5, pady=5)

        self.btn_update = tkinter.Button(
            root, text="Modifica", command=self.update_contact
        )
        self.btn_update.grid(row=4, column=1, padx=5, pady=5)

        self.btn_delete = tkinter.Button(
            root, text="Elimina", command=self.delete_contact
        )
        self.btn_delete.grid(row=4, column=2, padx=5, pady=5)

        self.update_phonelist()

    def new_contact(self):
        top_create = Toplevel(self.root)
        top_create.bind("<Destroy>", lambda e: self.update_phonelist(e))
        DetailContactWindow(top_create)

    def update_contact(self):
        """
        Try to open a window with details to update.
        """
        if selected := self.table.curselection():
            top_update = Toplevel(self.root)
            top_update.bind("<Destroy>", lambda e: self.update_phonelist(e))
            i = selected[0]
            DetailContactWindow(top_update, i)
        else:
            messagebox.showerror(
                "Errore", "Devi prima selezionare un contatto da modificare"
            )

    def delete_contact(self):
        if selected := self.table.curselection():
            i = selected[0]
            elem = phonebook.get(i)
            if messagebox.askyesno(
                "Cancella contatto",
                f"Sei sicuro di voler cancellare il contatto {elem.label()}?",
            ):
                destroyed = phonebook.pop(i)
                logging.info(f"Destroyed {destroyed.first_name} at {i}")
                self.update_phonelist()
        else:
            messagebox.showwarning(
                "Errore", "Seleziona almeno un contatto da eliminare."
            )

    def update_phonelist(self, e=None):
        """
        All contacts in the phonebook are listed in the table.
        """
        if e:
            logging.info("Qualcosa è arrivato: %s", str(e))

        self.table.delete(0, tkinter.END)
        for c in phonebook.items():
            self.table.insert(tkinter.END, f"{c.label()}")

        logging.info("Updated phonelist")


if __name__ == "__main__":
    widget = tkinter.Tk()
    App(widget)
    widget.mainloop()
