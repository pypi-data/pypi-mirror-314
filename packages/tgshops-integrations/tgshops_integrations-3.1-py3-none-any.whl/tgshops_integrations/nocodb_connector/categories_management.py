from typing import List
from loguru import logger
from aiocache import cached
from models.categories import CategoryModel, CategoryResponseModel, CategoryListResponseModel
from models.products import ProductModel
from tgshops_integrations.nocodb_connector.client import custom_key_builder, NocodbClient
from tgshops_integrations.nocodb_connector.model_mapping import (
    CATEGORY_IMAGE_FIELD,
    CATEGORY_NAME_FIELD,
    CATEGORY_PARENT_FIELD,
    CATEGORY_PARENT_ID_FIELD,
    PRODUCT_NAME_FIELD,
    CATEGORY_ID_OF_CATEGORY_FIELD,
    dump_category_data,
    get_pagination_info,
    parse_category_data,
)

class CategoryManager(NocodbClient):
    def __init__(
        self,
        table_id=None,
        logging=False,
        config_type=None,
        NOCODB_HOST=None,
        NOCODB_API_KEY=None,
        SOURCE=None,
        filter_buttons=None,
    ):
        super().__init__(NOCODB_HOST=NOCODB_HOST, NOCODB_API_KEY=NOCODB_API_KEY, SOURCE=SOURCE)
        self.NOCODB_HOST = NOCODB_HOST
        self.NOCODB_API_KEY = NOCODB_API_KEY
        self.SOURCE = SOURCE
        self.CONFIG_TYPE = config_type
        self.categories_table = table_id
        self.external_categories = {}
        self.logging = logging
        self.filter_categories = []
        self.filter_buttons = filter_buttons or []
        self.required_fields = [CATEGORY_NAME_FIELD]
        self.projection = ["Id", CATEGORY_NAME_FIELD, CATEGORY_PARENT_ID_FIELD, CATEGORY_ID_OF_CATEGORY_FIELD]

    @cached(ttl=30, key_builder=custom_key_builder)
    async def get_categories(self, table_id: str) -> List[CategoryModel]:
        records = await self.get_table_records(table_id, self.required_fields, self.projection)
        return [parse_category_data(record) for record in records]

    @cached(ttl=30, key_builder=custom_key_builder)
    async def get_categories_v2(self, table_id: str, offset: int = None, limit: int = None) -> CategoryListResponseModel:
        response = await self.get_table_records_v2(
            table_name=self.categories_table,
            required_fields=self.required_fields,
            projection=self.projection,
            offset=offset,
            limit=limit,
        )
        page_info = get_pagination_info(page_info=response['pageInfo'])
        categories = [parse_category_data(record) for record in response['list']]
        return CategoryListResponseModel(categories=categories, page_info=page_info)

    @cached(ttl=30, key_builder=custom_key_builder)
    async def get_category(self, table_id: str, category_id: str) -> CategoryModel:
        record = await self.get_table_record(self.categories_table, category_id, self.required_fields, self.projection)
        return parse_category_data(record)

    async def create_category(self, table_id: str, category: CategoryModel) -> CategoryModel:
        category_json = dump_category_data(category)
        record = await self.create_table_record(self.categories_table, category_json)
        return parse_category_data(record)

    @cached(ttl=30, key_builder=custom_key_builder)
    async def get_categories_in_category(self, table_id: str, category_id: str) -> List[CategoryModel]:
        extra_where = (
            f"({CATEGORY_PARENT_ID_FIELD},eq,{category_id})"
            if category_id
            else f"({CATEGORY_PARENT_FIELD},eq,0)"
        )
        records = await self.get_table_records(
            table_name=self.categories_table,
            required_fields=self.required_fields,
            projection=self.projection,
            extra_where=extra_where,
        )
        return [parse_category_data(record) for record in records]

    async def update_categories(self, external_products: List[ProductModel]) -> None:
        self.categories = await self.get_product_categories(table_id=self.categories_table, table_name=PRODUCT_NAME_FIELD)
        categories_list = list(self.categories.keys())
        properties_to_create = []

        for product in external_products:
            for num, product_property in enumerate(product.product_properties):
                if product_property not in categories_list:
                    parent_id = (
                        self.categories[self.filter_buttons[num]]
                        if self.filter_buttons
                        else self.categories[product.category_I_name[0]]
                    )
                    properties_to_create.append([product_property, parent_id])
                    categories_list.append(product_property)

        if properties_to_create:
            properties_to_create.sort(key=lambda x: x[0])
            new_id = max(self.categories.values(), default=0) + 1

            for product_property, parent_id in properties_to_create:
                new_property = await self.create_product_category(
                    table_id=self.categories_table,
                    property_name=product_property,
                    category_id=new_id,
                    table_name=PRODUCT_NAME_FIELD,
                )
                if self.logging:
                    logger.info(f"New Category: {new_property}")
                new_id += 1

    async def link_categories(self, parent_id: int, child_id: int):
        metadata = await self.get_table_meta(self.categories_table)
        linked_column = next((col for col in metadata['columns'] if col["title"] == "Set parent category" and col["uidt"] == "Links"), None)

        if linked_column:
            await self.link_table_record(
                linked_column["base_id"],
                linked_column["fk_model_id"],
                child_id,
                linked_column["id"],
                parent_id,
            )

    async def unlink_categories(self, parent_id: int, child_id: int):
        metadata = await self.get_table_meta(self.categories_table)
        linked_column = next((col for col in metadata['columns'] if col["uidt"] == "Links"), None)

        if linked_column:
            await self.unlink_table_record(
                linked_column["base_id"],
                linked_column["fk_model_id"],
                parent_id,
                linked_column["id"],
                child_id,
            )

    async def map_categories(self, external_products: List[ProductModel]) -> List[ProductModel]:
        for num, product in enumerate(external_products):
            if not product.category and product.product_properties:
                external_products[num].category = [
                    str(self.categories[property_name]) for property_name in product.product_properties
                ]
        return external_products
