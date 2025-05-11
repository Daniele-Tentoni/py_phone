from py_phone.model.contact import Contact


class ContactRepository:
    """
    Connect to storage for contacts.
    """

    def __init__(self):
        """
        Initialize the storage for contacts.
        """
        pass

    def append(self, c: Contact) -> int:
        """
        Append a new contact to the end of the phonebook.

        :param c: Contact to save.
        :type c: Contact
        :return: Identifier of the contact.
        :rtype: int
        """
        raise NotImplementedError()

    def items(self):
        """
        Return a list of all items in the repository. In some implementations it may use iterators instead return the entire list at once.
        """
        raise NotImplementedError()

    def pop(self, id: int) -> Contact:
        """
        Remove the item with given id and return it.

        :param id: Identifier of the contact.
        :type id: int
        """
        raise NotImplementedError()

    def get(self, id: int) -> Contact:
        """
        Return an item from the list without remove it.

        :param id: Identifier of the contact.
        :type id: int
        """
        raise NotImplementedError()

    def set(self, id: int, c: Contact) -> Contact:
        """
        Update the contact given its id.

        If you don't have an identifier, look at the append method.

        :param id: Identifier of the contact.
        :type id: int
        :param c: Contact to save.
        :type c: Contact
        """
        raise NotImplementedError()
