"""
Phonebook project
"""

import logging
from tkinter import Event, Toplevel, messagebox
from typing import Optional
import tkinter

from py_phone.model.contact import Contact
from py_phone.repository.contact_folder_repository import ContactFolderRepository
from py_phone.repository.contact_memory_repository import ContactMemoryRepository
from py_phone.repository.contact_repository import ContactRepository
from py_phone.repository.contact_file_repository import ContactFileRepository

logging.basicConfig(level=logging.INFO)


phonebook: ContactRepository = ContactFolderRepository()


def control(root, text: str, row: int):
    """
    Create a new control to be placed in the grid.
    """
    tkinter.Label(root, text=text).grid(row=row, column=0, padx=5, pady=5)
    ent = tkinter.Entry(root)
    ent.grid(row=row, column=1, columnspan=2, padx=5, pady=5)
    return ent


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

    def validate_age(self):
        age = self.ent_age.get()
        logging.debug(f"Validating age using {age} as value")
        if age:
            if age.isdigit() and int(age) in range(0, 200):
                self.lbl_error.config(text="Age control is ok")
                return True
            self.lbl_error.config(text="Age is not a number")
            return False
        self.lbl_error.config(text="Age is not given")
        return False

    def __init__(self, root: tkinter.Toplevel, id: Optional[int] = None):
        """
        Initialize the window, showing info about contact if passed as param.
        """
        self.id = id
        self.contact = Contact() if id is None else phonebook.get(id)
        logging.info(f"Ho caricato il contatto {self.contact.first_name} a {self.id}")

        self.root = root
        root.title("Nuovo contatto")

        self.ent_firstname = control(root, "Nome > ", 0)
        self.ent_firstname.insert(0, self.contact.first_name)

        self.ent_lastname = control(root, "Cognome > ", 1)
        self.ent_lastname.insert(0, self.contact.last_name)

        self.ent_telephone = control(root, "Tel > ", 2)
        self.ent_telephone.insert(0, self.contact.telephone)

        self.ent_address = control(root, "Indirizzo > ", 3)
        self.ent_address.insert(0, self.contact.address)

        self.ent_age = control(root, "Età > ", 4)
        given_age = self.contact.age or ""
        logging.info(f"Loading age {given_age} from {self.contact.age}.")
        self.ent_age.insert(0, given_age)
        self.ent_age.configure(validatecommand=self.validate_age, validate="focus")

        self.lbl_error = tkinter.Label(root, text="Error frame")
        self.lbl_error.grid(row=6, column=0, columnspan=3, padx=5, pady=5)

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
        try:
            age = int(self.ent_age.get().strip())
        except Exception as e:
            logging.error(f"Exception thrown from age conversion: {e}")
            messagebox.showerror("Errore", "Hai inserito una età non valida")

        if self.id is not None:
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

        self.update_phonelist(self.root)

    def new_contact(self):
        top_create = Toplevel(self.root)
        top_create.bind(
            "<Destroy>", lambda e: self.update_phonelist(e)
        )  # .protocol("WM_DELETE_WINDOW", )
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

    def update_phonelist(self, e: Optional[Event | Toplevel] = None):
        """
        All contacts in the phonebook are listed in the table.
        """
        if e:
            logging.info(f"Updated phonelist from {str(e)}")
            logging.debug("Event : %s", str(e))
            if isinstance(e, Toplevel):
                e.destroy()

            if isinstance(e, Event):
                if not isinstance(e.widget, Toplevel):
                    logging.debug(
                        "It's not a toplevel destroy event, we don't update phonelist"
                    )
                    return

        self.table.delete(0, tkinter.END)
        for c in phonebook.items():
            self.table.insert(tkinter.END, f"{c.label()}")


def main():
    widget = tkinter.Tk()
    App(widget)
    widget.mainloop()


if __name__ == "__main__":
    main()
