from typing import TYPE_CHECKING

from langinfra.services.factory import ServiceFactory
from langinfra.services.socket.service import SocketIOService

if TYPE_CHECKING:
    from langinfra.services.cache.service import CacheService


class SocketIOFactory(ServiceFactory):
    def __init__(self) -> None:
        super().__init__(
            service_class=SocketIOService,
        )

    def create(self, cache_service: "CacheService"):
        return SocketIOService(cache_service)
