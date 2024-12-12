from pydantic import BaseModel
from pydantic import BaseModel, Field, schema, validator
from typing import List

class PaginationResponseModel(BaseModel):
    total_rows: int
    page: int
    page_size: int
    is_first_page: bool
    is_last_page: bool


class ExternalCategoryModel(BaseModel):
    external_id: str
    name: str
    parent_category: str
    preview_url: str


class CategoryModel(ExternalCategoryModel):
    name: str
    parent_category: str = ''
    preview_url: str = ''

    @validator('name')
    def not_empty_string(cls, value):
        if not value:
            raise ValueError('Name cannot be an empty string.')
        return value
    

class CategoryResponseModel(BaseModel):
    id: str
    name: str
    parent_category: str
    preview_url: str

    # TODO: add bitrix category id here
    external_id: str = None

class CategoryListResponseModel(BaseModel):
    categories: List[CategoryResponseModel]
    page_info: PaginationResponseModel