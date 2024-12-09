from typing import TYPE_CHECKING

from langinfra.services.factory import ServiceFactory
from langinfra.services.session.service import SessionService

if TYPE_CHECKING:
    from langinfra.services.cache.service import CacheService


class SessionServiceFactory(ServiceFactory):
    def __init__(self) -> None:
        super().__init__(SessionService)

    def create(self, cache_service: "CacheService"):
        return SessionService(cache_service)
