class AuthenticationService:
    """
    Expose functionalities about authentication and authorization to the system.
    """

    def __init__(self):
        self.username = "phone"
        self.password = "admin"

    def login(self, username: str, password: str) -> bool:
        """
        Attempt a login to the system.

        :param username: Username to test
        :type username: str
        :param password: Password to test
        :type password: str
        :return: True if login as success, false otherwise.
        :rtype: bool
        """
        return self.username == username and self.password == password
