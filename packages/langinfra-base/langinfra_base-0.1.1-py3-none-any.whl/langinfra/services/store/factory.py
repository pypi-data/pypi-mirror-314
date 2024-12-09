from __future__ import annotations

from typing import TYPE_CHECKING

from langinfra.services.factory import ServiceFactory
from langinfra.services.store.service import StoreService

if TYPE_CHECKING:
    from langinfra.services.settings.service import SettingsService


class StoreServiceFactory(ServiceFactory):
    def __init__(self) -> None:
        super().__init__(StoreService)

    def create(self, settings_service: SettingsService):
        return StoreService(settings_service)
