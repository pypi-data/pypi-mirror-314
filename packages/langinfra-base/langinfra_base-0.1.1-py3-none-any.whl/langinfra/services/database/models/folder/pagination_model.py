from fastapi_pagination import Page

from langinfra.helpers.base_model import BaseModel
from langinfra.services.database.models.flow.model import Flow
from langinfra.services.database.models.folder.model import FolderRead


class FolderWithPaginatedFlows(BaseModel):
    folder: FolderRead
    flows: Page[Flow]
