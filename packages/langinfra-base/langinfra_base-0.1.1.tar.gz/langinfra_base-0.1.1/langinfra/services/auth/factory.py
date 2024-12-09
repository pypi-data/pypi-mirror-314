from langinfra.services.auth.service import AuthService
from langinfra.services.factory import ServiceFactory


class AuthServiceFactory(ServiceFactory):
    name = "auth_service"

    def __init__(self) -> None:
        super().__init__(AuthService)

    def create(self, settings_service):
        return AuthService(settings_service)
