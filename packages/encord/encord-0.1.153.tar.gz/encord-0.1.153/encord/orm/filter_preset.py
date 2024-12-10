import uuid
from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID

from encord.orm.base_dto import BaseDTO, Field, dto_validator


class GetPresetParams(BaseDTO):
    top_level_folder_uuid: Optional[UUID] = Field(default=None, alias="topLevelFolderUuid")
    preset_uuids: Optional[List[UUID]] = Field(default=[], alias="uuids")
    page_token: Optional[str] = Field(default=None, alias="pageToken")
    page_size: Optional[int] = Field(default=None, alias="pageSize")


class FilterPreset(BaseDTO):
    uuid: uuid.UUID
    name: str
    description: Optional[str]
    created_at: Optional[datetime] = Field(default=None, alias="createdAt")
    last_updated_at: Optional[datetime] = Field(default=None, alias="lastUpdatedAt")


class FilterDefinition(BaseDTO):
    filters: List[Dict] = Field(default_factory=list)


class FilterPresetDefinition(BaseDTO):
    local_filters: Dict[str, FilterDefinition] = Field(
        default_factory=lambda: {str(uuid.UUID(int=0)): FilterDefinition()}, alias="local_filters"
    )
    global_filters: FilterDefinition = Field(default_factory=FilterDefinition, alias="global_filters")

    @dto_validator(mode="after")
    def check_not_empty(cls, self):
        if len(self.global_filters.filters) == 0 and all(
            [len(value.filters) == 0 for value in self.local_filters.values()]
        ):
            raise ValueError("FilterPresetDefinition definition must contain at least one global or local filter.")

        return self


class GetPresetsResponse(BaseDTO):
    results: List[FilterPreset]


class CreatePresetParams(BaseDTO):
    top_level_folder_uuid: UUID = Field(default=UUID(int=0), alias="topLevelFolderUuid")


class CreatePresetPayload(BaseDTO):
    name: str
    description: Optional[str] = ""
    filter_preset_json: Dict


class UpdatePresetPayload(BaseDTO):
    name: Optional[str] = None
    description: Optional[str] = None
    filter_preset: Optional[FilterPresetDefinition] = None
