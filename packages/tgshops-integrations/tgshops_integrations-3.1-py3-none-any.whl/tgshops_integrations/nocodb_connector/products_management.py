from typing import List, Optional
import hashlib
from aiocache import cached
from loguru import logger
from models.products import ProductModel
from tgshops_integrations.nocodb_connector.client import custom_key_builder, NocodbClient
from tgshops_integrations.nocodb_connector.model_mapping import (
    dump_product_data,
    dump_product_data_with_check,
    get_pagination_info,
    parse_product_data,
    ID_FIELD,
    PRODUCT_CATEGORY_ID_LOOKUP_FIELD,
    PRODUCT_NAME_FIELD,
    PRODUCT_PRICE_FIELD,
    PRODUCT_STOCK_FIELD,
    PRODUCT_EXTERNAL_ID,
    PRODUCT_IMAGES_LOOKUP_FIELD,
)

class ProductManager(NocodbClient):
    def __init__(self, table_id=None, logging=False, NOCODB_HOST=None, NOCODB_API_KEY=None, SOURCE=None):
        super().__init__(NOCODB_HOST=NOCODB_HOST, NOCODB_API_KEY=NOCODB_API_KEY, SOURCE=SOURCE)
        self.logging = logging
        self.required_fields = [PRODUCT_NAME_FIELD, PRODUCT_PRICE_FIELD]
        self.projection = []
        self.products_table = table_id
        self.columns = []

    def hash_product(self, product: ProductModel, special_attributes=False) -> str:
        """
        Generates a hash of the product for comparison.
        """
        if special_attributes:
            hash_string = ''.join(attr.description for attr in product.extra_attributes if attr.name.endswith('*'))
        else:
            hash_string = f"{product.external_id}{product.price}{sorted(product.product_properties)}{product.name}{product.description}"

        return hashlib.sha256(hash_string.encode()).hexdigest()

    @cached(ttl=30, key_builder=custom_key_builder)
    async def get_products(self) -> List[ProductModel]:
        """
        Fetches all products from the table.
        """
        records = await self.get_table_records(self.products_table, self.required_fields, self.projection)
        return [parse_product_data(record) for record in records]

    async def get_products_v2(self, offset: int, limit: int) -> List[ProductModel]:
        """
        Fetches paginated products.
        """
        response = await self.get_table_records_v2(
            table_name=self.products_table,
            required_fields=self.required_fields,
            projection=self.projection,
            offset=offset,
            limit=limit,
        )
        return [await parse_product_data(record) for record in response['list']]

    @cached(ttl=180, key_builder=custom_key_builder)
    async def search_products(self, search_string: str, limit: int) -> List[ProductModel]:
        """
        Searches for products with names containing the search string.
        """
        records = await self.get_table_records(
            table_name=self.products_table,
            required_fields=self.required_fields,
            projection=self.projection,
            extra_where=f"({PRODUCT_NAME_FIELD},like,%{search_string}%)",
            limit=limit,
        )
        return [parse_product_data(record) for record in records]

    @cached(ttl=60, key_builder=custom_key_builder)
    async def get_product(self, product_id: str) -> ProductModel:
        """
        Fetches a single product by its ID.
        """
        record = await self.get_table_record(self.products_table, product_id)
        return parse_product_data(record)

    @cached(ttl=60, key_builder=custom_key_builder)
    async def get_product_in_category(self, category_id: Optional[str] = None) -> List[ProductModel]:
        """
        Fetches products within a specific category or all products if no category is specified.
        """
        extra_where = None
        if category_id:
            extra_where = f"({PRODUCT_STOCK_FIELD},gt,0)~and({PRODUCT_CATEGORY_ID_LOOKUP_FIELD},eq,{category_id})"

        records = await self.get_table_records(
            table_name=self.products_table,
            required_fields=self.required_fields,
            projection=self.projection,
            extra_where=extra_where,
        )
        return [parse_product_data(record) for record in records]

    async def update_product(self, product: ProductModel):
        """
        Updates an existing product in the table.
        """
        data = dump_product_data_with_check(data=product, data_check=self.category_manager.categories)
        await self.update_table_record(
            table_name=self.products_table,
            record_id=product.id,
            updated_data=data,
        )
        logger.info(f"Updated product {product.external_id}")

    async def create_product(self, checked_data: dict, product: ProductModel) -> ProductModel:
        """
        Creates a new product in the table.
        """
        external_id = checked_data.pop("ID")
        metadata = await self.get_table_meta(self.products_table)
        images_column = next(
            column["id"]
            for column in metadata["columns"]
            if column["column_name"] == "Images"
        )

        checked_data[PRODUCT_IMAGES_LOOKUP_FIELD] = [image['title'] for image in checked_data['Images']]

        for num, item in enumerate(checked_data['Images']):
            item['url'] = await self.save_image_to_nocodb(
                source_column_id=self.SOURCE,
                image_url=item['url'],
                image_name=item['title'],
                product_table_name=self.products_table,
                images_column_id=images_column,
            )

        record = await self.create_table_record(table_name=self.products_table, record=checked_data)
        logger.info(f"Created product {external_id}")
        return record

    async def get_all_products(self) -> List[ProductModel]:
        """
        Fetches all products in paginated portions.
        """
        all_products = []
        portion = 200
        for i in range(10):  # Limit to 10 iterations
            products_portion = await self.get_products_v2(offset=i * portion, limit=portion)
            all_products.extend(products_portion)
            if len(products_portion) < portion:
                break
        return all_products
