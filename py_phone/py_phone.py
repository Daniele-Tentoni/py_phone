"""
Phonebook project
"""

from argparse import ArgumentParser
import logging
import sys
from tkinter import Event, Toplevel, messagebox
from typing import Optional
import tkinter

from py_phone.repository.contact_folder_repository import ContactFolderRepository
from py_phone.repository.contact_memory_repository import ContactMemoryRepository
from py_phone.repository.contact_repository import ContactRepository
from py_phone.repository.contact_file_repository import ContactFileRepository
from py_phone.windows.details_window import DetailContactWindow
from py_phone.windows.login_window import LoginWindow

logging.basicConfig(level=logging.INFO)


class App:
    """
    The main application for tkinter.
    """

    def __init__(self, root: tkinter.Tk, phonebook: ContactRepository):
        self.root = root
        self.root.title("Phonebook")

        self.phonebook = phonebook

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
        top_create.bind("<Destroy>", lambda e: self.update_phonelist(e))
        DetailContactWindow(top_create, self.phonebook)

    def update_contact(self):
        """
        Try to open a window with details to update.
        """
        if selected := self.table.curselection():
            top_update = Toplevel(self.root)
            top_update.bind("<Destroy>", lambda e: self.update_phonelist(e))
            i = selected[0]
            DetailContactWindow(top_update, self.phonebook, i)
        else:
            messagebox.showerror(
                "Errore", "Devi prima selezionare un contatto da modificare"
            )

    def delete_contact(self):
        if selected := self.table.curselection():
            i = selected[0]
            elem = self.phonebook.get(i)
            if messagebox.askyesno(
                "Cancella contatto",
                f"Sei sicuro di voler cancellare il contatto {elem.label()}?",
            ):
                destroyed = self.phonebook.pop(i)
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
        for c in self.phonebook.items():
            self.table.insert(tkinter.END, f"{c.label()}")


def main():
    sources = {
        "mem": ContactMemoryRepository,
        "file": ContactFileRepository,
        "folder": ContactFolderRepository,
        "db": ContactRepository,
    }
    if len(sources) < 1:
        logging.error("There are no repositories configured for phonebook")
        sys.exit()

    parser = ArgumentParser(description="Turing phonebook application")
    parser.add_argument(
        "source",
        choices=[x for x in sources.keys()],
        help="Fonte dei dati per la rubrica",
        nargs="?",
        default="mem",
    )
    arg = parser.parse_args()
    logging.info(f"Using {arg.source} as source for the phonebook")
    phonebook: ContactRepository = sources.get(str(arg.source))()

    widget = tkinter.Tk()
    widget.withdraw()
    top_login = tkinter.Toplevel(widget)
    login_window = LoginWindow(top_login)
    widget.wait_window(top_login)
    if login_window.success:
        widget.deiconify()
        App(widget, phonebook)
        widget.mainloop()
    else:
        messagebox.showerror("Error", "Your login as failed, restart the app")

    logging.info("I'm going to close the application")


if __name__ == "__main__":
    main()
