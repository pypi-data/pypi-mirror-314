from typing import TYPE_CHECKING

from langinfra.services.factory import ServiceFactory
from langinfra.services.shared_component_cache.service import SharedComponentCacheService

if TYPE_CHECKING:
    from langinfra.services.settings.service import SettingsService


class SharedComponentCacheServiceFactory(ServiceFactory):
    def __init__(self) -> None:
        super().__init__(SharedComponentCacheService)

    def create(self, settings_service: "SettingsService"):
        return SharedComponentCacheService(expiration_time=settings_service.settings.cache_expire)
