from __future__ import annotations

from typing import TYPE_CHECKING

from langinfra.services.factory import ServiceFactory
from langinfra.services.telemetry.service import TelemetryService

if TYPE_CHECKING:
    from langinfra.services.settings.service import SettingsService


class TelemetryServiceFactory(ServiceFactory):
    def __init__(self) -> None:
        super().__init__(TelemetryService)

    def create(self, settings_service: SettingsService):
        return TelemetryService(settings_service)
