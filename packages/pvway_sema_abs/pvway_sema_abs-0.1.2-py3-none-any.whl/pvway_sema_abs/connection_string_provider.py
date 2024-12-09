from typing import Protocol

from src.pvway_sema_abs.sql_role_enu import SqlRoleEnu

class ConnectionStringProvider(Protocol):
    async def get_connection_string_async(
            self,
            role: SqlRoleEnu = SqlRoleEnu.APPLICATION) -> str:
        pass

class DefaultConnectionStringProvider(ConnectionStringProvider):
    def __init__(self, cs: str) -> None:
        self.cs = cs

    async def get_connection_string_async(
            self,
            role: SqlRoleEnu = SqlRoleEnu.APPLICATION) -> str:
        return self.cs
