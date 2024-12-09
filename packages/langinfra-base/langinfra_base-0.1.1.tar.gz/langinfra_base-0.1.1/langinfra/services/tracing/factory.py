from __future__ import annotations

from typing import TYPE_CHECKING

from langinfra.services.factory import ServiceFactory
from langinfra.services.tracing.service import TracingService

if TYPE_CHECKING:
    from langinfra.services.settings.service import SettingsService


class TracingServiceFactory(ServiceFactory):
    def __init__(self) -> None:
        super().__init__(TracingService)

    def create(self, settings_service: SettingsService):
        return TracingService(settings_service)
