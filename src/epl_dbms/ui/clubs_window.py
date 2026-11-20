"""Tkinter window for browsing the Clubs table."""

import tkinter as tk
from tkinter import messagebox, ttk

import oracledb

from epl_dbms.repositories.clubs import CLUB_COLUMNS, fetch_clubs
from epl_dbms.settings import OracleSettings


class ClubsWindow:
    def __init__(self, root: tk.Tk, settings: OracleSettings) -> None:
        self._root = root
        self._settings = settings
        self._root.title("CPS510 English Premier League - Clubs")
        self._root.geometry("980x520")
        self._root.minsize(720, 360)

        toolbar = ttk.Frame(root, padding=(12, 12, 12, 4))
        toolbar.pack(fill=tk.X)
        ttk.Label(toolbar, text="Clubs", font=("TkDefaultFont", 16, "bold")).pack(
            side=tk.LEFT
        )
        ttk.Button(toolbar, text="Refresh", command=self.refresh).pack(
            side=tk.RIGHT
        )

        content = ttk.Frame(root, padding=(12, 4, 12, 8))
        content.pack(fill=tk.BOTH, expand=True)
        self._tree = ttk.Treeview(
            content,
            columns=CLUB_COLUMNS,
            show="headings",
        )
        for column in CLUB_COLUMNS:
            self._tree.heading(column, text=column.replace("_", " "))
            self._tree.column(column, width=140, minwidth=80, anchor=tk.W)

        vertical_scrollbar = ttk.Scrollbar(
            content,
            orient=tk.VERTICAL,
            command=self._tree.yview,
        )
        horizontal_scrollbar = ttk.Scrollbar(
            content,
            orient=tk.HORIZONTAL,
            command=self._tree.xview,
        )
        self._tree.configure(
            yscrollcommand=vertical_scrollbar.set,
            xscrollcommand=horizontal_scrollbar.set,
        )
        self._tree.grid(row=0, column=0, sticky="nsew")
        vertical_scrollbar.grid(row=0, column=1, sticky="ns")
        horizontal_scrollbar.grid(row=1, column=0, sticky="ew")
        content.rowconfigure(0, weight=1)
        content.columnconfigure(0, weight=1)

        self._status = tk.StringVar(value="Loading Clubs...")
        ttk.Label(root, textvariable=self._status, padding=(12, 4)).pack(
            fill=tk.X
        )
        self.refresh()

    def refresh(self) -> None:
        try:
            rows = fetch_clubs(self._settings)
        except oracledb.Error as error:
            self._status.set("Could not load Clubs.")
            messagebox.showerror(
                "Oracle database error",
                f"Could not load the Clubs table:\n\n{error}",
                parent=self._root,
            )
            return

        self._tree.delete(*self._tree.get_children())
        for row in rows:
            self._tree.insert(
                "",
                tk.END,
                values=tuple("" if value is None else str(value) for value in row),
            )
        self._status.set(f"{len(rows)} club(s) loaded.")
