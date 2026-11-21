import oracledb

from epl_dbms.settings import OracleSettings


def connect(settings: OracleSettings) -> oracledb.Connection:
    """Open an Oracle connection using python-oracledb Thin mode."""
    return oracledb.connect(
        user=settings.user,
        password=settings.password,
        dsn=settings.dsn,
    )
