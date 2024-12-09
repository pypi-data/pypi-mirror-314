from __future__ import annotations

from typing import TYPE_CHECKING

from langinfra.services.factory import ServiceFactory
from langinfra.services.variable.service import DatabaseVariableService, VariableService

if TYPE_CHECKING:
    from langinfra.services.settings.service import SettingsService


class VariableServiceFactory(ServiceFactory):
    def __init__(self) -> None:
        super().__init__(VariableService)

    def create(self, settings_service: SettingsService):
        # here you would have logic to create and configure a VariableService
        # based on the settings_service

        if settings_service.settings.variable_store == "kubernetes":
            # Keep it here to avoid import errors
            from langinfra.services.variable.kubernetes import KubernetesSecretService

            return KubernetesSecretService(settings_service)
        return DatabaseVariableService(settings_service)
