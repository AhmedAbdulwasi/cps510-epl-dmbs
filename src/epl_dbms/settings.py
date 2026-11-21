import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class OracleSettings:
    user: str
    password: str
    dsn: str

    @classmethod
    def from_environment(cls) -> "OracleSettings":
        values = {
            "ORACLE_USER": os.environ.get("ORACLE_USER"),
            "ORACLE_PASSWORD": os.environ.get("ORACLE_PASSWORD"),
            "ORACLE_DSN": os.environ.get("ORACLE_DSN"),
        }
        missing = [
            name
            for name, value in values.items()
            if value is None or not value.strip()
        ]
        if missing:
            raise ValueError(
                "Set the following environment variable(s): "
                + ", ".join(missing)
            )

        return cls(
            user=values["ORACLE_USER"] or "",
            password=values["ORACLE_PASSWORD"] or "",
            dsn=values["ORACLE_DSN"] or "",
        )
