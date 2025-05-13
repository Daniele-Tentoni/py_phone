import tkinter

from py_phone.service.authentication_service import AuthenticationService
from py_phone.utils import control


class LoginWindow:
    def __init__(self, root: tkinter.Toplevel):
        self.root = root
        self.root.title("Login")

        self.ent_username = control(root, "Username > ", 0)
        self.ent_password = control(root, "Password > ", 1)

        self.login_button = tkinter.Button(
            root, text="Login", command=self.login_command
        )
        self.login_button.grid(row=2, column=1, padx=5, pady=5)

        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def login_command(self):
        username = self.ent_username.get().strip()
        password = self.ent_password.get().strip()
        self.success = AuthenticationService().login(username, password)
        self.root.destroy()

    def close(self):
        self.success = False
        self.root.destroy()
