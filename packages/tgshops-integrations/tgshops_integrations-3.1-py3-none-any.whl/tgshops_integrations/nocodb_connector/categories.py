from typing import List
from loguru import logger

from aiocache import cached
from tgshops_integrations.models.categories import CategoryModel,CategoryResponseModel,CategoryListResponseModel
from tgshops_integrations.models.products import ProductModel
from tgshops_integrations.nocodb_connector.client import custom_key_builder, NocodbClient
from tgshops_integrations.nocodb_connector.model_mapping import CATEGORY_IMAGE_FIELD, CATEGORY_NAME_FIELD, CATEGORY_PARENT_FIELD, \
    CATEGORY_PARENT_ID_FIELD, PRODUCT_NAME_FIELD,CATEGORY_ID_OF_CATEGORY_FIELD, dump_category_data, get_pagination_info, parse_category_data


class CategoryManager(NocodbClient):
    def __init__(self,table_id=None,logging=False,config_type=None,NOCODB_HOST=None,NOCODB_API_KEY=None,SOURCE=None,filter_buttons=[]):
        super().__init__(NOCODB_HOST=NOCODB_HOST,NOCODB_API_KEY=NOCODB_API_KEY,SOURCE=SOURCE)
        self.NOCODB_HOST = NOCODB_HOST
        self.NOCODB_API_KEY = NOCODB_API_KEY
        self.SOURCE=SOURCE
        self.CONFIG_TYPE=config_type
        self.categories_table=table_id
        self.external_categories={}
        self.logging=logging
        self.filter_categories=[]
        self.filter_buttons=filter_buttons
        self.required_fields = [CATEGORY_NAME_FIELD]
        self.projection = ["Id", CATEGORY_NAME_FIELD, CATEGORY_PARENT_ID_FIELD, CATEGORY_ID_OF_CATEGORY_FIELD]
        # self.projection = ["Id"]

    @cached(ttl=30, key_builder=custom_key_builder)
    async def get_categories(self, table_id: str) -> List[CategoryModel]:
        records = await self.get_table_records(table_id, self.required_fields, self.projection)
        return [parse_category_data(record) for record in records]

    @cached(ttl=30, key_builder=custom_key_builder)
    async def get_categories_v2(self,
                                table_id: str,
                                offset: int = None,
                                limit: int = None) -> CategoryModel:
        response = (await self.get_table_records_v2(table_name=self.categories_table,
                                                    required_fields=self.required_fields,
                                                    projection=self.projection,
                                                    offset=offset,
                                                    limit=limit))
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
        # ! In case category_id == 0,
        # we need to get all categories without parent by field CATEGORY_PARENT_FIELD not CATEGORY_PARENT_ID_FIELD
        records = await self.get_table_records(
            table_name=self.categories_table,
            required_fields=self.required_fields,
            projection=self.projection,
            extra_where=(f"({CATEGORY_PARENT_ID_FIELD},eq,{category_id})"
                         if category_id else f"({CATEGORY_PARENT_FIELD},eq,0)"))
        return [parse_category_data(record) for record in records]

    @cached(ttl=30, key_builder=custom_key_builder)
    async def get_categories_in_category_v2(self,
                                            table_id: str,
                                            category_id: str,
                                            offset: int,
                                            limit: int) -> CategoryModel:

        response = await self.get_table_records_v2(
            table_name=self.categories_table,
            required_fields=self.required_fields,
            projection=self.projection,
            extra_where=(f"({CATEGORY_PARENT_ID_FIELD},eq,{category_id})"
                         if category_id else f"({CATEGORY_PARENT_FIELD},eq,0)"),
            offset=offset,
            limit=limit)
        categories = [parse_category_data(record) for record in response['list']]
        page_info = get_pagination_info(page_info=response['pageInfo'])
        return CategoryModel(categories=categories, page_info=page_info)

    async def update_categories(self,external_products: List[ProductModel]) -> List[ProductModel]:
        # Get the names of the tables from the DB for further handling
        self.categories=await self.get_product_categories(table_id=self.categories_table, table_name=PRODUCT_NAME_FIELD)

        categories_list=[*self.categories.keys()]
        categories_to_create=[]

        for product in external_products:
            # Check for new categories
            # DEPRECATED IF some category number exists on external side
            # if product.category:
            #     for external_category_id,category_name in zip(product.category,product.category_name):
            #         if category_name not in [*self.categories.keys()]:
            #             new_category= await self.create_product_category(table_id=self.categories_table,category_name=category_name,category_id=external_category_id,table_name=PRODUCT_NAME_FIELD)
            #             if self.logging:
            #                 logger.info(f"New Category {new_category}")
            #             self.external_categories[new_category["Id"]]=external_category_id
            #             self.categories=await self.get_product_categories(table_id=self.categories_table, table_name=PRODUCT_NAME_FIELD)
            #Else if there is just the name, create the category with new id
            # else:
                #Needs the buttons to be initialized, can connect items to buttons , which allows filtered acces through the menu
            for num,category_name in enumerate(product.category_name):
                if category_name not in categories_list:
                    if self.filter_buttons:
                        parent_id=self.categories[self.filter_buttons[num]]
                    else:
                        parent_id=self.categories[product.category_II_name[0]]
                    categories_to_create.append([category_name,parent_id])
                    categories_list.append(category_name)

        if categories_to_create:
            categories_to_create.sort(key=lambda x: x[0]) 
            if [*self.categories.values()]:
                new_id=max(self.categories.values())+1
            else:
                new_id=1
            for category,parent_id in categories_to_create:
                new_category= await self.create_product_category(table_id=self.categories_table,category_name=category,category_id=new_id,table_name=PRODUCT_NAME_FIELD)
                if self.logging:
                    logger.info(f"New Category {new_category}")
                if self.filter_buttons:
                    #Rewind categories
                    await self.link_categories(parent_id=parent_id,child_id=new_id)
                new_id+=1

    async def link_categories(self,parent_id:int,child_id:int):
        metadata = await self.get_table_meta(self.categories_table)

        linked_column = None
        for col in metadata['columns']:
            if (col["title"]=="Set parent category" and col["uidt"] == "Links"):
                linked_column = col
                break
        await self.link_table_record(
            linked_column["base_id"],
            linked_column["fk_model_id"],
            child_id,
            linked_column["id"],
            parent_id)
        
    async def unlink_categories(self,parent_id:int,child_id:int):
        metadata = await self.get_table_meta(self.categories_table)

        linked_column = None
        for col in metadata['columns']:
            if col["uidt"] == "Links":
                linked_column = col
                break
        await self.unlink_table_record(
            linked_column["base_id"],
            linked_column["fk_model_id"],
            parent_id,
            linked_column["id"],
            child_id)
    
    async def map_categories(self,external_products: List[ProductModel]) -> List[ProductModel]:
        for num,product in enumerate(external_products):
            if not product.category:
                if product.category_name:
                    external_products[num].category=[str(self.categories[category_name]) for category_name in product.category_name]
        return external_products
