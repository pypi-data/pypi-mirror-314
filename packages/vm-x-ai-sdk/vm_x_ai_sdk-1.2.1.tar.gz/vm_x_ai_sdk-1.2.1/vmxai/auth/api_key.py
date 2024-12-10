from typing import TYPE_CHECKING

from vmxai.auth.provider import VMXClientAuthProvider

if TYPE_CHECKING:
    from vmxai.client import VMXClient


class VMXClientAPIKey(VMXClientAuthProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def inject_credentials(self, client: "VMXClient", grpc_metadata: list[tuple[str, str]]) -> tuple[tuple[str, str]]:
        grpc_metadata.append(("x-api-key", self.api_key))
        return grpc_metadata
