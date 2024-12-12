from typing import List, Optional
from pathlib import Path
import importlib.util

from aiocache import cached
from models.products import ProductModel

# TODO: For test purposes, remove in production
import sys
sys.path.append('/home/latoff/Desktop/MarketBots')

from tgshops_integrations.nocodb_connector.client import NocodbClient
from tgshops_integrations.nocodb_connector.model_mapping import (
    dump_product_data,
    dump_product_data_with_check,
    get_pagination_info,
    ID_FIELD,
    parse_product_data,
    PRODUCT_CATEGORY_ID_LOOKUP_FIELD,
    PRODUCT_NAME_FIELD,
    PRODUCT_PRICE_FIELD,
    PRODUCT_STOCK_FIELD,
    PRODUCT_IMAGES_LOOKUP_FIELD,
    PRODUCT_EXTERNAL_ID,
)
from tgshops_integrations.nocodb_connector.categories import CategoryManager
from tgshops_integrations.nocodb_connector.products import ProductManager
from loguru import logger


def custom_key_builder(func, *args, **kwargs):
    """
    Key builder function for caching.
    Excludes 'self' by processing args from args[1:].
    """
    args_key_part = "-".join(str(arg) for arg in args[1:])
    kwargs_key_part = "-".join(f"{key}-{value}" for key, value in sorted(kwargs.items()))
    return f"{func.__name__}-{args_key_part}-{kwargs_key_part}"


class Gateway(NocodbClient):

    def __init__(
        self,
        logging: bool = False,
        NOCODB_HOST: Optional[str] = None,
        NOCODB_API_KEY: Optional[str] = None,
        SOURCE: Optional[str] = None,
        filter_buttons: Optional[List[str]] = [],
        config_path: Optional[Path] = None,
        special_attributes: bool = False,
    ):
        super().__init__(NOCODB_HOST=NOCODB_HOST, NOCODB_API_KEY=NOCODB_API_KEY, SOURCE=SOURCE)

        self.logging = logging
        self.required_fields = []
        self.projection = []
        self.special_attributes = special_attributes
        self.filter_buttons = filter_buttons

        if config_path:
            self.load_config_from_path(config_path)

    def load_config_from_path(self, config_path: Path):
        """Loads configuration from the specified path."""
        if config_path.exists():
            spec = importlib.util.spec_from_file_location("config", config_path)
            self.config = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(self.config)
        else:
            raise FileNotFoundError(f"Configuration file not found at {config_path}")

    async def load_data(self, SOURCE: Optional[str] = None):
        """Loads necessary data including tables, categories, and products."""
        self.SOURCE = SOURCE
        self.tables_list = await self.get_all_tables()
        self.products_table = self.tables_list[self.config.NOCODB_PRODUCTS]
        self.category_manager = CategoryManager(
            table_id=self.tables_list[self.config.NOCODB_CATEGORIES],
            NOCODB_HOST=self.NOCODB_HOST,
            NOCODB_API_KEY=self.NOCODB_API_KEY,
            logging=True,
            filter_buttons=self.filter_buttons,
        )
        self.product_manager = ProductManager(
            table_id=self.tables_list[self.config.NOCODB_PRODUCTS],
            NOCODB_HOST=self.NOCODB_HOST,
            NOCODB_API_KEY=self.NOCODB_API_KEY,
            logging=True,
        )

    @cached(ttl=60, key_builder=custom_key_builder)
    async def update_attributes(self, products: List[ProductModel]):
        """Updates attributes for the product table."""
        system_attributes = [PRODUCT_EXTERNAL_ID, PRODUCT_IMAGES_LOOKUP_FIELD]
        attributes = await self.get_table_meta(table_name=self.products_table)
        self.columns = [item['title'].lower() for item in attributes.get('columns', [])]

        # Ensure system attributes exist
        for attribute_name in system_attributes:
            if attribute_name.lower() not in self.columns:
                await self.create_table_column(table_name=self.products_table, name=attribute_name)
                logger.info(f"Created attribute: {attribute_name}")

        # Validate and add extra attributes
        for item in products:
            attributes = await self.get_table_meta(table_name=self.products_table)
            self.columns = [col['title'].lower() for col in attributes.get('columns', [])]

            for attribute in item.extra_attributes:
                if attribute.name.rstrip().lower() not in self.columns:
                    await self.create_table_column(table_name=self.products_table, name=attribute.name.lower())
                    logger.info(f"Created attribute: {attribute.name.lower()}")

    async def update_products(self, external_products: List[ProductModel]):
        """Updates product data by comparing with existing records."""
        await self.update_attributes(products=external_products)
        self.actual_products = await self.product_manager.get_all_products()
        self.ids_mapping = {product.external_id: product.id for product in self.actual_products}
        self.products_meta = {product.external_id: product for product in self.actual_products}

        for product in external_products:
            if product.external_id in self.ids_mapping:
                product.id = self.ids_mapping[product.external_id]
                current_hash = self.product_manager.hash_product(product, special_attributes=self.special_attributes)
                existing_hash = self.product_manager.hash_product(
                    self.products_meta[product.external_id],
                    special_attributes=self.special_attributes,
                )
                if current_hash != existing_hash:
                    await self.product_manager.update_product(product=product)
            else:
                checked_data = dump_product_data_with_check(
                    data=product,
                    data_check=self.category_manager.categories,
                )
                await self.product_manager.create_product(product=product, checked_data=checked_data)

    async def delete_all_products(self):
        """Deletes all products in the table."""
        items = await self.product_manager.get_products_v2(offset=0, limit=200)
        for item in items:
            await self.product_manager.delete_table_record(self.products_table, item.id)
