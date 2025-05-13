import logging
from tkinter import messagebox
import tkinter
from typing import Optional

from py_phone.model.contact import Contact
from py_phone.repository.contact_repository import ContactRepository
from py_phone.utils import control


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

    def __init__(
        self,
        root: tkinter.Toplevel,
        phonebook: ContactRepository,
        id: Optional[int] = None,
    ):
        """
        Initialize the window, showing info about contact if passed as param.
        """
        self.id = id
        self.phonebook = phonebook
        self.contact = Contact() if id is None else self.phonebook.get(id)
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
            self.phonebook.set(self.id, self.contact)
        elif new := Contact(firstname, lastname, address, telephone, age):
            # It's a new contact
            self.phonebook.append(new)
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
