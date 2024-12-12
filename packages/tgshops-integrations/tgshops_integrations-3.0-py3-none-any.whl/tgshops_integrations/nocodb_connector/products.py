from typing import List,Optional

from aiocache import cached
from tgshops_integrations.models.products import ProductModel
from tgshops_integrations.models.products import ProductModel, ProductModel
from tgshops_integrations.nocodb_connector.client import custom_key_builder, NocodbClient
from tgshops_integrations.nocodb_connector.model_mapping import dump_product_data,dump_product_data_with_check, get_pagination_info, ID_FIELD, \
    parse_product_data, PRODUCT_CATEGORY_ID_LOOKUP_FIELD, PRODUCT_NAME_FIELD, PRODUCT_PRICE_FIELD, \
    PRODUCT_STOCK_FIELD,PRODUCT_EXTERNAL_ID,PRODUCT_IMAGES_LOOKUP_FIELD

from tgshops_integrations.nocodb_connector.tables import *
from loguru import logger
import hashlib


class ProductManager(NocodbClient):

    def __init__(self, table_id=None, logging=False, NOCODB_HOST=None, NOCODB_API_KEY=None, SOURCE=None):
        super().__init__(NOCODB_HOST=NOCODB_HOST, NOCODB_API_KEY=NOCODB_API_KEY, SOURCE=SOURCE)
        self.NOCODB_HOST = NOCODB_HOST
        self.NOCODB_API_KEY = NOCODB_API_KEY
        self.SOURCE = SOURCE
        self.logging = logging
        self.required_fields = [PRODUCT_NAME_FIELD, PRODUCT_PRICE_FIELD]
        self.projection = []
        self.external_categories = {}
        self.products_table = table_id
        self.actual_products = []
        self.columns = []

    def hash_product(self,product,special_attributes=False):
        if special_attributes:
            hash_string = ''.join(attr.description for attr in product.extra_attributes if attr.name.endswith('*'))
            # hash_string = f"{product.external_id}{product.price}{product.category_name.sort()}{product.name}{product.description}"
        else:
        # Concatenate relevant attributes into a single string
            hash_string = f"{product.external_id}{product.price}{product.category_name.sort()}{product.name}{product.description}"
        # hash_string = f"{product.external_id}{product.price}{product.category_name}{product.name}{product.description}{product.preview_url}"
        # Hash the concatenated string
        hash_object = hashlib.sha256(hash_string.encode())
        hex_dig = hash_object.hexdigest()
        return hex_dig

    @cached(ttl=30, key_builder=custom_key_builder)
    async def get_products(self, table_id: str) -> List[ProductModel]:
        records = await self.get_table_records(self.products_table, self.required_fields, self.projection)
        return [parse_product_data(record) for record in records]

    # @cached(ttl=30, key_builder=custom_key_builder)
    async def get_products_v2(self, offset: int, limit: int, table_id: Optional[str] = None) -> List[ProductModel]:
        # Get the names of the tables from the DB for further handling
        await self.get_all_tables()
        response = await self.get_table_records_v2(table_name=self.products_table,
                                                   required_fields=self.required_fields,
                                                   projection=self.projection,
                                                   offset=offset,
                                                   limit=limit)
        products = [await parse_product_data(record) for record in response['list']]

        return products

    @cached(ttl=180, key_builder=custom_key_builder)
    async def search_products(self, table_id: str, search_string: str, limit: int) -> List[ProductModel]:
        records = await self.get_table_records(
            table_name=self.products_table,
            required_fields=self.required_fields,
            projection=self.projection,
            extra_where=f"({PRODUCT_NAME_FIELD},like,%{search_string}%)",  # Update with actual product name field
            limit=limit
        )
        return [parse_product_data(record) for record in records]

    @cached(ttl=180, key_builder=custom_key_builder)
    async def search_products_v2(self, table_id: str, search_string: str, limit: int) -> List[ProductModel]:
        records = (await self.get_table_records_v2(
            table_name=self.products_table,
            required_fields=self.required_fields,
            projection=self.projection,
            extra_where=f"({PRODUCT_NAME_FIELD},like,%{search_string}%)",  # Update with actual product name field
            limit=limit
        ))['list']
        return [parse_product_data(record) for record in records]

    @cached(ttl=60, key_builder=custom_key_builder)
    async def get_product(self, table_id: str, product_id: str) -> ProductModel:
        record = await self.get_table_record(self.products_table, product_id)
        return parse_product_data(record)

    @cached(ttl=60, key_builder=custom_key_builder)
    async def get_product_v2(self, table_id: str, product_id: str) -> ProductModel:
        record = await self.get_table_record(self.products_table, product_id)
        product = parse_product_data(record)

        related_products = await self.get_table_records_v2(
            table_name=self.products_table,
            required_fields=self.required_fields,
            projection=self.projection,
            extra_where=(f'({PRODUCT_STOCK_FIELD},gt,0)~and'
                         f"({PRODUCT_CATEGORY_ID_LOOKUP_FIELD},eq,{product.category[0]})~and"
                         f'({PRODUCT_NAME_FIELD},neq,{product.name})'),
            limit=5
        )
        related_products = [parse_product_data(product) for product in related_products['list']]

        product.related_products = related_products
        return product

    @cached(ttl=60, key_builder=custom_key_builder)
    async def get_product_in_category(self, table_id: str, category_id: str = None) -> List[ProductModel]:
        if category_id is None:
            return await self.get_products(table_id=self.products_table)

        records = await self.get_table_records(
            table_name=self.products_table,
            required_fields=self.required_fields,
            projection=self.projection,
            extra_where=(f'({PRODUCT_STOCK_FIELD},gt,0)~and'
                         f"({PRODUCT_CATEGORY_ID_LOOKUP_FIELD},eq,{category_id})")
        )
        return [parse_product_data(record) for record in records]

    @cached(ttl=60, key_builder=custom_key_builder)
    async def get_product_in_category_v2(self,
                                         table_id: str,
                                         offset: int,
                                         limit: int,
                                         category_id: str = None) -> ProductModel:
        if category_id is None:
            return await self.get_products_v2(table_id=self.products_table, offset=offset, limit=limit)

        response = (await self.get_table_records_v2(
            table_name=self.products_table,
            required_fields=self.required_fields,
            projection=self.projection,
            extra_where=(f'({PRODUCT_STOCK_FIELD},gt,0)~and'
                         f"({PRODUCT_CATEGORY_ID_LOOKUP_FIELD},eq,{category_id})"),
            offset=offset,
            limit=limit
        ))
        page_info = get_pagination_info(page_info=response['pageInfo'])
        products = [parse_product_data(record) for record in response['list']]
        return ProductModel(products=products, page_info=page_info)

    @cached(ttl=60, key_builder=custom_key_builder)
    async def get_products_by_ids(self, table_id: str, product_ids: list) -> List[ProductModel]:
        product_ids_str = ','.join(str(product_id) for product_id in product_ids)

        records = await self.get_table_records(
            table_name=self.products_table,
            required_fields=self.required_fields,
            projection=self.projection,
            extra_where=f"({ID_FIELD},in,{product_ids_str})")
        return [parse_product_data(record) for record in records]   

    @cached(ttl=60, key_builder=custom_key_builder)
    async def update_attributes(self,products:List[ProductModel]):
        system_attributes = [PRODUCT_EXTERNAL_ID,PRODUCT_IMAGES_LOOKUP_FIELD]
        attributes=await self.get_table_meta(table_name=self.products_table)    
        self.columns =[item['title'].lower() for item in attributes.get('columns', [])]

        #TODO Requires Validation
        for attribute_name in system_attributes:
            if attribute_name.lower() not in self.columns:
                response =await self.create_table_column(table_name=self.products_table,name=attribute_name)
                logger.info(f"Created attribute: {attribute_name}")

        for item in products:
            attributes=await self.get_table_meta(table_name=self.products_table)
            self.columns =[item['title'].lower() for item in attributes.get('columns', [])]

            for attribute in item.extra_attributes:
                if attribute.name.rstrip().lower() not in self.columns:
                    response =await self.create_table_column(table_name=self.products_table,name=attribute.name.lower())
                    logger.info(f"Created attribute: {attribute.name.lower()}")

        
    def find_product_id_by_name(self,name: str):
        for product in self.actual_products.products:
            if product.name == name:
                return product.id
        return None  # Return None if no product is found with the given name
