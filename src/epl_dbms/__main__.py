"""Launch the English Premier League database user interface."""

import tkinter as tk

from epl_dbms.settings import OracleSettings
from epl_dbms.ui.clubs_window import ClubsWindow


def main() -> None:
    try:
        settings = OracleSettings.from_environment()
    except ValueError as error:
        raise SystemExit(f"Oracle configuration error: {error}") from error

    root = tk.Tk()
    ClubsWindow(root, settings)
    root.mainloop()


if __name__ == "__main__":
    main()
