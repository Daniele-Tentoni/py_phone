import tkinter


def control(root, text: str, row: int):
    """
    Create a new control to be placed in the grid.
    """
    tkinter.Label(root, text=text).grid(row=row, column=0, padx=5, pady=5)
    ent = tkinter.Entry(root)
    ent.grid(row=row, column=1, columnspan=2, padx=5, pady=5)
    return ent
